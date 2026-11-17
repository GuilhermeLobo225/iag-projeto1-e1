"""Juiz LLM da grelha comum: as duas avaliações (prompt_juiz.py), com o JSON validado em código.

Juízes (8/11):
  gpt-oss-120b  pelo Groq: o juiz proposto ao grupo (melhor concordância com as avaliações humanas do E3).
  gpt-oss-20b   pelo Ollama: a alternativa local da grelha, que só vale se passar no piloto.
Os dois com o mesmo prompt e os mesmos esquemas, temperatura 0 e raciocínio «medium» (não dá para o desligar;
no teste de 6/11, o 20b com «low» não seguiu o esquema JSON e deu nota a mais).
Corridas: no 20b, repetir o mesmo pedido deu sempre 1.ª corrida diferente e 2.ª igual à 3.ª, o que aponta para a
cache de prompts do Ollama e não para acaso. A mediana de 3 corridas não acrescenta robustez: fica 1 corrida.
Regra aplicada em código: uma resposta com afirmações e sem nenhuma citação [id] tem 0 nas citações («0 se não
cita»); a nota do juiz fica guardada em nota_citacoes_juiz.
Ciclos: com temperatura 0, o raciocínio pode entrar num ciclo (o 20b, na resposta do Qwen3.5 à E1-05, repetiu a
mesma frase até aos 4 096 tokens, sem chegar ao JSON), e repetir com temperatura 0 dá o mesmo ciclo. Por isso só a
1.ª tentativa usa temperatura 0; se falhar, as seguintes usam TEMPERATURA_REPETICAO, registada em cada pedido.
"""
import json
import statistics
import time

import ollama

import cliente_groq
import prompt_geracao
import prompt_juiz as p

JUIZES = {
    "gpt-oss-120b": {"fornecedor": "groq", "modelo": "openai/gpt-oss-120b", "raciocinio": "medium"},
    "gpt-oss-20b": {"fornecedor": "ollama", "modelo": "gpt-oss:20b", "raciocinio": "medium"},
}
TEMPERATURA, SEMENTE, MAX_TOKENS = 0, 42, 4096
OPCOES_OLLAMA = {"num_ctx": 12288}
CORRIDAS = 1
TENTATIVAS = 3  # pedidos a mais quando o JSON não é válido
TEMPERATURA_REPETICAO = 0.5


def parametros(nome):
    """Para o config.json."""
    extra = {"ollama_options": OPCOES_OLLAMA} if JUIZES[nome]["fornecedor"] == "ollama" else {}
    return JUIZES[nome] | {"temperature": TEMPERATURA, "seed": SEMENTE, "max_tokens": MAX_TOKENS, "runs": CORRIDAS,
                           "retries": TENTATIVAS - 1, "retry_temperature": TEMPERATURA_REPETICAO} | extra


def _chama(nome, mensagens, esquema, temperatura, semente):
    """Texto da resposta do juiz e os dados do pedido (tokens, tempo, se veio da cache)."""
    j, t = JUIZES[nome], time.perf_counter()
    if j["fornecedor"] == "ollama":
        r = ollama.chat(model=j["modelo"], messages=mensagens, format=esquema, think=j["raciocinio"],
                        options=OPCOES_OLLAMA | {"temperature": temperatura, "seed": semente, "num_predict": MAX_TOKENS})
        return r.message.content, {"s": round(time.perf_counter() - t, 1), "tokens_in": r.prompt_eval_count,
                                   "tokens_out": r.eval_count}
    corpo = {"model": j["modelo"], "messages": mensagens, "temperature": temperatura, "seed": semente,
             "reasoning_effort": j["raciocinio"], "max_completion_tokens": MAX_TOKENS,
             "response_format": {"type": "json_schema", "json_schema": {"name": "avaliacao", "schema": esquema}}}
    previstos = sum(len(m["content"]) for m in mensagens) // 3 + 2000
    r, da_cache = cliente_groq.pede(corpo, previstos)
    u = r.get("usage", {})
    return r["choices"][0]["message"].get("content") or "", {
        "s": round(time.perf_counter() - t, 1), "tokens_in": u.get("prompt_tokens"), "tokens_out": u.get("completion_tokens"),
        "tokens_raciocinio": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
        "cache": da_cache, "modelo_devolvido": r.get("model")}


def valida_correcao(d, sem_resposta):
    if not isinstance(d.get("justificacao"), str) or d.get("nota_correcao") not in p.notas_correcao(sem_resposta):
        raise ValueError(f"correção inválida: {d}")


