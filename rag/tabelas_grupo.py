#!/usr/bin/env python3
"""Tabelas para a mensagem ao grupo (8/11), no formato da do E3: texto com tabulações e os números da «Leitura».

Embeddings: Recall@5 e MRR@5 (regra do E1) na A e na B (pesquisa densa) e na C (A + BM25 por RRF, k = 60), para
todos os modelos testados, por ordem do Recall@5 na A.
LLM (com um juiz): correção em pontos na A, na B e na C (12 perguntas com resposta × 2 = 24 por configuração) e o
total em 72; fidelidade, afirmações sem suporte e citações nas respostas que não se abstêm; segundos por resposta.
Só entram as configurações com as 15 respostas avaliadas; as outras ficam com «—».
Números para a leitura: respostas só com a frase de abstenção, pontos por configuração, perguntas em que todos
falham, o peso de cada pergunta na diferença entre os dois primeiros e o tamanho de cada modelo no Ollama.

Saída: experiments/E1/tabelas_grupo_<juiz>.md (as tabelas e os números) e o mesmo texto no ecrã.
Uso: .venv\\Scripts\\python rag/tabelas_grupo.py --juiz gpt-oss-20b
"""
import argparse
import json
import statistics
from collections import defaultdict

import ollama

import avalia_embeddings
import avalia_llm
import comum
import geracao
import prompt_geracao

NOMES = {"gemma4-12b": "Gemma 4 12B", "qwen3.5-9b": "Qwen3.5 9B", "amalia-9b": "AMALIA 9B", "ministral-3-14b": "Ministral 3 14B"}


def num(x, c=3):
    return "—" if x is None else f"{x:.{c}f}".replace(".", ",")


def pontos(x):
    return "—" if x is None else (f"{x:.0f}" if float(x).is_integer() else f"{x:.1f}".replace(".", ","))


def tabela_embeddings():
    hib = comum.EXPERIENCIAS / "modelos/hibrida"
    por = defaultdict(dict)
    for c in avalia_embeddings.le_configs():
        por[c["embedding"]["name"]][c["chunks"]["config"]] = c["metrics"]
    for nome in por:
        f = hib / f"{nome}_A" / "config.json"
        if f.exists():
            por[nome]["C"] = json.loads(f.read_text(encoding="utf-8"))["metrics"]
    variantes = {"embeddinggemma-sem-prefixos": " (variante)", "embeddinggemma-titulo": " (variante)"}
    ordem = sorted(por, key=lambda n: (-por[n]["A"]["recall_at_5"], -por[n]["A"]["mrr_at_5"]))
    linhas = ["Modelo\tA: Recall@5\tA: MRR@5\tB: Recall@5\tB: MRR@5\tC: Recall@5\tC: MRR@5"]
    for n in ordem:
        m = por[n]
        linhas.append("\t".join([n + variantes.get(n, "")] + [num(m.get(c, {}).get(k)) for c in "ABC" for k in ("recall_at_5", "mrr_at_5")]))
    return linhas


def dados_llm(juiz):
    """Por LLM e configuração: as linhas do results.jsonl e as avaliações do juiz (só se as 15 estiverem avaliadas)."""
    d = defaultdict(dict)
    for config, pasta in avalia_llm.PASTAS.items():
        for m in geracao.LLMS:
            r, j = pasta / m / "results.jsonl", pasta / m / f"juiz_{juiz}.jsonl"
            if r.exists() and j.exists():
                linhas, aval = comum.le_jsonl(r), {x["question_id"]: x["judge"] for x in comum.le_jsonl(j)}
                if all(x["question_id"] in aval for x in linhas):
                    d[m][config] = (linhas, aval)
    return d


def so_frase(resposta):
    t = resposta.strip().strip("«»\"“”*_ ").rstrip(".")
    return t == prompt_geracao.ABSTENCAO.rstrip(".")


