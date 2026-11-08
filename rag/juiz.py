"""Juiz LLM da grelha comum: as duas avaliações (prompt_juiz.py), com o JSON validado em código.

Juiz por omissão: gpt-oss-20b pelo Ollama, a alternativa local da grelha (só vale se passar no piloto).
Não dá para desligar o raciocínio deste modelo: no teste de 6/11, com «low» não seguiu o esquema JSON e deu nota
a mais; com «medium» seguiu-o e acertou.
Corridas: com temperatura 0, repetir o mesmo pedido deu sempre 1.ª corrida diferente e 2.ª igual à 3.ª, o que
aponta para a cache de prompts do Ollama (calculado de raiz contra reaproveitado), e não para acaso. A mediana de
3 corridas não acrescenta robustez, por isso fica 1 corrida, como na grelha.
Regra aplicada em código: uma resposta com afirmações e sem nenhuma citação [id] tem 0 nas citações («0 se não
cita»); a nota do juiz fica guardada em nota_citacoes_juiz.
Ciclos: com temperatura 0, o raciocínio pode entrar num ciclo (na resposta do Qwen3.5 à E1-05 repetiu a mesma
frase até aos 4 096 tokens, sem chegar ao JSON), e repetir com temperatura 0 dá o mesmo ciclo. Por isso só a 1.ª
tentativa usa temperatura 0; se falhar, as seguintes usam TEMPERATURA_REPETICAO, registada em cada pedido.
"""
import json
import statistics
import time

import ollama

import geracao
import prompt_juiz as p

JUIZES = {"gpt-oss-20b": {"ollama": "gpt-oss:20b", "think": "medium"}}
OPCOES = {"temperature": 0, "seed": 42, "num_ctx": 12288, "num_predict": 4096}
CORRIDAS = 1
TENTATIVAS = 3  # pedidos a mais quando o JSON não é válido
TEMPERATURA_REPETICAO = 0.5


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


def pede(juiz, mensagens, esquema, valida):
    """Um pedido ao juiz; repete (com outra semente e TEMPERATURA_REPETICAO) se o JSON não for válido."""
    j, erro = JUIZES[juiz], None
    for tentativa in range(TENTATIVAS):
        opcoes = OPCOES | {"seed": OPCOES["seed"] + tentativa} | ({"temperature": TEMPERATURA_REPETICAO} if tentativa else {})
        t = time.perf_counter()
        r = ollama.chat(model=j["ollama"], messages=mensagens, format=esquema, think=j["think"], options=opcoes)
        try:
            dados = json.loads(r.message.content)
            valida(dados)
            return dados, {"tentativas": tentativa + 1, "temperature": opcoes["temperature"],
                           "s": round(time.perf_counter() - t, 1), "tokens_out": r.eval_count}
        except (json.JSONDecodeError, ValueError) as e:
            erro = e
    raise RuntimeError(f"o juiz não devolveu JSON válido em {TENTATIVAS} tentativas: {erro}")


def mediana(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def maioria(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) > len(xs) / 2 if xs else None


def avalia(juiz, pergunta, excertos, resposta):
    """As duas avaliações, CORRIDAS vezes. Devolve (corridas, agregado)."""
    sem = pergunta["type"] == "unanswerable"
    ids_escritos = list(dict.fromkeys(c.strip("[]") for c in geracao.CITACAO.findall(resposta)))
    corridas = []
    for _ in range(CORRIDAS):
        a, ta = pede(juiz, p.mensagens_correcao(pergunta, resposta), p.esquema_correcao(sem), lambda d: valida_correcao(d, sem))
        b, tb = pede(juiz, p.mensagens_fidelidade(pergunta, excertos, resposta, ids_escritos), p.ESQUEMA_FIDELIDADE,
                     valida_fidelidade)
        af = b["afirmacoes"]
        nota_citacoes = None if not af else 0 if not ids_escritos else b["nota_citacoes"]
        corridas.append({"justificacao_correcao": a["justificacao"], "nota_correcao": a["nota_correcao"],
                         "afirmacoes": af,
                         "fidelidade": round(sum(x["suportada"] for x in af) / len(af), 3) if af else None,
                         "nao_suportadas": sum(not x["suportada"] for x in af),
                         "justificacao_citacoes": b["justificacao_citacoes"],
                         "nota_citacoes": nota_citacoes,  # None se não há afirmações; 0 se não cita
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
