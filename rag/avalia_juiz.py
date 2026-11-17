#!/usr/bin/env python3
"""Avalia com um juiz as respostas dos LLM (experiments/E1/modelos/llm/) e resume-as pela grelha comum.

Cada juiz guarda as avaliações à parte, em <modelo>/juiz_<juiz>.jsonl: uma linha por pergunta, com judge_model,
judge_prompt, judge_runs e judge (formato de 20/10) e os SHA-1 da resposta avaliada e da resposta de referência.
Grava a cada resposta, por isso a corrida pode parar e retomar: salta o que já foi avaliado com o mesmo juiz, o
mesmo prompt do juiz, a mesma resposta e a mesma resposta de referência. Ordem: primeiro as 20 respostas do piloto (experiments/E1/piloto/chave_piloto.json), depois as outras.
Com o Groq, ao chegar a um limite diário, para de forma limpa e diz quantas faltam.

Resumo por modelo (grelha): correção média (perguntas com resposta, e à parte as sem resposta); fidelidade média
e total de afirmações não suportadas (respostas que não se abstiveram); média das citações; abstenções certas
(perguntas sem resposta) e indevidas (as outras), com a frase fixa medida em código; % em português europeu.

Saída: os juiz_<juiz>.jsonl, config.json["judges"][<juiz>] de cada modelo e resumo_grelha_<juiz>.md.

Com --config B ou C, avalia as respostas de experiments/E1/modelos/llm_B ou llm_C (sem a ordem do piloto).

Uso, na raiz do repositório:
  .venv\\Scripts\\python rag/avalia_juiz.py --juiz gpt-oss-120b                o piloto e depois o resto
  .venv\\Scripts\\python rag/avalia_juiz.py --juiz gpt-oss-120b --espera       sem parar no limite diário
  .venv\\Scripts\\python rag/avalia_juiz.py --juiz gpt-oss-20b --config B      as respostas da B
  .venv\\Scripts\\python rag/avalia_juiz.py --juiz gpt-oss-120b --so-piloto    só as 20 do piloto
  .venv\\Scripts\\python rag/avalia_juiz.py --juiz gpt-oss-20b --so-resumo     só refaz os resumos
"""
import argparse
import hashlib
import json
import re
import statistics
import time
from datetime import date

import avalia_llm
import cliente_groq
import comum
import geracao
import juiz
import prompt_juiz

PASTA = avalia_llm.PASTA  # a pasta da configuração avaliada (muda com --config)
CHAVE_PILOTO = comum.EXPERIENCIAS / "piloto/chave_piloto.json"


def usa_config(config):
    global PASTA
    PASTA = avalia_llm.PASTAS[config]


def ficheiro(modelo, nome_juiz):
    return PASTA / modelo / f"juiz_{nome_juiz}.jsonl"


def le_avaliacoes(modelo, nome_juiz):
    caminho = ficheiro(modelo, nome_juiz)
    return {x["question_id"]: x for x in comum.le_jsonl(caminho)} if caminho.exists() else {}


def versao_prompt():
    return f"{prompt_juiz.VERSAO} ({prompt_juiz.sha1()[:12]})"


def sha1(texto):
    return hashlib.sha1(texto.encode("utf-8")).hexdigest()


def sha_referencia(pergunta):
    return sha1(pergunta.get("reference_answer") or "")


def em_dia(registo, resposta, pergunta):
    """Se a avaliação guardada foi feita com o prompt do juiz atual, sobre esta resposta e com a resposta de
    referência atual. As avaliações anteriores a 15/11 não guardam a referência e contam como feitas com a atual
    (as da E1-03, cuja referência mudou a 15/11, foram apagadas para se refazerem)."""
    return (bool(registo) and registo.get("judge_prompt") == versao_prompt() and registo.get("answer_sha1") == sha1(resposta)
            and registo.get("reference_sha1", sha_referencia(pergunta)) == sha_referencia(pergunta))


def piloto():
    return [(i["llm"], i["question_id"]) for i in json.loads(CHAVE_PILOTO.read_text(encoding="utf-8"))["items"]]


def tarefas(so_piloto, modelos):
    """(modelo, pergunta) por ordem: as do piloto primeiro (só na A, de onde o piloto foi sorteado), depois as outras."""
    primeiro = [t for t in piloto() if t[0] in modelos] if PASTA == avalia_llm.PASTAS["A"] else []
    if so_piloto:
        return primeiro
    resto = [(m, x["question_id"]) for m in modelos for x in comum.le_jsonl(PASTA / m / "results.jsonl")]
    return primeiro + [t for t in resto if t not in primeiro]


