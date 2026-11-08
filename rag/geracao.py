"""Respostas dos LLM locais (Ollama) com os parâmetros do plano de 2/11, e as verificações automáticas de cada uma.

Parâmetros iguais para os 4 modelos: temperatura 0, semente fixa, contexto de 8 192 tokens, até 600 tokens de
resposta, sem raciocínio (think=False nos modelos que o têm) e penalizações de repetição a zero (decidido a 6/11:
o Qwen3.5 traz presence_penalty 1.5, que mesmo com temperatura 0 castiga repetir tokens como [E1-003]).
"""
import functools
import re
import time

import ollama

import prompt_geracao as prompt

LLMS = {
    "gemma4-12b": "gemma4:12b",
    "qwen3.5-9b": "qwen3.5:9b",
    "amalia-9b": "hf.co/teex-pt/AMALIA-9B-0626-DPO-GGUF:Q4_K_M",
    "ministral-3-14b": "ministral-3:14b",
}
OPCOES = {"temperature": 0, "seed": 42, "num_ctx": 8192, "num_predict": 600,
          "repeat_penalty": 1.0, "presence_penalty": 0.0, "frequency_penalty": 0.0}

CITACAO = re.compile(r"\[E[1-4]-\d{3}\]")  # a expressão regular combinada no grupo
QUASE_CITACAO = re.compile(r"\[[^\]\n]*E\d-\d+[^\]\n]*\]")  # um doc_id entre parênteses retos, bem ou mal escrito


@functools.cache
def info(modelo):
    """Versão exata do modelo e se tem modo de raciocínio (para o desligar)."""
    m = LLMS[modelo]
    s = ollama.show(m)
    digest = next((x.digest for x in ollama.list().models if x.model == m), None)
    return {"name": modelo, "ollama_model": m, "digest": digest, "quantization": s.details.quantization_level,
            "parameters": s.details.parameter_size, "thinking": "thinking" in (s.capabilities or [])}


def responde(modelo, pergunta, excertos):
    kw = {"think": False} if info(modelo)["thinking"] else {}
    t = time.perf_counter()
    r = ollama.chat(model=LLMS[modelo], messages=prompt.mensagens(pergunta, excertos), options=OPCOES, **kw)
    latencia = time.perf_counter() - t
    return {"answer": r.message.content, "llm_model_returned": r.model, "latency_s": round(latencia, 2),
            "load_s": round(r.load_duration / 1e9, 2), "tokens_in": r.prompt_eval_count, "tokens_out": r.eval_count,
            "tokens_per_s": round(r.eval_count / (r.eval_duration / 1e9), 1), "done_reason": r.done_reason,
            "thinking_returned": bool(r.message.thinking)}


def verifica(resposta, excertos):
    """Abstenção (a frase fixa no início), citações válidas, citações fora dos excertos e citações mal escritas."""
    inicio = resposta.strip().lstrip("«\"“*_ ").lower()
    citados = list(dict.fromkeys(c.strip("[]") for c in CITACAO.findall(resposta)))
    dados = {x["doc_id"] for x in excertos}
    return {"abstained": inicio.startswith(prompt.ABSTENCAO.rstrip(".").lower()),
            "abstention_phrase_elsewhere": prompt.ABSTENCAO.rstrip(".").lower() in resposta.lower()
                                           and not inicio.startswith(prompt.ABSTENCAO.rstrip(".").lower()),
            "cited_doc_ids": citados,
            "citations_outside_context": [c for c in citados if c not in dados],
            "malformed_citations": [c for c in QUASE_CITACAO.findall(resposta) if not CITACAO.fullmatch(c)]}
