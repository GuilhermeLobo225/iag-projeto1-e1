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

CITACAO = prompt.regex()  # a expressão regular combinada no grupo (formato "doc"; os formatos estão no prompt_geracao)
QUASE_CITACAO = re.compile(r"\[[^\]\n]*E\d-\d+[^\]\n]*\]")  # um doc_id entre parênteses retos, bem ou mal escrito


@functools.cache
def info(modelo):
    """Versão exata do modelo e se tem modo de raciocínio (para o desligar)."""
    m = LLMS[modelo]
    s = ollama.show(m)
    digest = next((x.digest for x in ollama.list().models if x.model == m), None)
    return {"name": modelo, "ollama_model": m, "digest": digest, "quantization": s.details.quantization_level,
            "parameters": s.details.parameter_size, "thinking": "thinking" in (s.capabilities or [])}


def responde(modelo, pergunta, excertos, abstencao=prompt.ABSTENCAO, citacao=prompt.CITACAO):
    kw = {"think": False} if info(modelo)["thinking"] else {}
    t = time.perf_counter()
    r = ollama.chat(model=LLMS[modelo], messages=prompt.mensagens(pergunta, excertos, abstencao, citacao), options=OPCOES, **kw)
    latencia = time.perf_counter() - t
    return {"answer": r.message.content, "llm_model_returned": r.model, "latency_s": round(latencia, 2),
            "load_s": round(r.load_duration / 1e9, 2), "tokens_in": r.prompt_eval_count, "tokens_out": r.eval_count,
            "tokens_per_s": round(r.eval_count / (r.eval_duration / 1e9), 1), "done_reason": r.done_reason,
            "thinking_returned": bool(r.message.thinking)}


def verifica(resposta, excertos, abstencao=prompt.ABSTENCAO, citacao=prompt.CITACAO):
    """Abstenção (a frase fixa no início), citações válidas, citações fora dos excertos e citações mal escritas.
    cited_doc_ids tem sempre doc_id; no formato "excerto", os ids citados vêm em cited_ids."""
    frase = abstencao.rstrip(".").lower()
    inicio = resposta.strip().lstrip("«\"“*_ ").lower()
    rx, campo = prompt.regex(citacao), prompt.CITACOES[citacao]["campo"]
    citados = list(dict.fromkeys(c.strip("[]") for c in rx.findall(resposta)))
    dados = {x[campo] for x in excertos}
    return {"abstained": inicio.startswith(frase),
            "abstention_phrase_elsewhere": frase in resposta.lower() and not inicio.startswith(frase),
            "cited_ids": citados, "cited_doc_ids": list(dict.fromkeys(c.split("_")[0] for c in citados)),
            "citations_outside_context": [c for c in citados if c not in dados],
            "malformed_citations": [c for c in QUASE_CITACAO.findall(resposta) if not rx.fullmatch(c)]}
