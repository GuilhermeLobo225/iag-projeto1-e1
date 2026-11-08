#!/usr/bin/env python3
"""Avalia com o juiz as respostas dos LLM e resume-as pela grelha comum.

Lê experiments/E1/modelos/llm/<modelo>/results.jsonl e acrescenta a cada linha judge_model, judge_prompt,
judge_runs e judge (formato combinado a 20/10). Grava depois de cada resposta, por isso pode ser interrompido e
retomado: salta as linhas já avaliadas com o mesmo juiz e a mesma versão do prompt do juiz.

Resumo por modelo (grelha): correção média (perguntas com resposta, e à parte as sem resposta); fidelidade média
e total de afirmações não suportadas (respostas que não se abstiveram); média das citações; abstenções certas
(perguntas sem resposta) e indevidas (as outras), com a frase fixa medida em código; % em português europeu.

Saída: os results.jsonl, as secções "judge" e "grid_summary" de cada config.json, e resumo_grelha.md.

Uso, na raiz do repositório (com o Ollama a correr):
  .venv\\Scripts\\python rag/avalia_juiz.py                                         as 60 respostas
  .venv\\Scripts\\python rag/avalia_juiz.py --modelo amalia-9b --perguntas E1-15    só algumas
  .venv\\Scripts\\python rag/avalia_juiz.py --so-resumo                             só refaz os resumos
"""
import argparse
import json
import statistics
from datetime import date

import avalia_llm
import comum
import geracao
import juiz
import prompt_juiz

PASTA = avalia_llm.PASTA


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.mean(xs), 3) if xs else None


def resume_grelha(linhas):
    com = [x for x in linhas if x["type"] != "unanswerable"]
    sem = [x for x in linhas if x["type"] == "unanswerable"]
    respostas = [x for x in linhas if not x["abstained"]]
    return {"correcao_media": media(x["judge"]["correcao"] for x in com),
            "correcao_media_sem_resposta": media(x["judge"]["correcao"] for x in sem),
            "fidelidade_media": media(x["judge"]["fidelidade"] for x in respostas),
            "nao_suportadas_total": sum(x["judge"]["nao_suportadas"] or 0 for x in respostas),
            "citacoes_media": media(x["judge"]["citacoes"] for x in respostas),
            "abstencoes_certas": f"{sum(x['abstained'] for x in sem)}/{len(sem)}",
            "abstencoes_indevidas": f"{sum(x['abstained'] for x in com)}/{len(com)}",
            "indevidas_com_resposta_nos_excertos": sum(bool(x["abstained"] and x["judge"]["abstencao_com_resposta_nos_excertos"])
                                                       for x in com),
            "portugues_europeu_pct": round(100 * statistics.mean(bool(x["judge"]["portugues_europeu"]) for x in linhas))}


def avalia_modelo(modelo, nome_juiz, so=None):
    caminho = PASTA / modelo / "results.jsonl"
    linhas = comum.le_jsonl(caminho)
    perguntas = {p["id"]: p for p in comum.le_jsonl(comum.PERGUNTAS)}
    contextos = {c["question_id"]: c["excertos"] for c in comum.le_jsonl(PASTA / "contexto.jsonl")}
    marca = {"judge_model": nome_juiz, "judge_prompt": f"{prompt_juiz.VERSAO} ({prompt_juiz.sha1()[:12]})"}
    for x in linhas:
        if (so and x["question_id"] not in so) or (x.get("judge_model"), x.get("judge_prompt")) == tuple(marca.values()):
            continue
        corridas, agregado = juiz.avalia(nome_juiz, perguntas[x["question_id"]], contextos[x["question_id"]], x["answer"])
        x.update(marca | {"judge_runs": corridas, "judge": agregado})
        comum.grava_jsonl(caminho, linhas)  # grava já, para se poder retomar
        tempo = sum(c["pedidos"]["correcao"]["s"] + c["pedidos"]["fidelidade"]["s"] for c in corridas)
        print(f"  {modelo} {x['question_id']}: correção {agregado['correcao']}, fidelidade {agregado['fidelidade']}, "
              f"citações {agregado['citacoes']}, PT-PT {agregado['portugues_europeu']} ({tempo:.0f} s)", flush=True)
    return linhas


