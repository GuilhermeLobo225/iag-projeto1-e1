#!/usr/bin/env python3
"""Parte os .txt da base em excertos para as configurações A (500/50 tokens) e B (200/20 tokens).

Regras (plano de 2/11):
  1. Unidades: o texto parte-se primeiro nas mudanças de linha e depois no fim das frases.
     Uma frase com mais tokens do que o máximo é cortada por tokens.
  2. Cada excerto junta unidades inteiras, pela ordem, enquanto o texto do excerto couber no máximo.
     O máximo é estrito; só o último excerto de cada documento pode ficar bastante mais curto.
  3. Sobreposição: o excerto seguinte começa com as últimas unidades do anterior que caibam em
     50 (A) ou 20 (B) tokens. Se a última unidade já passar desse limite, não há sobreposição.
  4. O texto não muda: cada excerto é texto[start:end] do .txt (fim exclusivo) e nunca junta documentos.
Os tokens contam-se no texto de cada excerto, com o tokenizador do bge-m3 e sem tokens especiais.

Saída em experiments/E1/:
  excertos_A.jsonl   um excerto por linha: chunk_id, doc_id, start, end, tokens, title, entity, url, text
  excertos_A.json    parâmetros, tokenizador, SHA-1 dos .txt e estatísticas (para o relatório)
No fim, relê os ficheiros gravados e confirma as regras 2 e 4 e que nenhum texto ficou de fora.

Uso, na raiz do repositório:
  .venv\\Scripts\\python rag/excertos.py              gera A e B
  .venv\\Scripts\\python rag/excertos.py --config B   gera só a B
"""
import argparse
import json
import re
import statistics
from datetime import date

import comum

CONFIGS = {"A": {"max_tokens": 500, "overlap_tokens": 50}, "B": {"max_tokens": 200, "overlap_tokens": 20}}

# Fim de frase: . ! ? ou … (com aspas ou parênteses a fechar), espaço e uma maiúscula (ou aspas/parêntese a abrir).
# Não corta antes de algarismos, para não partir «art. 5.º» ou «p. 12».
FIM_FRASE = re.compile(r"[.!?…]+[»\"”’)\]]*(?=\s+[«\"“‘(\[]?[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ])")
# Abreviaturas seguidas de maiúscula que não acabam a frase («Sr. Presidente», «cf. Anexo»).
ABREVIATURAS = {"sr", "sra", "srs", "dr", "dra", "drs", "eng", "enga", "arq", "prof", "profa", "av", "exmo", "exma",
                "art", "arts", "al", "cf", "ex", "p", "pp", "pág", "págs", "lda", "n", "nº", "fig", "tab"}


def aparado(texto, s, e):
    while s < e and texto[s].isspace():
        s += 1
    while e > s and texto[e - 1].isspace():
        e -= 1
    return s, e


def frases(texto, s, e):
    """Intervalos das frases de uma linha [s, e)."""
    inicio = s
    for m in FIM_FRASE.finditer(texto, s, e):
        palavra = re.search(r"(\w+)$", texto[inicio:m.start()])
        if texto[m.start()] == "." and palavra and (palavra[1].lower() in ABREVIATURAS
                                                   or (len(palavra[1]) == 1 and palavra[1].isupper())):
            continue  # abreviatura ou inicial («D. João»)
        yield aparado(texto, inicio, m.end())
        inicio = m.end()
    yield aparado(texto, inicio, e)


def por_tokens(texto, s, e, tokenizador, maximo):
    """Corta uma frase demasiado longa em pedaços de até `maximo` tokens, pelas posições dos tokens."""
    conta = comum.contador(tokenizador)
    offsets = [(s + a, s + b) for a, b in tokenizador.encode(texto[s:e], add_special_tokens=False).offsets]
    i = 0
    while i < len(offsets):
        j = min(i + maximo, len(offsets))
        while conta(texto[offsets[i][0]:offsets[j - 1][1]]) > maximo:  # recontado no texto do pedaço
            j -= 1
        yield aparado(texto, offsets[i][0], offsets[j - 1][1])
        i = j


def unidades(texto, tokenizador, maximo):
    """Intervalos [s, e) das unidades do documento (regra 1) e quantas frases foram cortadas por tokens."""
    conta = comum.contador(tokenizador)
    lista, cortadas = [], 0
    for linha in re.finditer(r"[^\n]+", texto):
        for s, e in frases(texto, linha.start(), linha.end()):
            if s == e:
                continue
            if conta(texto[s:e]) <= maximo:
                lista.append((s, e))
            else:
                lista += [p for p in por_tokens(texto, s, e, tokenizador, maximo) if p[0] < p[1]]
                cortadas += 1
    return lista, cortadas


def junta(texto, us, conta, maximo, sobreposicao):
    """Junta as unidades em excertos (regras 2 e 3). Devolve os intervalos [start, end) dos excertos."""
    excertos, i, n = [], 0, len(us)
    while i < n:
        j = i  # última unidade do excerto
        while j + 1 < n and conta(texto[us[i][0]:us[j + 1][1]]) <= maximo:
            j += 1
        excertos.append((us[i][0], us[j][1]))
        if j == n - 1:
            break
        # As últimas unidades que caibam na sobreposição (nunca o excerto inteiro, para avançar sempre).
        k = j + 1
        while k - 1 > i and conta(texto[us[k - 1][0]:us[j][1]]) <= sobreposicao:
            k -= 1
        # Se a sobreposição e a unidade seguinte não couberem juntas no máximo, começa sem sobreposição.
        if k <= j and conta(texto[us[k][0]:us[j + 1][1]]) > maximo:
            k = j + 1
        i = k
    return excertos


