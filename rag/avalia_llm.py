#!/usr/bin/env python3
"""Teste dos 4 LLM para o grupo (7/11): as 15 perguntas, com os mesmos 5 excertos para todos os modelos.

1. contexto.jsonl: para cada pergunta, os 5 primeiros excertos do melhor embedding na melhor configuração
   (regra do plano: Recall@5, depois MRR@5, depois B), tirados do results.jsonl do teste dos embeddings.
2. Para cada LLM: um aquecimento com a 1.ª pergunta, cuja resposta se deita fora. Carrega o modelo, compila os
   kernels da GPU e gasta a primeira resposta depois de carregar, que pode sair diferente das seguintes.
   Depois, as 15 perguntas, com a latência de cada uma.
3. As verificações automáticas de cada resposta (geracao.verifica) e o resumo por modelo.
A avaliação pela grelha (juízes) faz-se depois, sobre estes results.jsonl.

Saída em experiments/E1/modelos/llm/:
  contexto.jsonl            os 5 excertos de cada pergunta, com o texto
  <modelo>/config.json      modelo (com o digest), parâmetros, prompt (versão e SHA-1), contexto e tempos
  <modelo>/results.jsonl    uma linha por pergunta: resposta, citações, abstenção, latência e tokens
  resumo.md                 a tabela das verificações automáticas e da latência

Configurações B e C (8/11): as mesmas 15 perguntas com os 5 primeiros excertos das experiências B e C do
Qwen3-Embedding 8B (experiments/E1/B e C), para os 4 LLM serem comparados em A, B e C com o mesmo embedding.
Saída em experiments/E1/modelos/llm_B/ e llm_C/, com a mesma estrutura. As respostas que já existem nessas
experiências (o Gemma 4) reaproveitam-se, se o prompt e os excertos forem os mesmos.

Uso, na raiz do repositório (com o Ollama a correr):
  .venv\\Scripts\\python rag/avalia_llm.py                       os 4 modelos, na A
  .venv\\Scripts\\python rag/avalia_llm.py --modelo gemma4-12b   só um
  .venv\\Scripts\\python rag/avalia_llm.py --config B            os 4 modelos, na B
"""
import argparse
import json
import statistics
from datetime import date

import avalia_embeddings
import comum
import geracao
import metricas
import prompt_geracao as prompt

PASTAS = {"A": comum.EXPERIENCIAS / "modelos/llm", "B": comum.EXPERIENCIAS / "modelos/llm_B",
          "C": comum.EXPERIENCIAS / "modelos/llm_C"}
PASTA = PASTAS["A"]


def contexto_da_experiencia(config):
    """B e C: os 5 primeiros excertos de cada pergunta na experiência final com o mesmo nome (Qwen3-Embedding 8B)."""
    cfg = json.loads((comum.EXPERIENCIAS / config / "config.json").read_text(encoding="utf-8"))
    nome = f"{cfg['retrieval']['embedding']}_{config} ({cfg['run']['retrieval']['mode']}, excertos {cfg['run']['chunks']})"
    perguntas = {p["id"]: p for p in comum.le_jsonl(comum.PERGUNTAS)}
    linhas = []
    for r in comum.le_jsonl(comum.EXPERIENCIAS / config / "results.jsonl"):
        por_id = {x["chunk_id"]: x for x in comum.le_jsonl(comum.EXPERIENCIAS / f"excertos_{r['chunks']}.jsonl")}
        linhas.append({"question_id": r["question_id"], "type": r["type"], "question": perguntas[r["question_id"]]["question"],
                       "embedding_experiment": nome, "config": config, "recall_at_5": r["recall_at_5"],
                       "excertos": [por_id[x["chunk_id"]] | {"rank": x["rank"], "score": x["score"]}
                                    for x in r["retrieved"][:metricas.K]]})
    comum.grava_jsonl(PASTAS[config] / "contexto.jsonl", linhas)
    return linhas


def contexto(config="A"):
    """Os 5 excertos de cada pergunta, do melhor embedding; grava-os e devolve-os.
    Se o contexto.jsonl já existir, fica o embedding com que foi feito: a 8/11, com o Qwen3-Embedding 4B, a melhor
    experiência mudou, e o teste dos LLM (e as avaliações dos juízes) foi feito com o 8B na A."""
    if config != "A":
        return contexto_da_experiencia(config)
    caminho = PASTA / "contexto.jsonl"
    if caminho.exists():
        antigo = comum.le_jsonl(caminho)[0]
        nome, config = antigo["embedding_experiment"], antigo["config"]
    else:
        melhor = avalia_embeddings.melhor(avalia_embeddings.le_configs())
        nome, config = melhor["experiment"], melhor["chunks"]["config"]
    por_id = {x["chunk_id"]: x for x in comum.le_jsonl(comum.EXPERIENCIAS / f"excertos_{config}.jsonl")}
    perguntas = {p["id"]: p for p in comum.le_jsonl(comum.PERGUNTAS)}
    linhas = []
    for r in comum.le_jsonl(avalia_embeddings.PASTA / nome / "results.jsonl"):
        linhas.append({"question_id": r["question_id"], "type": r["type"], "question": perguntas[r["question_id"]]["question"],
                       "embedding_experiment": nome, "config": config, "recall_at_5": r["recall_at_5"],
                       "excertos": [por_id[x["chunk_id"]] | {"rank": x["rank"], "score": x["score"]}
                                    for x in r["retrieved"][:metricas.K]]})
    comum.grava_jsonl(PASTA / "contexto.jsonl", linhas)
    return linhas


