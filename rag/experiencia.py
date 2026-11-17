#!/usr/bin/env python3
"""Experiências finais do E1 (A, B e C), de ponta a ponta, a partir do config.json de cada pasta.

O config.json (experiments/E1/A, B ou C) diz o que muda entre experiências:
  {"experiment": "A", "provisional": true, "note": "...",
   "retrieval": {"mode": "dense" ou "hybrid", "embedding": "qwen3-embedding-8b", "chunks": "A", "B" ou "best_of_AB", "k": 5},
   "llm": "gemma4-12b",
   "prompt": {"abstention_phrase": "...", "citation_format": "doc" ou "excerto"},
   "judge": "gpt-oss-120b"}
"best_of_AB" (para a C) aplica a regra do plano aos resultados já corridos de A e de B: maior Recall@5, depois
maior MRR@5, depois maior média do juiz (correção + fidelidade), depois a B.

Passos:
  1. Recuperação das 15 perguntas (os 10 primeiros ficam guardados) e métricas: regra do E1 e, à parte, a do E2.
  2. Geração com o LLM, com os 5 primeiros excertos (aquecimento com a 1.ª pergunta, deitado fora), e as
     verificações em código (abstenção com a frase fixa, citações no formato, ids fora dos excertos).
  3. Só com --juiz: avaliação pelo juiz, retomável, em juiz_<juiz>.jsonl (salta o que já foi avaliado com o mesmo
     prompt do juiz e a mesma resposta; com o Groq, para de forma limpa no limite diário).
O script acrescenta ao config.json a secção "run" (versões, parâmetros completos, data, commit e resumos), grava
results.jsonl e resumo.md na pasta e refaz experiments/E1/resumo_ABC.md.

Uso, na raiz do repositório (com o Ollama a correr):
  .venv\\Scripts\\python rag/experiencia.py experiments/E1/A/config.json
  .venv\\Scripts\\python rag/experiencia.py experiments/E1/C/config.json --so-pesquisa
  .venv\\Scripts\\python rag/experiencia.py experiments/E1/A/config.json --so-juiz
  .venv\\Scripts\\python rag/experiencia.py experiments/E1/A/config.json --so-juiz --espera
"""
import argparse
import hashlib
import json
import re
import statistics
import time
from datetime import date
from pathlib import Path

import avalia_embeddings
import avalia_juiz
import avalia_llm
import cliente_groq
import comum
import embeddings
import geracao
import juiz
import metricas
import pesquisa
import prompt_geracao
import prompt_juiz

PASTA = comum.EXPERIENCIAS