def gera(nome, tokenizador, catalogo):
    p = CONFIGS[nome]
    conta = comum.contador(tokenizador)
    linhas, documentos, cortadas = [], {}, 0
    for entrada in catalogo:
        texto, sha1 = comum.le_documento(entrada)
        documentos[entrada["doc_id"]] = sha1
        us, c = unidades(texto, tokenizador, p["max_tokens"])
        cortadas += c
        for n, (s, e) in enumerate(junta(texto, us, conta, p["max_tokens"], p["overlap_tokens"]), start=1):
            linhas.append({"chunk_id": f"{entrada['doc_id']}_{nome}{n:04d}", "doc_id": entrada["doc_id"], "config": nome,
                           "start": s, "end": e, "tokens": conta(texto[s:e]),
                           "title": entrada["title"], "entity": entrada["entity"], "url": entrada["url"],
                           "text": texto[s:e]})
    return linhas, documentos, cortadas


def estatisticas(linhas, conta):
    tokens = [x["tokens"] for x in linhas]
    ultimos = {x["doc_id"]: x["chunk_id"] for x in linhas}  # o último excerto de cada documento
    sem_ultimos = [x["tokens"] for x in linhas if x["chunk_id"] not in ultimos.values()]
    sobre = []
    for a, b in zip(linhas, linhas[1:]):
        if a["doc_id"] == b["doc_id"]:
            sobre.append(conta(a["text"][b["start"] - a["start"]:]) if b["start"] < a["end"] else 0)
    return {"excertos": len(linhas), "tokens_min": min(tokens), "tokens_media": round(statistics.mean(tokens), 1),
            "tokens_max": max(tokens), "tokens_min_sem_o_ultimo_de_cada_doc": min(sem_ultimos),
            "pares_seguidos_com_sobreposicao": f"{sum(1 for s in sobre if s)}/{len(sobre)}",
            "sobreposicao_media_tokens": round(statistics.mean(sobre), 1)}


def verifica(nome, catalogo, conta):
    """Relê o .jsonl gravado e confirma as regras 2 e 4 e que todo o texto não vazio está em algum excerto."""
    maximo = CONFIGS[nome]["max_tokens"]
    textos = {c["doc_id"]: comum.le_documento(c)[0] for c in catalogo}
    erros, por_doc = [], {}
    for x in comum.le_jsonl(comum.EXPERIENCIAS / f"excertos_{nome}.jsonl"):
        t = textos[x["doc_id"]]
        if t[x["start"]:x["end"]] != x["text"]:
            erros.append(f"{x['chunk_id']}: o text não é igual a texto[start:end]")
        if conta(x["text"]) != x["tokens"] or x["tokens"] > maximo:
            erros.append(f"{x['chunk_id']}: {conta(x['text'])} tokens (máximo {maximo})")
        por_doc.setdefault(x["doc_id"], []).append(x)
    for doc_id, t in textos.items():
        fim, inicio_anterior = 0, -1  # fim: até onde o texto já está coberto
        for x in por_doc.get(doc_id, []):
            if x["start"] <= inicio_anterior:
                erros.append(f"{x['chunk_id']}: excerto fora de ordem")
            if x["start"] > fim and t[fim:x["start"]].strip():
                erros.append(f"{x['chunk_id']}: ficou texto de fora antes da posição {x['start']}")
            inicio_anterior, fim = x["start"], max(fim, x["end"])
        if t[fim:].strip():
            erros.append(f"{doc_id}: o fim do documento ficou de fora")
    return erros


def main():
    ap = argparse.ArgumentParser(description="Parte a base do E1 em excertos (configurações A e B).")
    ap.add_argument("--config", choices=sorted(CONFIGS), action="append", help="A, B ou ambas (por omissão)")
    args = ap.parse_args()
    comum.prepara_consola()
    catalogo = comum.le_catalogo()
    tokenizador = comum.carrega_tokenizador()
    conta = comum.contador(tokenizador)
    for nome in args.config or sorted(CONFIGS):
        linhas, documentos, cortadas = gera(nome, tokenizador, catalogo)
        comum.grava_jsonl(comum.EXPERIENCIAS / f"excertos_{nome}.jsonl", linhas)
        stats = estatisticas(linhas, conta) | {"frases_cortadas_por_tokens": cortadas}
        meta = {"config": nome, **CONFIGS[nome], "tokenizer": comum.TOKENIZADOR, "tokenizer_revision": comum.TOKENIZADOR_REVISAO,
                "add_special_tokens": False, "date": date.today().isoformat(), "git_commit": comum.commit_git(),
                "documents_sha1": documentos, "stats": stats}
        (comum.EXPERIENCIAS / f"excertos_{nome}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                                                   encoding="utf-8", newline="\n")
        erros = verifica(nome, catalogo, conta)
        print(f"Configuração {nome} ({CONFIGS[nome]['max_tokens']}/{CONFIGS[nome]['overlap_tokens']} tokens): "
              + ", ".join(f"{k} {v}" for k, v in stats.items()))
        for e in erros[:20]:
            print("  ERRO:", e)
        print(f"  verificação: {'ok' if not erros else f'{len(erros)} erros'}")


if __name__ == "__main__":
    main()