def resume(linhas):
    sem = [x for x in linhas if x["type"] == "unanswerable"]
    # Nas perguntas com resposta, abster-se só é falsa abstenção se algum trecho certo estava nos 5 excertos.
    com = [x for x in linhas if x["type"] != "unanswerable" and x["recall_at_5"] > 0]
    sem_evidencia = [x for x in linhas if x["type"] != "unanswerable" and x["recall_at_5"] == 0]
    respostas = [x for x in linhas if not x["abstained"]]
    return {"abstencao_correta": f"{sum(x['abstained'] for x in sem)}/{len(sem)}",
            "falsa_abstencao": f"{sum(x['abstained'] for x in com)}/{len(com)}",
            "abstencao_sem_o_trecho_nos_excertos": f"{sum(x['abstained'] for x in sem_evidencia)}/{len(sem_evidencia)}",
            "frase_de_abstencao_fora_do_inicio": sum(x["abstention_phrase_elsewhere"] for x in linhas),
            "respostas_com_citacao": f"{sum(bool(x['cited_doc_ids']) for x in respostas)}/{len(respostas)}",
            "citacoes_fora_dos_excertos": sum(len(x["citations_outside_context"]) for x in linhas),
            "citacoes_mal_escritas": sum(len(x["malformed_citations"]) for x in linhas),
            "truncadas": sum(x["done_reason"] == "length" for x in linhas),
            "com_raciocinio": sum(x["thinking_returned"] for x in linhas),
            "latencia_media_s": round(statistics.mean(x["latency_s"] for x in linhas), 2),
            "latencia_max_s": max(x["latency_s"] for x in linhas),
            "tokens_por_s_media": round(statistics.mean(x["tokens_per_s"] for x in linhas), 1),
            "tokens_in_media": round(statistics.mean(x["tokens_in"] for x in linhas)),
            "tokens_out_media": round(statistics.mean(x["tokens_out"] for x in linhas))}


def linha(c, modelo, r, v):
    return ({"question_id": c["question_id"], "type": c["type"], "config": c["config"], "embedding": c["embedding_experiment"],
             "llm": modelo, "recall_at_5": c["recall_at_5"],
             "retrieved": [{k: x[k] for k in ("rank", "chunk_id", "doc_id", "start", "end", "score")} for x in c["excertos"]]}
            | r | v)