def avalia(nome_juiz, so_piloto, modelos, espera=False):
    """Avalia o que falta. Com espera=True, no limite diário do Groq espera o tempo que o Groq indica e continua,
    em vez de parar (o limite vai-se repondo aos poucos)."""
    perguntas = {p["id"]: p for p in comum.le_jsonl(comum.PERGUNTAS)}
    contextos = {c["question_id"]: c["excertos"] for c in comum.le_jsonl(PASTA / "contexto.jsonl")}
    respostas = {m: {x["question_id"]: x for x in comum.le_jsonl(PASTA / m / "results.jsonl")} for m in modelos}
    feitas = {m: le_avaliacoes(m, nome_juiz) for m in modelos}
    lista = tarefas(so_piloto, modelos)
    por_fazer = [(m, q) for m, q in lista if not em_dia(feitas[m].get(q), respostas[m][q]["answer"], perguntas[q])]
    print(f"{nome_juiz}: {len(lista) - len(por_fazer)} de {len(lista)} já avaliadas; faltam {len(por_fazer)}", flush=True)
    n = 0
    while n < len(por_fazer):
        m, q = por_fazer[n]
        try:
            corridas, agregado = juiz.avalia(nome_juiz, perguntas[q], contextos[q], respostas[m][q]["answer"])
        except cliente_groq.LimiteDiario as e:
            hoje = cliente_groq.uso_hoje()
            if espera:
                pausa = max(60.0, cliente_groq._segundos((re.search(r"try again in (\S+?)\.?\s", str(e) + " ") or [None, ""])[1]))
                print(f"  limite diário do Groq; faltam {len(por_fazer) - n}; espero {pausa:.0f} s "
                      f"({time.strftime('%H:%M')})", flush=True)
                time.sleep(pausa)
                continue
            print(f"Limite diário do Groq: {e}\nParei de forma limpa. Faltam {len(por_fazer) - n} respostas; "
                  f"hoje foram pagos {hoje['pedidos']} pedidos e {hoje['tokens']} tokens. Corre outra vez depois do reset.")
            return False
        n += 1
        feitas[m][q] = {"question_id": q, "judge_model": nome_juiz, "judge_prompt": versao_prompt(),
                        "answer_sha1": sha1(respostas[m][q]["answer"]), "reference_sha1": sha_referencia(perguntas[q]),
                        "judge_runs": corridas, "judge": agregado}
        comum.grava_jsonl(ficheiro(m, nome_juiz), [feitas[m][x] for x in respostas[m] if x in feitas[m]])
        pedidos = [c["pedidos"][k] for c in corridas for k in ("correcao", "fidelidade")]
        print(f"  {m} {q}: correção {agregado['correcao']}, fidelidade {agregado['fidelidade']}, citações {agregado['citacoes']} "
              f"({sum(x['s'] for x in pedidos):.0f} s, {sum((x.get('tokens_in') or 0) + (x.get('tokens_out') or 0) for x in pedidos)} tokens)",
              flush=True)
    return True


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.mean(xs), 3) if xs else None


def resume_grelha(linhas, avaliacoes):
    j = {q: a["judge"] for q, a in avaliacoes.items()}
    com = [x for x in linhas if x["type"] != "unanswerable"]
    sem = [x for x in linhas if x["type"] == "unanswerable"]
    respostas = [x for x in linhas if not x["abstained"]]
    return {"correcao_media": media(j[x["question_id"]]["correcao"] for x in com),
            "correcao_media_sem_resposta": media(j[x["question_id"]]["correcao"] for x in sem),
            "fidelidade_media": media(j[x["question_id"]]["fidelidade"] for x in respostas),
            "nao_suportadas_total": sum(j[x["question_id"]]["nao_suportadas"] or 0 for x in respostas),
            "citacoes_media": media(j[x["question_id"]]["citacoes"] for x in respostas),
            "abstencoes_certas": f"{sum(x['abstained'] for x in sem)}/{len(sem)}",
            "abstencoes_indevidas": f"{sum(x['abstained'] for x in com)}/{len(com)}",
            "indevidas_com_resposta_nos_excertos": sum(bool(x["abstained"] and j[x["question_id"]]["abstencao_com_resposta_nos_excertos"])
                                                       for x in com),
            "portugues_europeu_pct": round(100 * statistics.mean(bool(j[x["question_id"]]["portugues_europeu"]) for x in linhas))}


def atualiza_config(modelo, nome_juiz):
    """Grava o resumo do juiz no config.json do modelo, se as 15 respostas já estiverem avaliadas."""
    linhas, avaliacoes = comum.le_jsonl(PASTA / modelo / "results.jsonl"), le_avaliacoes(modelo, nome_juiz)
    if any(x["question_id"] not in avaliacoes for x in linhas):
        return False
    pedidos = [c["pedidos"][k] for a in avaliacoes.values() for c in a["judge_runs"] for k in ("correcao", "fidelidade")]
    caminho = PASTA / modelo / "config.json"
    cfg = json.loads(caminho.read_text(encoding="utf-8"))
    cfg.setdefault("judges", {})[nome_juiz] = {
        **juiz.parametros(nome_juiz), "prompt_version": prompt_juiz.VERSAO, "prompt_sha1": prompt_juiz.sha1(),
        "file": ficheiro(modelo, nome_juiz).relative_to(comum.RAIZ).as_posix(), "date": date.today().isoformat(),
        "answers_with_retry": sum(any(c["pedidos"][k]["tentativas"] > 1 for c in a["judge_runs"] for k in ("correcao", "fidelidade"))
                                  for a in avaliacoes.values()),
        "tokens": {"in": sum(x.get("tokens_in") or 0 for x in pedidos), "out": sum(x.get("tokens_out") or 0 for x in pedidos),
                   "reasoning": sum(x.get("tokens_raciocinio") or 0 for x in pedidos)},
        "grid_summary": resume_grelha(linhas, avaliacoes)}
    caminho.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return True


