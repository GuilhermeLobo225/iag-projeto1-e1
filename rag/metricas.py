#!/usr/bin/env python3
"""Métricas de recuperação combinadas no grupo (decisões de 20/10, ponto 6).

Acerto: o excerto [cs, ce) acerta no trecho [es, ee) se forem do mesmo documento e
  max(0, min(ce, ee) − max(cs, es)) ≥ 0,5 × min(ce − cs, ee − es)   (50% do mais curto)

Por pergunta, com os 5 primeiros excertos:
  recall_at_5      fração dos grupos de trechos cobertos por algum excerto. Os trechos com o mesmo
                   "group" são alternativos e contam uma vez; um trecho sem group é um grupo sozinho.
  rr               1 / posição do primeiro excerto que acerta em algum trecho; 0 se nenhum acertar.
  cobertura_total  1 se todos os grupos ficarem cobertos (reporta-se nas multi_doc).
As perguntas sem resposta (unanswerable) não entram no Recall@5 nem no MRR@5.

Regra do E2 (8/11), só para comparar números entre áreas, sem mudar a nossa: acerta com pelo menos 1 carácter de
sobreposição no mesmo documento, e o RR conta até ao 10.º excerto (MRR@10). O Recall@5 continua nos 5 primeiros.

Uso, na raiz do repositório:
  .venv\\Scripts\\python rag/metricas.py teto experiments/E1/excertos_B.jsonl
      melhor resultado possível com estes excertos, se a pesquisa escolhesse sempre os excertos certos,
      e os trechos em que nenhum excerto acerta (por ficarem partidos entre dois excertos)
Os 4 casos de teste das decisões de 20/10 estão em tests/test_metricas.py (.venv\\Scripts\\python -m pytest).
"""
import argparse
import statistics

import comum

K = 5
K_MRR = {"E1": 5, "E2": 10}


def sobreposicao(a, b):
    return max(0, min(a["end"], b["end"]) - max(a["start"], b["start"]))


def acerta(excerto, trecho, regra="E1"):
    if excerto["doc_id"] != trecho["doc_id"]:
        return False
    if regra == "E2":
        return sobreposicao(excerto, trecho) >= 1
    menor = min(excerto["end"] - excerto["start"], trecho["end"] - trecho["start"])
    return sobreposicao(excerto, trecho) >= 0.5 * menor


def grupos(evidence):
    """Lista de grupos; cada grupo é a lista dos trechos alternativos."""
    if evidence and all("group" in e for e in evidence):
        por_numero = {}
        for e in evidence:
            por_numero.setdefault(e["group"], []).append(e)
        return list(por_numero.values())
    return [[e] for e in evidence]


def avalia(evidence, recuperados, k=K, regra="E1"):
    """Métricas de uma pergunta. `recuperados` vem por ordem, cada um com doc_id, start e end.
    Com regra="E2", o rr conta até ao 10.º excerto (é o MRR@10) e os hit_ranks também."""
    if not evidence:  # sem resposta: fora do Recall@5 e do MRR@5
        return {"hit_ranks": [], "recall_at_5": None, "rr": None, "cobertura_total": None}
    topo = recuperados[:k]
    hit_ranks = [r for r, c in enumerate(recuperados[:K_MRR[regra]], start=1) if any(acerta(c, e, regra) for e in evidence)]
    gs = grupos(evidence)
    cobertos = sum(1 for g in gs if any(acerta(c, e, regra) for c in topo for e in g))
    return {"hit_ranks": hit_ranks, "recall_at_5": cobertos / len(gs), "rr": 1 / hit_ranks[0] if hit_ranks else 0.0,
            "cobertura_total": int(cobertos == len(gs))}


def resumo(resultados):
    """Médias das perguntas com resposta. Cada resultado tem "type" e as chaves de avalia()."""
    com = [r for r in resultados if r["recall_at_5"] is not None]
    out = {"perguntas": len(com), "recall_at_5": statistics.mean(r["recall_at_5"] for r in com),
           "mrr_at_5": statistics.mean(r["rr"] for r in com)}
    for tipo in sorted({r["type"] for r in com}):
        rs = [r for r in com if r["type"] == tipo]
        out[f"recall_at_5_{tipo}"] = statistics.mean(r["recall_at_5"] for r in rs)
        out[f"mrr_at_5_{tipo}"] = statistics.mean(r["rr"] for r in rs)
    multi = [r for r in com if r["type"] == "multi_doc"]
    if multi:
        out["cobertura_total_multi_doc"] = statistics.mean(r["cobertura_total"] for r in multi)
    return out


def teto(caminho_excertos, caminho_perguntas=comum.PERGUNTAS):
    """Recall@5 máximo: para cada grupo, há algum excerto que acerte? Mostra os trechos sem nenhum."""
    excertos = comum.le_jsonl(caminho_excertos)
    por_doc = {}
    for x in excertos:
        por_doc.setdefault(x["doc_id"], []).append(x)
    resultados, falhas = [], []
    for p in comum.le_jsonl(caminho_perguntas):
        if not p["evidence"]:
            continue
        gs = grupos(p["evidence"])
        cobertos = 0
        for g in gs:
            if any(acerta(x, e) for e in g for x in por_doc.get(e["doc_id"], [])):
                cobertos += 1
                continue
            for e in g:
                melhor = max((sobreposicao(x, e) for x in por_doc.get(e["doc_id"], [])), default=0)
                falhas.append(f"{p['id']}: {e['doc_id']} [{e['start']}, {e['end']}) ({e['end'] - e['start']} caracteres); "
                              f"o melhor excerto só tem {melhor} ({melhor / (e['end'] - e['start']):.0%} do trecho)")
        # Com 5 posições chegam para todos os grupos (no máximo 3), o melhor caso cobre todos os que têm acerto.
        resultados.append({"type": p["type"], "recall_at_5": cobertos / len(gs), "rr": 1.0 if cobertos else 0.0,
                           "cobertura_total": int(cobertos == len(gs))})
    return resumo(resultados), falhas


def main():
    ap = argparse.ArgumentParser(description="Métricas de recuperação do E1.")
    ap.add_argument("acao", choices=["teto"])
    ap.add_argument("excertos", nargs="+", help="ficheiros excertos_*.jsonl")
    args = ap.parse_args()
    comum.prepara_consola()
    for caminho in args.excertos:
        r, falhas = teto(caminho)
        print(f"{caminho}: teto com {r['perguntas']} perguntas: Recall@5 {r['recall_at_5']:.3f}, MRR@5 {r['mrr_at_5']:.3f}, "
              f"cobertura total das multi_doc {r['cobertura_total_multi_doc']:.2f}")
        for f in falhas:
            print("  sem acerto possível:", f)


if __name__ == "__main__":
    main()
