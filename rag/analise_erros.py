#!/usr/bin/env python3
"""Análise de erros do E1: por pergunta e por experiência, junta o que é preciso para perceber cada falha.

Para cada pergunta e experiência (experiments/E1/A, B e C): os 5 excertos recuperados (documento, pontuação e se
acertam num trecho), os trechos certos que só aparecem entre o 6.º e o 10.º lugar (quase-acertos), a resposta, as
notas do juiz (se já houver) e os problemas detetados em código:
  pesquisa: sem acerto nos 5 primeiros, ou só parte dos trechos (multi_doc), ou quase-acerto;
  geração: abstenção numa pergunta com resposta (com ou sem o trecho nos excertos), resposta a uma pergunta sem
  resposta, sem citações, citações fora dos excertos ou mal escritas, resposta cortada;
  juiz: correção abaixo de 2, afirmações não suportadas, citações abaixo de 2, abstenção com a resposta nos
  excertos, sem português europeu.
As notas sobre as respostas de referência (E1-03, E1-05 e E1-10) estão em NOTAS_REFERENCIA.
Saída: experiments/E1/analise_erros.md (uma secção por pergunta) e analise_erros.csv (uma linha por pergunta e
experiência, para contar os problemas por tipo).

Uso, na raiz do repositório:
  .venv\\Scripts\\python rag/analise_erros.py
  .venv\\Scripts\\python rag/analise_erros.py --experiencias A C
"""
import argparse
import csv
import json
from collections import Counter

import comum
import metricas
import pesquisa

PASTA = comum.EXPERIENCIAS

# Notas sobre as respostas de referência, decididas pelo Lobo; entram na secção de cada pergunta.
NOTAS_REFERENCIA = {
    "E1-03": "A referência foi completada a 15/11. O regulamento municipal (E1-004, art. 38.º) também manda levar os "
             "volumosos aos ecocentros, e antes as respostas que iam por aí levavam 0 por «contradizerem» a referência "
             "(como na E2-02). Ficou «Há duas formas, e qualquer uma basta: contactar a Vitrus Ambiente para agendar a "
             "recolha, que é gratuita, ou levá-lo a um ecocentro», sem dizer de que entidade, para valer tanto para os "
             "ecocentros de Aldão e Ponte (E1-001) como para os da Resinorte (E1-004). Os trechos continuam os do E1-014. "
             "Mesmo assim, os dois juízes leem as duas formas como obrigatórias: com o 120b, a resposta só com a Vitrus "
             "e a recolha gratuita (B) desce de 2 para 1, por omitir a alternativa do ecocentro. "
             "As notas antes e depois estão no docs/pipeline_E1_15-11.md.",
    "E1-05": "Decisão de 8/11: o PAPERSU (E1-001) descreve um reembolso de 50% da tarifa variável, mas em dezembro de 2024 "
             "e com outras condições. Não entra como trecho alternativo: é informação parecida noutro documento.",
    "E1-10": "A referência fica como está (decisão de 15/11), mas inclui os 120 dias de transição, que a pergunta não pede. "
             "Isso tira 1 ponto, por igual, a quase todas as respostas que não se abstêm. Com o juiz 120b, nenhuma das "
             "respostas à E1-10 tem 2, e só uma em 10 refere os 120 dias (o AMALIA no teste na A).",
}


def problemas(x, juiz):
    """Códigos curtos dos problemas de uma resposta (x: linha do results.jsonl; juiz: o agregado ou None)."""
    p, com_resposta = [], x["type"] != "unanswerable"
    if com_resposta:
        if x["recall_at_5"] == 0:
            p.append("pesquisa_sem_acerto")
        elif x["recall_at_5"] < 1:
            p.append("pesquisa_parcial")
    if "answer" in x:
        if com_resposta and x["abstained"]:
            p.append("abstencao_com_trecho_nos_excertos" if x["recall_at_5"] > 0 else "abstencao_sem_trecho_nos_excertos")
        if not com_resposta and not x["abstained"]:
            p.append("respondeu_sem_resposta_na_base")
        if not x["abstained"] and not x["cited_doc_ids"]:
            p.append("sem_citacoes")
        if x["citations_outside_context"]:
            p.append("citacoes_fora_dos_excertos")
        if x["malformed_citations"]:
            p.append("citacoes_mal_escritas")
        if x["done_reason"] == "length":
            p.append("resposta_cortada")
    if juiz:
        if juiz["correcao"] is not None and juiz["correcao"] < 2:
            p.append(f"correcao_{juiz['correcao']:g}")
        if juiz["nao_suportadas"]:
            p.append("afirmacoes_nao_suportadas")
        if juiz["citacoes"] is not None and juiz["citacoes"] < 2:
            p.append(f"citacoes_{juiz['citacoes']:g}")
        if juiz["abstencao_com_resposta_nos_excertos"]:
            p.append("juiz_abstencao_com_resposta_nos_excertos")
        if juiz["portugues_europeu"] is False:
            p.append("sem_portugues_europeu")
    return p


