#!/usr/bin/env python3
"""Teste dos modelos de embeddings para o grupo (7/11): Recall@5, MRR@5, cobertura das multi_doc e tempo.

Para cada modelo e configuração:
  1. o aquecimento (ver aquece) e depois os embeddings de todos os excertos (tempo de indexação);
  2. a coleção no ChromaDB (indice.py);
  3. as 15 perguntas: embedding da pergunta e pesquisa dos 10 primeiros (tempo médio por pergunta);
  4. as métricas dos 5 primeiros (metricas.py) e a confirmação de que o HNSW deu o mesmo que a pesquisa exata.

Saída em experiments/E1/modelos/embeddings/:
  <modelo>_<A|B>/config.json    modelo (com o digest), excertos, índice, métricas e tempos
  <modelo>_<A|B>/results.jsonl  uma linha por pergunta: os 10 primeiros excertos e as métricas
  resumo.md                     a tabela para o grupo, com todas as pastas que existirem

Uso, na raiz do repositório (com o Ollama a correr):
  .venv\\Scripts\\python rag/avalia_embeddings.py                              todos os modelos, A e B
  .venv\\Scripts\\python rag/avalia_embeddings.py --modelo bge-m3 --config B   só um
"""
import argparse
import json
import statistics
import subprocess
import time
from datetime import date

import chromadb
import numpy as np

import comum
import embeddings
import indice
import metricas

PASTA = comum.EXPERIENCIAS / "modelos/embeddings"
TOPO = 10  # registados para a análise de erros; as métricas usam os 5 primeiros


def gpu():
    try:
        return subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def aquece(modelo, excertos):
    """Na primeira utilização de cada tamanho de entrada, a GPU compila kernels (até 4 s de cada vez, porque esta versão
    do Ollama não traz código compilado para a RTX 5060 Ti). Sem aquecimento, o tempo por pergunta media a compilação.
    Aquece com um lote de excertos e com textos de 2 a 80 palavras, que não são as perguntas."""
    embeddings.embeda(modelo, [x["text"] for x in excertos[:embeddings.LOTE]], "document")
    palavras = " ".join(x["text"] for x in excertos[:3]).split()
    for n in range(2, 81, 3):
        embeddings.embeda(modelo, [" ".join(palavras[:n])], "query")