def grava(modelo, contextos, linhas, pasta, origem=None):
    info = geracao.info(modelo)
    comum.grava_jsonl(pasta / modelo / "results.jsonl", linhas)
    cfg = {"experiment": f"llm_{modelo}", "area": "E1", "date": date.today().isoformat(), "git_commit": comum.commit_git(),
           "llm": info | {"options": geracao.OPCOES, "think": False if info["thinking"] else None,
                          "ollama_version": comum.versao_ollama()},
           "prompt": {"version": prompt.VERSAO, "sha1": prompt.sha1(), "abstention_phrase": prompt.ABSTENCAO},
           "context": {"file": (pasta / "contexto.jsonl").relative_to(comum.RAIZ).as_posix(),
                       "embedding_experiment": contextos[0]["embedding_experiment"], "config": contextos[0]["config"], "k": metricas.K},
           "warmup": "1.ª pergunta, resposta deitada fora", "gpu": avalia_embeddings.gpu(),
           "summary": resume(linhas)} | ({"answers_from": origem} if origem else {})
    (pasta / modelo / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return cfg


def reaproveita(modelo, contextos, pasta):
    """Na B e na C: usa as respostas da experiência final com o mesmo nome, se forem deste LLM, com o mesmo prompt
    e os mesmos 5 excertos em cada pergunta. Devolve o config.json gravado, ou None."""
    config = contextos[0]["config"]
    caminho = comum.EXPERIENCIAS / config / "config.json"
    if config == "A" or not caminho.exists():
        return None
    exp = json.loads(caminho.read_text(encoding="utf-8"))
    if exp["llm"] != modelo or exp["run"].get("prompt", {}).get("sha1") != prompt.sha1():
        return None
    respostas = {x["question_id"]: x for x in comum.le_jsonl(comum.EXPERIENCIAS / config / "results.jsonl")}
    if any([x["chunk_id"] for x in respostas[c["question_id"]]["retrieved"][:metricas.K]] != [x["chunk_id"] for x in c["excertos"]]
           for c in contextos):
        return None
    campos = ("answer", "llm_model_returned", "latency_s", "load_s", "tokens_in", "tokens_out", "tokens_per_s", "done_reason",
              "thinking_returned")
    linhas = [linha(c, modelo, {k: respostas[c["question_id"]][k] for k in campos},
                    geracao.verifica(respostas[c["question_id"]]["answer"], c["excertos"])) for c in contextos]
    return grava(modelo, contextos, linhas, pasta, f"experiments/E1/{config}/results.jsonl")


def corre(modelo, contextos, pasta=PASTA):
    cfg = reaproveita(modelo, contextos, pasta)
    if cfg:
        print(f"  respostas reaproveitadas de {cfg['answers_from']}", flush=True)
        return cfg
    geracao.responde(modelo, contextos[0]["question"], contextos[0]["excertos"])  # aquecimento, deita-se fora
    linhas = []
    for c in contextos:
        r = geracao.responde(modelo, c["question"], c["excertos"])
        linhas.append(linha(c, modelo, r, geracao.verifica(r["answer"], c["excertos"])))
        print(f"  {c['question_id']}: {r['latency_s']} s, {r['tokens_out']} tokens", flush=True)
    return grava(modelo, contextos, linhas, pasta)


def escreve_resumo(pasta=PASTA):
    num = avalia_embeddings.num
    cfgs = [json.loads((pasta / m / "config.json").read_text(encoding="utf-8"))
            for m in geracao.LLMS if (pasta / m / "config.json").exists()]
    c0 = cfgs[0]
    md = ["# Teste dos LLM (E1): verificações automáticas e latência", "",
          f"{date.today():%d/%m/%Y}. As 15 perguntas, com os mesmos 5 excertos para todos ({c0['context']['embedding_experiment']}). "
          f"Prompt {c0['prompt']['version']} (SHA-1 `{c0['prompt']['sha1'][:12]}`); temperatura 0, semente {geracao.OPCOES['seed']}, "
          f"contexto de {geracao.OPCOES['num_ctx']} tokens, até {geracao.OPCOES['num_predict']} de resposta, sem raciocínio, "
          f"penalizações de repetição a zero. {c0['gpu']}, Ollama {c0['llm']['ollama_version']}, todos em Q4_K_M, "
          "depois de um aquecimento com a 1.ª pergunta.", "",
          "| LLM | Abstenção correta (sem resposta) | Falsa abstenção (trecho nos excertos) | Abstenção (trecho fora dos excertos) "
          "| Respostas com citação | Citações fora dos excertos | Citações mal escritas | Truncadas | Latência média (s) | Tokens/s |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for c in cfgs:
        s = c["summary"]
        md.append(f"| {c['llm']['name']} | {s['abstencao_correta']} | {s['falsa_abstencao']} "
                  f"| {s['abstencao_sem_o_trecho_nos_excertos']} | {s['respostas_com_citacao']} "
                  f"| {s['citacoes_fora_dos_excertos']} | {s['citacoes_mal_escritas']} | {s['truncadas']} "
                  f"| {num(s['latencia_media_s'], 1)} | {num(s['tokens_por_s_media'], 0)} |")
    md += ["", "Abstenção: a resposta começa com a frase fixa (uma abstenção por outras palavras não conta). Falsa abstenção: "
               "nas perguntas com resposta em que algum trecho certo estava nos 5 excertos; quando nenhum estava "
               "(Recall@5 = 0), abster-se é o comportamento certo e conta-se à parte. Respostas com citação: das que não se "
               "abstêm, as que têm pelo menos uma citação `[E1-003]` válida. A correção, a fidelidade e as citações frase a "
               "frase avaliam-se depois com os juízes."]
    (pasta / "resumo.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description="Testa os 4 LLM do E1 com as 15 perguntas.")
    ap.add_argument("--modelo", choices=list(geracao.LLMS), action="append", help="por omissão, todos")
    ap.add_argument("--config", choices=list(PASTAS), default="A", help="excertos da A (por omissão), da B ou da C")
    ap.add_argument("--so-resumo", action="store_true",
                    help="não gera respostas: recalcula os resumos a partir dos results.jsonl que existem")
    args = ap.parse_args()
    comum.prepara_consola()
    pasta = PASTAS[args.config]
    if args.so_resumo:
        for m in geracao.LLMS:
            caminho = pasta / m / "config.json"
            if caminho.exists():
                cfg = json.loads(caminho.read_text(encoding="utf-8"))
                cfg["summary"] = resume(comum.le_jsonl(pasta / m / "results.jsonl"))
                caminho.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        escreve_resumo(pasta)
        print(f"Tabela em {(pasta / 'resumo.md').relative_to(comum.RAIZ)}")
        return
    contextos = contexto(args.config)
    for modelo in args.modelo or geracao.LLMS:
        print(f"{modelo} ({args.config}):", flush=True)
        s = corre(modelo, contextos, pasta)["summary"]
        print(f"{modelo}: " + ", ".join(f"{k} {v}" for k, v in s.items()), flush=True)
    escreve_resumo(pasta)
    print(f"Tabela em {(pasta / 'resumo.md').relative_to(comum.RAIZ)}")


if __name__ == "__main__":
    main()