def atualiza_config(modelo, linhas, nome_juiz):
    caminho = PASTA / modelo / "config.json"
    cfg = json.loads(caminho.read_text(encoding="utf-8"))
    if all("judge" in x for x in linhas):
        cfg["judge"] = {"name": nome_juiz, "ollama_model": juiz.JUIZES[nome_juiz]["ollama"], "think": juiz.JUIZES[nome_juiz]["think"],
                        "options": juiz.OPCOES, "runs": juiz.CORRIDAS, "aggregation": "mediana das notas, maioria nos sim/não",
                        "retries": juiz.TENTATIVAS - 1, "retry_temperature": juiz.TEMPERATURA_REPETICAO,
                        "answers_with_retry": sum(any(c["pedidos"][k]["tentativas"] > 1 for c in x["judge_runs"]
                                                      for k in ("correcao", "fidelidade")) for x in linhas),
                        "prompt_version": prompt_juiz.VERSAO, "prompt_sha1": prompt_juiz.sha1(), "date": date.today().isoformat()}
        cfg["grid_summary"] = resume_grelha(linhas)
        caminho.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return cfg


def escreve_resumo():
    num = lambda x, c=2: "—" if x is None else f"{x:.{c}f}".replace(".", ",")
    cfgs = [json.loads((PASTA / m / "config.json").read_text(encoding="utf-8")) for m in geracao.LLMS]
    cfgs = [c for c in cfgs if "grid_summary" in c]
    if not cfgs:
        return
    j = cfgs[0]["judge"]
    corridas = "1 corrida" if j["runs"] == 1 else f"{j['runs']} corridas, mediana"
    repetidas = sum(c["judge"]["answers_with_retry"] for c in cfgs)
    md = ["# Teste dos LLM (E1) pela grelha comum", "",
          f"{date.today():%d/%m/%Y}. As 15 perguntas com os mesmos 5 excertos ({cfgs[0]['context']['embedding_experiment']}), "
          f"prompt de geração {cfgs[0]['prompt']['version']}. Juiz {j['ollama_model']} (raciocínio «{j['think']}», temperatura 0, "
          f"{corridas}), prompt do juiz {j['prompt_version']}; em {repetidas} das {15 * len(cfgs)} respostas, o 1.º pedido não deu "
          f"JSON válido (por um ciclo no raciocínio) e repetiu-se com temperatura {str(j['retry_temperature']).replace('.', ',')}. "
          "**Provisório**: o juiz local só vale se passar no piloto com as avaliações humanas.", "",
          "| LLM | Correção (com resposta, 0–2) | Correção (sem resposta, 0–2) | Fidelidade (0–1) | Afirmações não suportadas "
          "| Citações (0–2) | Abstenções certas | Abstenções indevidas | Português europeu | Latência média (s) | Tokens/s |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in cfgs:
        g, s = c["grid_summary"], c["summary"]
        md.append(f"| {c['llm']['name']} | {num(g['correcao_media'])} | {num(g['correcao_media_sem_resposta'])} "
                  f"| {num(g['fidelidade_media'])} | {num(g['nao_suportadas_total'], 0)} | {num(g['citacoes_media'])} "
                  f"| {g['abstencoes_certas']} | {g['abstencoes_indevidas']} | {g['portugues_europeu_pct']}% "
                  f"| {num(s['latencia_media_s'], 1)} | {num(s['tokens_por_s_media'], 0)} |")
    md += ["", "Correção: média das 12 perguntas com resposta; nas 3 sem resposta, 2 se diz que a informação não está nas "
               "fontes. Fidelidade, afirmações não suportadas e citações: nas respostas que não se abstêm (frase fixa, "
               "medida em código). Abstenções indevidas: nas perguntas com resposta, incluindo aquelas em que a pesquisa "
               "não trouxe o trecho certo."]
    (PASTA / "resumo_grelha.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description="Avalia as respostas dos LLM do E1 com o juiz da grelha comum.")
    ap.add_argument("--modelo", choices=list(geracao.LLMS), action="append", help="por omissão, todos")
    ap.add_argument("--perguntas", nargs="+", help="só estas perguntas (por omissão, as 15)")
    ap.add_argument("--juiz", choices=list(juiz.JUIZES), default="gpt-oss-20b")
    ap.add_argument("--so-resumo", action="store_true", help="não chama o juiz: só refaz os resumos")
    args = ap.parse_args()
    comum.prepara_consola()
    for modelo in args.modelo or geracao.LLMS:
        linhas = comum.le_jsonl(PASTA / modelo / "results.jsonl") if args.so_resumo else avalia_modelo(modelo, args.juiz, args.perguntas)
        atualiza_config(modelo, linhas, args.juiz)
    escreve_resumo()
    print(f"Tabela em {(PASTA / 'resumo_grelha.md').relative_to(comum.RAIZ)}")


if __name__ == "__main__":
    main()