def le(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def grava(caminho, dados):
    Path(caminho).write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def escolhe_excertos(cfg):
    """A configuração de excertos: a do config.json ou, com best_of_AB, a melhor de A e B pela regra do plano."""
    pedido = cfg["retrieval"]["chunks"]
    if pedido != "best_of_AB":
        return pedido, None
    corridas = {n: le(PASTA / n / "config.json")["run"] for n in ("A", "B")}
    juiz_ = lambda r: (r.get("grid_summary") or {}).get("correcao_media", 0) + (r.get("grid_summary") or {}).get("fidelidade_media", 0)
    chave = lambda n: (round(corridas[n]["retrieval_metrics"]["recall_at_5"], 6), round(corridas[n]["retrieval_metrics"]["mrr_at_5"], 6),
                       round(juiz_(corridas[n]), 6), n == "B")
    melhor = max(("A", "B"), key=chave)
    porque = {n: {"recall_at_5": corridas[n]["retrieval_metrics"]["recall_at_5"], "mrr_at_5": corridas[n]["retrieval_metrics"]["mrr_at_5"],
                  "juiz_correcao_mais_fidelidade": juiz_(corridas[n]) or None} for n in ("A", "B")}
    return corridas[melhor]["chunks"], {"rule": "Recall@5, depois MRR@5, depois juiz (correção + fidelidade), depois B",
                                         "chosen": melhor, "candidates": porque}


def recupera(cfg, chunks):
    r, perguntas = cfg["retrieval"], comum.le_jsonl(comum.PERGUNTAS)
    if r["mode"] != "bm25":
        embeddings.embeda(r["embedding"], ["aquecimento"], "query")
    linhas = []
    for p in perguntas:
        topo = pesquisa.recupera(r["mode"], r.get("embedding"), chunks, p["question"], 10)
        linhas.append({"question_id": p["id"], "type": p["type"], "config": cfg["experiment"], "chunks": chunks,
                       "retrieved": topo, **metricas.avalia(p["evidence"], topo, k=r["k"]),
                       "e2": metricas.avalia(p["evidence"], topo, k=r["k"], regra="E2")})
    return linhas


def gera(cfg, linhas, chunks):
    por_id = {x["chunk_id"]: x for x in pesquisa.excertos(chunks)}
    perguntas = {p["id"]: p for p in comum.le_jsonl(comum.PERGUNTAS)}
    k, frase, formato = cfg["retrieval"]["k"], cfg["prompt"]["abstention_phrase"], cfg["prompt"]["citation_format"]
    contexto = lambda x: [por_id[c["chunk_id"]] for c in x["retrieved"][:k]]
    geracao.responde(cfg["llm"], perguntas[linhas[0]["question_id"]]["question"], contexto(linhas[0]), frase, formato)  # aquecimento
    for x in linhas:
        r = geracao.responde(cfg["llm"], perguntas[x["question_id"]]["question"], contexto(x), frase, formato)
        x.update(r | geracao.verifica(r["answer"], contexto(x), frase, formato))
        print(f"  {x['question_id']}: {r['latency_s']} s, {r['tokens_out']} tokens", flush=True)
    return linhas


def avalia_com_juiz(cfg, pasta, linhas, chunks, espera=False):
    """Com espera=True, no limite diário do Groq espera o tempo que o Groq indica e continua (como no avalia_juiz.py)."""
    nome = cfg["judge"]
    caminho = pasta / f"juiz_{nome}.jsonl"
    feitas = {x["question_id"]: x for x in comum.le_jsonl(caminho)} if caminho.exists() else {}
    por_id = {x["chunk_id"]: x for x in pesquisa.excertos(chunks)}
    perguntas = {p["id"]: p for p in comum.le_jsonl(comum.PERGUNTAS)}
    versao = avalia_juiz.versao_prompt()
    for x in linhas:
        sha = hashlib.sha1(x["answer"].encode("utf-8")).hexdigest()
        if avalia_juiz.em_dia(feitas.get(x["question_id"]), x["answer"], perguntas[x["question_id"]]):
            continue
        excertos = [por_id[c["chunk_id"]] for c in x["retrieved"][:cfg["retrieval"]["k"]]]
        while True:
            try:
                corridas, agregado = juiz.avalia(nome, perguntas[x["question_id"]], excertos, x["answer"], cfg["prompt"]["citation_format"])
                break
            except cliente_groq.LimiteDiario as e:
                falta = sum(q not in feitas for q in (y["question_id"] for y in linhas))
                if not espera:
                    print(f"Limite diário do Groq: {e}\nParei de forma limpa; faltam {falta} respostas.")
                    return feitas
                pausa = max(60.0, cliente_groq._segundos((re.search(r"try again in (\S+?)\.?\s", str(e) + " ") or [None, ""])[1]))
                print(f"  limite diário do Groq; faltam {falta}; espero {pausa:.0f} s ({time.strftime('%H:%M')})", flush=True)
                time.sleep(pausa)
        feitas[x["question_id"]] = {"question_id": x["question_id"], "judge_model": nome, "judge_prompt": versao, "answer_sha1": sha,
                                    "reference_sha1": avalia_juiz.sha_referencia(perguntas[x["question_id"]]),
                                    "judge_runs": corridas, "judge": agregado}
        comum.grava_jsonl(caminho, [feitas[y["question_id"]] for y in linhas if y["question_id"] in feitas])
        print(f"  juiz {x['question_id']}: correção {agregado['correcao']}, fidelidade {agregado['fidelidade']}", flush=True)
    return feitas


def resumo_recuperacao(linhas):
    m = metricas.resumo(linhas)
    e2 = metricas.resumo([{"type": x["type"]} | x["e2"] for x in linhas])
    return m, {"recall_at_5": e2["recall_at_5"], "mrr_at_10": e2["mrr_at_5"], "cobertura_total_multi_doc": e2.get("cobertura_total_multi_doc")}


def corre(caminho_cfg, so_pesquisa=False, so_juiz=False, espera=False):
    caminho_cfg = Path(caminho_cfg)
    pasta, cfg = caminho_cfg.parent, le(caminho_cfg)
    run = cfg.get("run", {})
    if so_juiz:
        linhas, chunks = comum.le_jsonl(pasta / "results.jsonl"), run["chunks"]
    else:
        chunks, escolha = escolhe_excertos(cfg)
        print(f"{cfg['experiment']}: excertos {chunks}, pesquisa {cfg['retrieval']['mode']}", flush=True)
        linhas = recupera(cfg, chunks)
        m, e2 = resumo_recuperacao(linhas)
        r = cfg["retrieval"]
        run = {"date": date.today().isoformat(), "git_commit": comum.commit_git(), "chunks": chunks, "chunks_choice": escolha,
               "chunks_meta": {k: v for k, v in le(PASTA / f"excertos_{chunks}.json").items() if k != "documents_sha1"},
               "retrieval": pesquisa.parametros(r["mode"], r.get("embedding"), chunks) | {"k": r["k"], "top_logged": 10},
               "embedding_model": embeddings.info(r["embedding"]) if r["mode"] != "bm25" else None,
               "retrieval_metrics": m, "retrieval_metrics_e2": e2}
        if not so_pesquisa:
            gera(cfg, linhas, chunks)
            run |= {"llm_model": geracao.info(cfg["llm"]) | {"options": geracao.OPCOES, "ollama_version": comum.versao_ollama()},
                    "prompt": {"version": prompt_geracao.VERSAO, "sha1": prompt_geracao.sha1(cfg["prompt"]["abstention_phrase"],
                                                                                            cfg["prompt"]["citation_format"])},
                    "warmup": "1.ª pergunta, resposta deitada fora", "gpu": avalia_embeddings.gpu(),
                    "generation_summary": avalia_llm.resume(linhas)}
        comum.grava_jsonl(pasta / "results.jsonl", linhas)
    if so_juiz:
        feitas = avalia_com_juiz(cfg, pasta, linhas, chunks, espera)
        if all(x["question_id"] in feitas for x in linhas):
            run["judge"] = juiz.parametros(cfg["judge"]) | {"prompt_version": prompt_juiz.VERSAO, "prompt_sha1": prompt_juiz.sha1()}
            run["grid_summary"] = avalia_juiz.resume_grelha(linhas, feitas)
    cfg["run"] = run
    grava(caminho_cfg, cfg)
    escreve_resumo(pasta, cfg)
    escreve_resumo_geral()
    return cfg


def num(x, c=3):
    return "—" if x is None else f"{x:.{c}f}".replace(".", ",")


def linha_tabela(cfg):
    r = cfg["run"]
    m, e2, g, s = r["retrieval_metrics"], r["retrieval_metrics_e2"], r.get("grid_summary") or {}, r.get("generation_summary") or {}
    return (f"| {cfg['experiment']} | {r['chunks']} | {r['retrieval']['mode']} | {num(m['recall_at_5'])} | {num(m['mrr_at_5'])} "
            f"| {num(m.get('cobertura_total_multi_doc'), 2)} | {num(e2['recall_at_5'])} | {num(e2['mrr_at_10'])} "
            f"| {s.get('abstencao_correta', '—')} | {s.get('falsa_abstencao', '—')} | {s.get('respostas_com_citacao', '—')} "
            f"| {num(g.get('correcao_media'), 2)} | {num(g.get('fidelidade_media'), 2)} | {num(g.get('citacoes_media'), 2)} "
            f"| {num(s.get('latencia_media_s'), 1)} |")


CABECALHO = ["| Exp. | Excertos | Pesquisa | Recall@5 | MRR@5 | Cobertura multi_doc | Recall@5 (E2) | MRR@10 (E2) "
             "| Abstenção correta | Falsa abstenção | Respostas com citação | Correção (juiz) | Fidelidade (juiz) | Citações (juiz) "
             "| Latência (s) |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]


def cabecalho_texto(cfg):
    r = cfg["run"]
    aviso = f"**Provisório**: {cfg.get('note', '')} " if cfg.get("provisional") else ""
    return (f"{aviso}Embedding `{cfg['retrieval'].get('embedding')}`, LLM `{cfg['llm']}`, juiz `{cfg['judge']}` "
            f"({'avaliado' if r.get('grid_summary') else 'ainda não avaliado'}). Frase de abstenção: «{cfg['prompt']['abstention_phrase']}». "
            f"Citações: formato «{cfg['prompt']['citation_format']}». k = {cfg['retrieval']['k']}.")


def escreve_resumo(pasta, cfg):
    md = [f"# Experiência {cfg['experiment']} (E1)", "", f"{cfg['run']['date']}. " + cabecalho_texto(cfg), ""] + CABECALHO + [linha_tabela(cfg)]
    if cfg["run"].get("chunks_choice"):
        md += ["", f"Excertos escolhidos pela regra do plano: {cfg['run']['chunks_choice']['chosen']} "
                   f"({json.dumps(cfg['run']['chunks_choice']['candidates'], ensure_ascii=False)})."]
    (pasta / "resumo.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")


def escreve_resumo_geral():
    cfgs = [le(PASTA / n / "config.json") for n in ("A", "B", "C") if (PASTA / n / "config.json").exists()]
    cfgs = [c for c in cfgs if "run" in c]
    if not cfgs:
        return
    md = ["# Experiências A, B e C (E1)", "", cabecalho_texto(cfgs[0]), ""] + CABECALHO + [linha_tabela(c) for c in cfgs]
    (PASTA / "resumo_ABC.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description="Corre uma experiência final do E1 (A, B ou C) a partir do config.json.")
    ap.add_argument("config", nargs="+", help="um ou mais config.json (por ordem: A e B antes da C)")
    ap.add_argument("--so-pesquisa", action="store_true", help="só a recuperação e as métricas, sem o LLM")
    ap.add_argument("--so-juiz", action="store_true", help="só a avaliação pelo juiz, sobre as respostas já geradas")
    ap.add_argument("--espera", action="store_true", help="com --so-juiz: no limite diário do Groq, espera e continua em vez de parar")
    args = ap.parse_args()
    comum.prepara_consola()
    for c in args.config:
        cfg = corre(c, args.so_pesquisa, args.so_juiz, args.espera)
        m = cfg["run"]["retrieval_metrics"]
        print(f"{cfg['experiment']}: Recall@5 {num(m['recall_at_5'])}, MRR@5 {num(m['mrr_at_5'])}"
              + (f"; {cfg['run']['generation_summary']}" if cfg["run"].get("generation_summary") else ""), flush=True)
    print(f"Tabela em {(PASTA / 'resumo_ABC.md').relative_to(comum.RAIZ)}")


if __name__ == "__main__":
    main()