def valida_fidelidade(d):
    erros = [k for k in ("justificacao_citacoes", "justificacao_abstencao", "justificacao_portugues") if not isinstance(d.get(k), str)]
    erros += [k for k in ("abstencao", "excertos_tinham_resposta", "portugues_europeu") if not isinstance(d.get(k), bool)]
    if d.get("nota_citacoes") not in (0, 1, 2):
        erros.append("nota_citacoes")
    if not isinstance(d.get("afirmacoes"), list):
        erros.append("afirmacoes")
    else:
        for a in d["afirmacoes"]:
            if not (isinstance(a, dict) and isinstance(a.get("afirmacao"), str) and isinstance(a.get("suportada"), bool)
                    and all(isinstance(a.get(k), list) and all(isinstance(i, str) for i in a[k])
                            for k in ("ids_citados", "ids_que_suportam"))):
                erros.append(f"afirmação inválida: {a}")
    if erros:
        raise ValueError(f"fidelidade inválida: {erros}")


def pede(nome, mensagens, esquema, valida):
    """Um pedido ao juiz; repete (com outra semente e TEMPERATURA_REPETICAO) se o JSON não for válido."""
    erro = None
    for tentativa in range(TENTATIVAS):
        temperatura = TEMPERATURA_REPETICAO if tentativa else TEMPERATURA
        try:
            texto, dados_pedido = _chama(nome, mensagens, esquema, temperatura, SEMENTE + tentativa)
            dados = json.loads(texto)
            valida(dados)
            return dados, dados_pedido | {"tentativas": tentativa + 1, "temperature": temperatura}
        except (json.JSONDecodeError, ValueError, cliente_groq.RespostaInvalida) as e:
            erro = e
    raise RuntimeError(f"o juiz não devolveu JSON válido em {TENTATIVAS} tentativas: {erro}")


def mediana(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def maioria(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) > len(xs) / 2 if xs else None


def avalia(nome, pergunta, excertos, resposta, citacao=prompt_geracao.CITACAO):
    """As duas avaliações, CORRIDAS vezes. citacao: o formato das citações ("doc" ou "excerto").
    Devolve (corridas, agregado)."""
    sem = pergunta["type"] == "unanswerable"
    ids_escritos = list(dict.fromkeys(c.strip("[]") for c in prompt_geracao.regex(citacao).findall(resposta)))
    corridas = []
    for _ in range(CORRIDAS):
        a, ta = pede(nome, p.mensagens_correcao(pergunta, resposta), p.esquema_correcao(sem), lambda d: valida_correcao(d, sem))
        b, tb = pede(nome, p.mensagens_fidelidade(pergunta, excertos, resposta, ids_escritos, citacao), p.ESQUEMA_FIDELIDADE,
                     valida_fidelidade)
        af = b["afirmacoes"]
        corridas.append({"justificacao_correcao": a["justificacao"], "nota_correcao": a["nota_correcao"],
                         "afirmacoes": af,
                         "fidelidade": round(sum(x["suportada"] for x in af) / len(af), 3) if af else None,
                         "nao_suportadas": sum(not x["suportada"] for x in af),
                         "justificacao_citacoes": b["justificacao_citacoes"],
                         "nota_citacoes": None if not af else 0 if not ids_escritos else b["nota_citacoes"],
                         "nota_citacoes_juiz": b["nota_citacoes"],
                         "justificacao_abstencao": b["justificacao_abstencao"], "abstencao": b["abstencao"],
                         "excertos_tinham_resposta": b["excertos_tinham_resposta"],
                         "justificacao_portugues": b["justificacao_portugues"], "portugues_europeu": b["portugues_europeu"],
                         "pedidos": {"correcao": ta, "fidelidade": tb}})
    agregado = {"correcao": mediana(c["nota_correcao"] for c in corridas),
                "fidelidade": mediana(c["fidelidade"] for c in corridas),
                "nao_suportadas": mediana(c["nao_suportadas"] for c in corridas),
                "citacoes": mediana(c["nota_citacoes"] for c in corridas),
                "abstencao": maioria(c["abstencao"] for c in corridas),
                "abstencao_com_resposta_nos_excertos": maioria(c["abstencao"] and c["excertos_tinham_resposta"] for c in corridas),
                "portugues_europeu": maioria(c["portugues_europeu"] for c in corridas)}
    return corridas, agregado