def corre(modelo, config):
    excertos = comum.le_jsonl(comum.EXPERIENCIAS / f"excertos_{config}.jsonl")
    meta_excertos = json.loads((comum.EXPERIENCIAS / f"excertos_{config}.json").read_text(encoding="utf-8"))
    perguntas = comum.le_jsonl(comum.PERGUNTAS)
    info = embeddings.info(modelo)

    aquece(modelo, excertos)
    t = time.perf_counter()
    V = embeddings.embeda(modelo, [x["text"] for x in excertos], "document")
    t_indexacao = time.perf_counter() - t

    nome = indice.nome_colecao(modelo, config)
    col = indice.cria(indice.cliente(), nome, excertos, V,
                      {"modelo": info["ollama_model"], "digest": info["digest"] or "", "config": config})

    linhas, tempos, iguais = [], [], 0
    for p in perguntas:
        t = time.perf_counter()
        q = embeddings.embeda(modelo, [p["question"]], "query")[0]
        recuperados = indice.pesquisa(col, q, TOPO)
        tempos.append(time.perf_counter() - t)
        exata = [excertos[i]["chunk_id"] for i in np.argsort(-(V @ q), kind="stable")[:TOPO]]
        iguais += exata == [r["chunk_id"] for r in recuperados]
        linhas.append({"question_id": p["id"], "type": p["type"], "config": config, "embedding": modelo,
                       "retrieved": recuperados} | metricas.avalia(p["evidence"], recuperados))

    pasta = PASTA / f"{modelo}_{config}"
    comum.grava_jsonl(pasta / "results.jsonl", linhas)
    cfg = {"experiment": f"{modelo}_{config}", "area": "E1", "date": date.today().isoformat(), "git_commit": comum.commit_git(),
           "embedding": info,
           "chunks": {"file": f"experiments/E1/excertos_{config}.jsonl", "excertos": len(excertos),
                      **{k: meta_excertos[k] for k in ("config", "max_tokens", "overlap_tokens", "tokenizer", "tokenizer_revision")}},
           "index": {"type": "chromadb", "chromadb_version": chromadb.__version__, "collection": nome, **indice.HNSW},
           "retrieval": {"k": metricas.K, "top_logged": TOPO},
           "metrics": metricas.resumo(linhas),
           "timing": {"gpu": gpu(), "index_s": round(t_indexacao, 1), "excertos_por_s": round(len(excertos) / t_indexacao, 1),
                      "query_ms_media": round(1000 * statistics.mean(tempos), 1)},
           "hnsw_igual_a_exata": f"{iguais}/{len(perguntas)}"}
    (pasta / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return cfg


def num(x, casas=3):
    return f"{x:.{casas}f}".replace(".", ",")


def le_configs():
    ordem = list(embeddings.MODELOS)
    cfgs = [json.loads(c.read_text(encoding="utf-8")) for c in PASTA.glob("*/config.json")]
    return sorted(cfgs, key=lambda c: (ordem.index(c["embedding"]["name"]), c["chunks"]["config"]))


def melhor(cfgs):
    """Regra do plano: maior Recall@5, depois maior MRR@5, depois a B."""
    return max(cfgs, key=lambda c: (round(c["metrics"]["recall_at_5"], 6), round(c["metrics"]["mrr_at_5"], 6),
                                    c["chunks"]["config"] == "B"))


def escreve_resumo():
    cfgs = le_configs()
    melhor_ = melhor(cfgs)
    md = ["# Teste dos modelos de embeddings (E1)", "",
          f"{date.today():%d/%m/%Y}. 12 perguntas com resposta (8 factual, 4 multi_doc); as 3 sem resposta não entram. "
          "Métricas nos 5 primeiros excertos, com acerto a partir de 50% do mais curto (excerto ou trecho). "
          "Com estes excertos, o teto do Recall@5 é 1 em A e em B. "
          f"Tempos numa {cfgs[0]['timing']['gpu']}, Ollama {cfgs[0]['embedding']['ollama_version']}, "
          "depois de um aquecimento com textos de 2 a 80 palavras (a GPU compila kernels na primeira utilização).", "",
          "| Modelo | Config. | Recall@5 | MRR@5 | Cobertura total das multi_doc | Recall@5 factual | Recall@5 multi_doc "
          "| Indexação (s) | Por pergunta (ms) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for c in cfgs:
        m, t = c["metrics"], c["timing"]
        nome = f"**{c['embedding']['name']}**" if c is melhor_ else c["embedding"]["name"]
        md.append(f"| {nome} | {c['chunks']['config']} | {num(m['recall_at_5'])} | {num(m['mrr_at_5'])} "
                  f"| {num(m.get('cobertura_total_multi_doc', 0), 2)} | {num(m.get('recall_at_5_factual', 0))} "
                  f"| {num(m.get('recall_at_5_multi_doc', 0))} | {num(t['index_s'], 1)} | {num(t['query_ms_media'], 0)} |")
    md += ["", f"A negrito, a melhor pela regra do plano (Recall@5, depois MRR@5, depois B): "
               f"{melhor_['embedding']['name']} na {melhor_['chunks']['config']}.", "",
           "| Modelo | No Ollama | Digest | Quantização | Dimensões | Prefixo das perguntas | Prefixo dos excertos |",
           "|---|---|---|---|---|---|---|"]
    vistos = set()
    for c in cfgs:
        e = c["embedding"]
        if e["name"] in vistos:
            continue
        vistos.add(e["name"])
        celula = lambda p: "`" + p.replace("\n", "⏎").replace("|", "\\|") + "`" if p else "—"  # | partia a tabela
        md.append(f"| {e['name']} | `{e['ollama_model']}` | `{(e['digest'] or '')[:12]}` | {e['quantization']} | {e['dimensions']} "
                  f"| {celula(e['query_prefix'])} | {celula(e['document_prefix'])} |")
    md += ["", "O embeddinggemma-sem-prefixos é um desvio ao plano, decidido a 6/11: num teste prévio com os 25 trechos das "
               "perguntas, o EmbeddingGemma do Ollama acertou 7 em 12 com os prefixos do model card e 10 em 12 sem eles."]
    (PASTA / "resumo.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description="Testa os modelos de embeddings do E1 nas configurações A e B.")
    ap.add_argument("--modelo", choices=list(embeddings.MODELOS), action="append", help="por omissão, todos")
    ap.add_argument("--config", choices=["A", "B"], action="append", help="por omissão, A e B")
    args = ap.parse_args()
    comum.prepara_consola()
    for modelo in args.modelo or embeddings.MODELOS:
        for config in args.config or ["A", "B"]:
            c = corre(modelo, config)
            m, t = c["metrics"], c["timing"]
            print(f"{modelo} {config}: Recall@5 {num(m['recall_at_5'])}, MRR@5 {num(m['mrr_at_5'])}, "
                  f"cobertura multi_doc {num(m.get('cobertura_total_multi_doc', 0), 2)}; indexação {num(t['index_s'], 1)} s, "
                  f"{num(t['query_ms_media'], 0)} ms por pergunta; HNSW igual à pesquisa exata em {c['hnsw_igual_a_exata']}",
                  flush=True)
    escreve_resumo()
    print(f"Tabela em {(PASTA / 'resumo.md').relative_to(comum.RAIZ)}")


if __name__ == "__main__":
    main()
