#!/usr/bin/env python3
"""Piloto do juiz (grelha comum, ponto 5): folha às cegas para a avaliação humana e a concordância com o juiz.

cria     sorteia 20 das 60 respostas (semente fixa; 5 por LLM e pelo menos 3 de perguntas sem resposta) e grava em
         experiments/E1/piloto/ a folha_piloto.csv, que cada avaliador preenche sem saber o modelo, e a
         chave_piloto.json, que liga cada item à resposta (não abrir antes de avaliar).
compara  compara as folhas preenchidas com o juiz (e os avaliadores entre si) e grava concordancia.md.
         Pela grelha, ganha o juiz com mais notas iguais às humanas na correção e nas citações e com a menor
         diferença na fidelidade.

A folha abre no Excel (UTF-8, separador ;). Colunas a preencher, como na grelha:
  nota_correcao              0, 1 ou 2 (nas perguntas sem resposta, 0 ou 2)
  afirmacoes_total           quantas afirmações factuais tem a resposta
  afirmacoes_suportadas      quantas delas algum excerto suporta (a fidelidade é a divisão das duas)
  nota_citacoes              0, 1 ou 2; vazio se a resposta não tiver afirmações
  abstencao                  sim ou não: a resposta diz que não tem informação?
  excertos_tinham_resposta   sim ou não, só se abstencao = sim
  portugues_europeu          sim ou não

Uso, na raiz do repositório:
  .venv\\Scripts\\python rag/piloto.py cria
  .venv\\Scripts\\python rag/piloto.py compara experiments/E1/piloto/folha_lobo.csv experiments/E1/piloto/folha_X.csv
"""
import argparse
import csv
import json
import random
import statistics
from datetime import date
from pathlib import Path

import comum
import geracao
import prompt_geracao

PASTA = comum.EXPERIENCIAS / "piloto"
LLM = comum.EXPERIENCIAS / "modelos/llm"
SEMENTE = 42
POR_LLM, MIN_SEM_RESPOSTA = 5, 3
PREENCHER = ["nota_correcao", "afirmacoes_total", "afirmacoes_suportadas", "nota_citacoes", "abstencao",
             "excertos_tinham_resposta", "portugues_europeu", "observacoes"]


def sorteia(perguntas):
    rng = random.Random(SEMENTE)
    ids = sorted(perguntas)
    while True:  # repete o sorteio (com a mesma sequência aleatória) até ter as perguntas sem resposta pedidas
        itens = [(m, q) for m in geracao.LLMS for q in rng.sample(ids, POR_LLM)]
        if sum(perguntas[q]["type"] == "unanswerable" for _, q in itens) >= MIN_SEM_RESPOSTA:
            rng.shuffle(itens)
            return itens