def main():
    ap = argparse.ArgumentParser(description="Junta, por pergunta e experiência, o necessário para a análise de erros.")
    ap.add_argument("--experiencias", nargs="+", default=["A", "B", "C"])
    args = ap.parse_args()
    comum.prepara_consola()
    perguntas = comum.le_jsonl(comum.PERGUNTAS)
    exps = {}
    for n in args.experiencias:
        if not (PASTA / n / "results.jsonl").exists():
            continue
        cfg = json.loads((PASTA / n / "config.json").read_text(encoding="utf-8"))
        juiz_f = PASTA / n / f"juiz_{cfg['judge']}.jsonl"
        exps[n] = {"cfg": cfg, "linhas": {x["question_id"]: x for x in comum.le_jsonl(PASTA / n / "results.jsonl")},
                   "juiz": {x["question_id"]: x for x in comum.le_jsonl(juiz_f)} if juiz_f.exists() else {}}
    md = ["# Análise de erros (E1)", "",
          "Por pergunta e experiência: os 5 excertos recuperados (✔ = acerta num trecho, pela regra do E1), os quase-acertos "
          "(trecho certo entre o 6.º e o 10.º), a resposta, os problemas detetados em código e as notas do juiz, se houver.", ""]
    tabela, contagem = [], Counter()
    for p in perguntas:
        md += [f"## {p['id']} ({p['type']}): {p['question']}", "", f"**Referência:** {p['reference_answer']}", ""]
        if p["id"] in NOTAS_REFERENCIA:
            md += [f"**Nota sobre a referência:** {NOTAS_REFERENCIA[p['id']]}", ""]
        for e in p["evidence"]:
            md.append(f"- Trecho {e['doc_id']} [{e['start']}, {e['end']})" + (f", grupo {e['group']}" if "group" in e else "")
                      + f": «{e['text'][:220]}{'…' if len(e['text']) > 220 else ''}»")
        for n, d in exps.items():
            x, chunks = d["linhas"][p["id"]], d["linhas"][p["id"]]["chunks"]
            por_id = {c["chunk_id"]: c for c in pesquisa.excertos(chunks)}
            a = d["juiz"].get(p["id"])
            j = a["judge"] if a else None
            prob = problemas(x, j)
            contagem.update(f"{n}:{c}" for c in prob)
            md += ["", f"### {n} ({d['cfg']['run']['retrieval']['mode']}, excertos {chunks}): Recall@5 "
                       f"{'—' if x['recall_at_5'] is None else round(x['recall_at_5'], 2)}, RR "
                       f"{'—' if x['rr'] is None else round(x['rr'], 2)}", "",
                   "| # | Excerto | Pontuação | Acerta | Início do texto |", "|---|---|---|---|---|"]
            for c in x["retrieved"][:5]:
                ok = "✔" if any(metricas.acerta(c, e) for e in p["evidence"]) else ""
                inicio = por_id[c["chunk_id"]]["text"][:140].replace("\n", " ").replace("|", "\\|")
                md.append(f"| {c['rank']} | {c['chunk_id']} | {c['score']} | {ok} | {inicio}… |")
            quase = [c for c in x["retrieved"][5:10] if any(metricas.acerta(c, e) for e in p["evidence"])]
            if quase:
                md.append("\nQuase-acertos: " + ", ".join(f"{c['chunk_id']} em {c['rank']}.º" for c in quase))
            if "answer" in x:
                md += ["", f"**Resposta** ({x['llm_model_returned']}, {x['latency_s']} s): {x['answer'].strip()}"]
            md += ["", f"**Problemas em código:** {', '.join(prob) or 'nenhum'}"]
            if a:
                r0 = a["judge_runs"][0]
                md += [f"**Juiz** ({a['judge_model']}): correção {j['correcao']} ({r0['justificacao_correcao']}); fidelidade "
                       f"{j['fidelidade']}; citações {j['citacoes']} ({r0['justificacao_citacoes']})"]
                for af in r0["afirmacoes"]:
                    if not af["suportada"]:
                        md.append(f"- não suportada: {af['afirmacao']}")
            tabela.append({"question_id": p["id"], "type": p["type"], "experiment": n, "recall_at_5": x["recall_at_5"], "rr": x["rr"],
                           "abstained": x.get("abstained"), "cited_doc_ids": " ".join(x.get("cited_doc_ids", [])),
                           "correcao": j["correcao"] if j else None, "fidelidade": j["fidelidade"] if j else None,
                           "citacoes": j["citacoes"] if j else None, "problemas": "; ".join(prob)})
        md.append("")
    md += ["## Contagem dos problemas", "", "| Experiência | Problema | Respostas |", "|---|---|---|"]
    for k, v in sorted(contagem.items()):
        n, c = k.split(":", 1)
        md.append(f"| {n} | {c} | {v} |")
    (PASTA / "analise_erros.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    with open(PASTA / "analise_erros.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(tabela[0]), delimiter=";")
        w.writeheader()
        w.writerows(tabela)
    print(f"analise_erros.md e analise_erros.csv em {PASTA.relative_to(comum.RAIZ)}: {len(tabela)} linhas; "
          f"problemas mais frequentes: {', '.join(f'{k} ({v})' for k, v in contagem.most_common(6))}")


if __name__ == "__main__":
    main()
