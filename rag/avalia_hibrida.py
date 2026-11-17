#!/usr/bin/env python3
"""Configuração C: pesquisa híbrida (densa + BM25, juntas por RRF) sobre os mesmos excertos, para cada embedding.

Para cada experiência do teste dos embeddings (modelo × A/B) e para as 15 perguntas: os 50 primeiros da pesquisa
densa e do BM25, juntos por RRF com k = 60 (pesquisa.py); métricas nos 5 primeiros com a regra do E1 (Recall@5 e
MRR@5) e com a do E2 (Recall@5 e MRR@10). Mede também o BM25 sozinho em A e em B.
A C usa a melhor configuração de cada embedding (pela regra do plano, a A em todos), mas mede-se nas duas.

Saída em experiments/E1/modelos/hibrida/: <modelo>_<A|B>/ e bm25_<A|B>/, cada uma com config.json e results.jsonl
(os 10 primeiros de cada pergunta), e resumo.md com a tabela.

Uso, na raiz do repositório (com o Ollama a correr):
  .venv\\Scripts\\python rag/avalia_hibrida.py
"""
import json
import time
from datetime import date

import avalia_embeddings
import comum
import embeddings
import metricas
import pesquisa

PASTA = comum.EXPERIENCIAS / "modelos/hibrida"


def corre(nome, modo, embedding, config):
    perguntas = comum.le_jsonl(comum.PERGUNTAS)
    if embedding:
        embeddings.embeda(embedding, ["aquecimento"], "query")
    linhas, tempos = [], []
    for p in perguntas:
        t = time.perf_counter()
        recuperados = pesquisa.recupera(modo, embedding, config, p["question"], 10)
        tempos.append(time.perf_counter() - t)
        linhas.append({"question_id": p["id"], "type": p["type"], "config": config, "retrieved": recuperados,
                       **metricas.avalia(p["evidence"], recuperados),
                       "e2": metricas.avalia(p["evidence"], recuperados, regra="E2")})
    e2 = metricas.resumo([{"type": x["type"]} | x["e2"] for x in linhas])
    cfg = {"experiment": nome, "area": "E1", "date": date.today().isoformat(), "git_commit": comum.commit_git(),
           "retrieval": pesquisa.parametros(modo, embedding, config) | {"k": metricas.K, "top_logged": 10},
           "metrics": metricas.resumo(linhas),
           "metrics_e2": {"recall_at_5": e2["recall_at_5"], "mrr_at_10": e2["mrr_at_5"],
                          "cobertura_total_multi_doc": e2.get("cobertura_total_multi_doc")},
           "query_ms_media": round(1000 * sum(tempos) / len(tempos), 1)}
    pasta = PASTA / nome
    comum.grava_jsonl(pasta / "results.jsonl", linhas)
    (pasta / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return cfg


def main():
    comum.prepara_consola()
    num = avalia_embeddings.num
    densas = avalia_embeddings.le_configs()
    linhas_md = []
    for config in ("A", "B"):
        c = corre(f"bm25_{config}", "bm25", None, config)
        linhas_md.append(f"| BM25 sozinho | {config} | — | — | {num(c['metrics']['recall_at_5'])} | {num(c['metrics']['mrr_at_5'])} "
                         f"| {num(c['metrics'].get('cobertura_total_multi_doc', 0), 2)} | {num(c['metrics_e2']['recall_at_5'])} "
                         f"| {num(c['metrics_e2']['mrr_at_10'])} |")
        print(f"BM25 {config}: Recall@5 {num(c['metrics']['recall_at_5'])}, MRR@5 {num(c['metrics']['mrr_at_5'])}", flush=True)
    for d in densas:
        modelo, config = d["embedding"]["name"], d["chunks"]["config"]
        c = corre(f"{modelo}_{config}", "hybrid", modelo, config)
        m, e2, dm = c["metrics"], c["metrics_e2"], d["metrics"]
        linhas_md.append(f"| {modelo} | {config} | {num(dm['recall_at_5'])} | {num(dm['mrr_at_5'])} | {num(m['recall_at_5'])} "
                         f"| {num(m['mrr_at_5'])} | {num(m.get('cobertura_total_multi_doc', 0), 2)} | {num(e2['recall_at_5'])} "
                         f"| {num(e2['mrr_at_10'])} |")
        print(f"C com {modelo} {config}: Recall@5 {num(m['recall_at_5'])} (densa {num(dm['recall_at_5'])}), "
              f"MRR@5 {num(m['mrr_at_5'])} (densa {num(dm['mrr_at_5'])})", flush=True)
    b = json.loads((PASTA / "bm25_A" / "config.json").read_text(encoding="utf-8"))["retrieval"]
    md = ["# Configuração C (E1): pesquisa híbrida, densa + BM25 por RRF", "",
          f"{date.today():%d/%m/%Y}. 12 perguntas com resposta. BM25: {b['bm25']['variant']}, k1 = {num(b['bm25']['k1'], 1)}, "
          f"b = {num(b['bm25']['b'], 2)}; minúsculas, tokens `\\w+`, stopwords {b['bm25']['stopwords']}, {b['bm25']['stemmer']} "
          f"(NLTK {b['bm25']['nltk_version']}). RRF com k = {pesquisa.RRF_K} e os {pesquisa.CANDIDATOS} primeiros de cada pesquisa; "
          "empates pela posição na densa. A densa é a do teste dos embeddings, sobre os mesmos excertos.", "",
          "| Embedding | Excertos | Recall@5 densa | MRR@5 densa | Recall@5 C | MRR@5 C | Cobertura multi_doc C "
          "| Recall@5 C (E2) | MRR@10 C (E2) |",
          "|---|---|---|---|---|---|---|---|---|"] + linhas_md
    (PASTA / "resumo.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print(f"Tabela em {(PASTA / 'resumo.md').relative_to(comum.RAIZ)}")


if __name__ == "__main__":
    main()