def escreve_resumo(nome_juiz):
    num = lambda x, c=2: "—" if x is None else f"{x:.{c}f}".replace(".", ",")
    cfgs = [json.loads((PASTA / m / "config.json").read_text(encoding="utf-8")) for m in geracao.LLMS]
    completos = [c for c in cfgs if nome_juiz in c.get("judges", {})]
    if not completos:
        return
    j = completos[0]["judges"][nome_juiz]
    repetidas = sum(c["judges"][nome_juiz]["answers_with_retry"] for c in completos)
    em_falta = [c["llm"]["name"] for c in cfgs if c not in completos]
    md = [f"# Teste dos LLM (E1) pela grelha comum, com o juiz {nome_juiz}", "",
          f"{date.today():%d/%m/%Y}. As 15 perguntas com os mesmos 5 excertos ({completos[0]['context']['embedding_experiment']}), "
          f"prompt de geração {completos[0]['prompt']['version']}. Juiz `{j['modelo']}` ({j['fornecedor']}, raciocínio «{j['raciocinio']}», "
          f"temperatura {j['temperature']}, {j['runs']} corrida), prompt do juiz {j['prompt_version']}. Em {repetidas} das "
          f"{15 * len(completos)} respostas, o 1.º pedido não deu JSON válido e repetiu-se com temperatura "
          f"{str(j['retry_temperature']).replace('.', ',')}." + (f" Ainda por avaliar: {', '.join(em_falta)}." if em_falta else ""), "",
          "| LLM | Correção (com resposta, 0–2) | Correção (sem resposta, 0–2) | Fidelidade (0–1) | Afirmações não suportadas "
          "| Citações (0–2) | Abstenções certas | Abstenções indevidas | Português europeu | Latência média (s) | Tokens/s |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in completos:
        g, s = c["judges"][nome_juiz]["grid_summary"], c["summary"]
        md.append(f"| {c['llm']['name']} | {num(g['correcao_media'])} | {num(g['correcao_media_sem_resposta'])} "
                  f"| {num(g['fidelidade_media'])} | {num(g['nao_suportadas_total'], 0)} | {num(g['citacoes_media'])} "
                  f"| {g['abstencoes_certas']} | {g['abstencoes_indevidas']} | {g['portugues_europeu_pct']}% "
                  f"| {num(s['latencia_media_s'], 1)} | {num(s['tokens_por_s_media'], 0)} |")
    md += ["", "Correção: média das 12 perguntas com resposta; nas 3 sem resposta, 2 se diz que a informação não está nas "
               "fontes. Fidelidade, afirmações não suportadas e citações: nas respostas que não se abstêm (frase fixa, "
               "medida em código). Abstenções indevidas: nas perguntas com resposta, incluindo aquelas em que a pesquisa "
               "não trouxe o trecho certo."]
    (PASTA / f"resumo_grelha_{nome_juiz}.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description="Avalia as respostas dos LLM do E1 com um juiz da grelha comum.")
    ap.add_argument("--juiz", choices=list(juiz.JUIZES), required=True)
    ap.add_argument("--modelo", choices=list(geracao.LLMS), action="append", help="por omissão, todos")
    ap.add_argument("--so-piloto", action="store_true", help="só as 20 respostas do piloto")
    ap.add_argument("--so-resumo", action="store_true", help="não chama o juiz: só refaz os resumos")
    ap.add_argument("--config", choices=list(avalia_llm.PASTAS), default="A", help="respostas da A (por omissão), da B ou da C")
    ap.add_argument("--espera", action="store_true", help="no limite diário do Groq, espera e continua em vez de parar")
    args = ap.parse_args()
    comum.prepara_consola()
    usa_config(args.config)
    modelos = args.modelo or list(geracao.LLMS)
    if not args.so_resumo:
        avalia(args.juiz, args.so_piloto, modelos, args.espera)
    completos = [m for m in modelos if atualiza_config(m, args.juiz)]
    escreve_resumo(args.juiz)
    if juiz.JUIZES[args.juiz]["fornecedor"] == "groq":
        hoje = cliente_groq.uso_hoje()
        print(f"Groq hoje: {hoje['pedidos']} pedidos e {hoje['tokens']} tokens pagos "
              f"(limites: {cliente_groq.LIMITES['pedidos_dia']} pedidos e {cliente_groq.LIMITES['tokens_dia']} tokens por dia)")
    print(f"Modelos com as 15 avaliadas: {', '.join(completos) or 'nenhum'}; tabela em "
          f"{(PASTA / f'resumo_grelha_{args.juiz}.md').relative_to(comum.RAIZ)}")


if __name__ == "__main__":
    main()