def cria():
    perguntas = {p["id"]: p for p in comum.le_jsonl(comum.PERGUNTAS)}
    contextos = {c["question_id"]: c["excertos"] for c in comum.le_jsonl(LLM / "contexto.jsonl")}
    respostas = {(m, r["question_id"]): r for m in geracao.LLMS for r in comum.le_jsonl(LLM / m / "results.jsonl")}
    itens = sorteia(perguntas)
    PASTA.mkdir(parents=True, exist_ok=True)
    with open(PASTA / "folha_piloto.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["item", "pergunta", "resposta_de_referencia", "excertos", "resposta_do_sistema",
                    "ids_escritos_na_resposta"] + PREENCHER)
        for n, (m, q) in enumerate(itens, start=1):
            r = respostas[(m, q)]
            w.writerow([f"P{n:02d}", perguntas[q]["question"], perguntas[q]["reference_answer"],
                        prompt_geracao.contexto(contextos[q]), r["answer"].strip(), ", ".join(r["cited_doc_ids"]) or "nenhum"]
                       + [""] * len(PREENCHER))
    chave = {"seed": SEMENTE, "date": date.today().isoformat(),
             "items": [{"item": f"P{n:02d}", "llm": m, "question_id": q, "type": perguntas[q]["type"]}
                       for n, (m, q) in enumerate(itens, start=1)]}
    (PASTA / "chave_piloto.json").write_text(json.dumps(chave, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    sem = sum(i["type"] == "unanswerable" for i in chave["items"])
    print(f"folha_piloto.csv: {len(itens)} respostas ({POR_LLM} por LLM, {sem} de perguntas sem resposta)")


def sim_nao(v):
    v = (v or "").strip().lower()
    return True if v in ("sim", "s", "1", "true") else False if v in ("não", "nao", "n", "0", "false") else None


def inteiro(v):
    v = (v or "").strip()
    return int(v) if v.lstrip("-").isdigit() else None


def le_folha(caminho):
    """Notas de um avaliador por item, no mesmo formato do agregado do juiz."""
    notas = {}
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        for linha in csv.DictReader(f, delimiter=";"):
            total, sup = inteiro(linha["afirmacoes_total"]), inteiro(linha["afirmacoes_suportadas"])
            notas[linha["item"]] = {"correcao": inteiro(linha["nota_correcao"]),
                                    "fidelidade": round(sup / total, 3) if total and sup is not None else None,
                                    "citacoes": inteiro(linha["nota_citacoes"]),
                                    "abstencao": sim_nao(linha["abstencao"]),
                                    "portugues_europeu": sim_nao(linha["portugues_europeu"])}
    return notas


def concordancia(a, b, itens):
    """Notas iguais (correção, citações, português) e diferença média da fidelidade entre duas fontes de notas."""
    def iguais(k):
        pares = [(a[i][k], b[i][k]) for i in itens if a[i][k] is not None and b[i][k] is not None]
        return f"{sum(x == y for x, y in pares)}/{len(pares)}"
    difs = [abs(a[i]["fidelidade"] - b[i]["fidelidade"]) for i in itens
            if a[i]["fidelidade"] is not None and b[i]["fidelidade"] is not None]
    return {"correcao_iguais": iguais("correcao"), "citacoes_iguais": iguais("citacoes"),
            "fidelidade_diferenca_media": round(statistics.mean(difs), 3) if difs else None,
            "portugues_iguais": iguais("portugues_europeu")}


def compara(folhas):
    chave = json.loads((PASTA / "chave_piloto.json").read_text(encoding="utf-8"))
    respostas = {(m, r["question_id"]): r for m in geracao.LLMS for r in comum.le_jsonl(LLM / m / "results.jsonl")}
    juiz = {i["item"]: respostas[(i["llm"], i["question_id"])]["judge"] for i in chave["items"]}
    nome_juiz = respostas[(chave["items"][0]["llm"], chave["items"][0]["question_id"])]["judge_model"]
    humanos = {Path(f).stem: le_folha(f) for f in folhas}
    itens = [i["item"] for i in chave["items"]]
    linhas = [(f"{nome_juiz} contra {h}", concordancia(juiz, n, itens)) for h, n in humanos.items()]
    nomes = list(humanos)
    for i, h1 in enumerate(nomes):
        for h2 in nomes[i + 1:]:
            linhas.append((f"{h1} contra {h2}", concordancia(humanos[h1], humanos[h2], itens)))
    md = ["# Piloto do juiz (E1): concordância com as avaliações humanas", "",
          f"{date.today():%d/%m/%Y}. {len(itens)} respostas sorteadas com a semente {chave['seed']}, avaliadas às cegas.", "",
          "| Comparação | Correção igual | Citações iguais | Diferença média na fidelidade | Português europeu igual |",
          "|---|---|---|---|---|"]
    for nome, c in linhas:
        dif = "—" if c["fidelidade_diferenca_media"] is None else f"{c['fidelidade_diferenca_media']:.3f}".replace(".", ",")
        md.append(f"| {nome} | {c['correcao_iguais']} | {c['citacoes_iguais']} | {dif} | {c['portugues_iguais']} |")
    (PASTA / "concordancia.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(md))


def main():
    ap = argparse.ArgumentParser(description="Piloto do juiz do E1.")
    ap.add_argument("acao", choices=["cria", "compara"])
    ap.add_argument("folhas", nargs="*", help="no compara, as folhas preenchidas")
    args = ap.parse_args()
    comum.prepara_consola()
    cria() if args.acao == "cria" else compara(args.folhas)


if __name__ == "__main__":
    main()