def tabela_llm(juiz):
    d = dados_llm(juiz)
    tamanhos = {x.model: x.size for x in ollama.list().models}
    resumo = {}
    for m, configs in d.items():
        pts = {c: sum(a[x["question_id"]]["correcao"] for x in linhas if x["type"] != "unanswerable")
               for c, (linhas, a) in configs.items()}
        todas = [(x, a[x["question_id"]]) for linhas, a in configs.values() for x in linhas]
        respostas = [(x, j) for x, j in todas if not x["abstained"]]
        sem = [x for x, _ in todas if x["type"] == "unanswerable"]
        resumo[m] = {"pontos": pts, "total": sum(pts.values()) if len(pts) == 3 else None,
                     "fidelidade": statistics.mean(j["fidelidade"] for _, j in respostas if j["fidelidade"] is not None),
                     "sem_suporte": sum(j["nao_suportadas"] or 0 for _, j in respostas),
                     "citacoes": statistics.mean(j["citacoes"] for _, j in respostas if j["citacoes"] is not None),
                     "segundos": statistics.mean(x["latency_s"] for x, _ in todas),
                     "so_frase": f"{sum(so_frase(x['answer']) for x in sem)} de {len(sem)}",
                     "gb": round(tamanhos.get(geracao.LLMS[m], 0) / 1e9, 1)}
    ordem = sorted(resumo, key=lambda m: -(resumo[m]["total"] if resumo[m]["total"] is not None else sum(resumo[m]["pontos"].values())))
    linhas = ["Modelo\tA\tB\tC\tTotal em 72\tFidelidade\tSem suporte\tCitações (0 a 2)\tSegundos por resposta"]
    for m in ordem:
        r = resumo[m]
        linhas.append("\t".join([NOMES[m]] + [pontos(r["pontos"].get(c)) for c in "ABC"]
                                + [pontos(r["total"]), num(r["fidelidade"], 2), str(r["sem_suporte"]), num(r["citacoes"], 2),
                                   num(r["segundos"], 1)]))
    return linhas, resumo, d, ordem


def leitura(resumo, d, ordem):
    """Os números para a «Leitura»."""
    out = []
    configs = sorted({c for m in d for c in d[m]})
    for c in configs:
        tot = sum(resumo[m]["pontos"][c] for m in resumo if c in resumo[m]["pontos"])
        falham = []
        for x in next(iter(d.values()))[c][0]:
            q = x["question_id"]
            if x["type"] == "unanswerable":
                continue
            notas = [d[m][c][1][q]["correcao"] for m in d if c in d[m]]
            if max(notas) < 2:
                falham.append(f"{q} ({'/'.join(pontos(n) for n in notas)})")
        out.append(f"{c}: {pontos(tot)} pontos somando os {len([m for m in d if c in d[m]])} LLM; perguntas sem nenhum 2: {', '.join(falham) or 'nenhuma'}")
    if len(ordem) >= 2:
        a, b = ordem[0], ordem[1]
        difs = defaultdict(float)
        for c in configs:
            if c in d[a] and c in d[b]:
                for x in d[a][c][0]:
                    if x["type"] != "unanswerable":
                        q = x["question_id"]
                        difs[f"{q} na {c}"] += d[a][c][1][q]["correcao"] - d[b][c][1][q]["correcao"]
        total = sum(difs.values())
        maiores = sorted(((k, v) for k, v in difs.items() if v), key=lambda kv: -abs(kv[1]))
        out.append(f"{NOMES[a]} − {NOMES[b]}: {pontos(total)} pontos; diferenças por pergunta: "
                   + ", ".join(f"{k} {'+' if v > 0 else ''}{pontos(v)}" for k, v in maiores))
    for m in ordem:
        out.append(f"{NOMES[m]}: só a frase de abstenção em {resumo[m]['so_frase']} respostas sem resposta; "
                   f"{num(resumo[m]['segundos'], 2)} s por resposta; {num(resumo[m]['gb'], 1)} GB no Ollama")
    return out


def main():
    ap = argparse.ArgumentParser(description="Tabelas do E1 para a mensagem ao grupo.")
    ap.add_argument("--juiz", default="gpt-oss-20b")
    args = ap.parse_args()
    comum.prepara_consola()
    emb = tabela_embeddings()
    llm, resumo, d, ordem = tabela_llm(args.juiz)
    texto = (["Embeddings (Recall@5 e MRR@5; C = A + BM25 por RRF, k = 60)"] + emb + ["", f"LLM, correção em pontos (juiz {args.juiz})"]
             + llm + ["", "Números para a leitura:"] + leitura(resumo, d, ordem))
    (comum.EXPERIENCIAS / f"tabelas_grupo_{args.juiz}.md").write_text("\n".join(texto) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(texto))


if __name__ == "__main__":
    main()
