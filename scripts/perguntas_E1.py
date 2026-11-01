#!/usr/bin/env python3
"""Ajuda a escrever e a validar as perguntas de teste do E1 (tests/questions_E1.jsonl).

Formato combinado no grupo (uma pergunta por linha):
  {"id": "E1-01", "type": "factual", "subtopic": "...", "question": "...", "reference_answer": "...",
   "evidence": [{"doc_id": "E1-004", "start": 1234, "end": 1456, "sha1": "...", "text": "..."}], "notes": "..."}

- type: factual (8), multi_doc (4, com trechos de pelo menos 2 documentos) ou unanswerable (3, com "evidence": []).
- start e end são posições de carácter no .txt limpo, com o fim exclusivo: texto[start:end] == text.
- sha1 é o SHA-1 dos bytes do .txt do documento (UTF-8, LF), para se saber se o .txt mudou depois.
- group (opcional): trechos com o mesmo número são alternativos e basta um; se um trecho tem group, todos têm.

Uso, na raiz do repositório:
  python scripts/perguntas_E1.py procura "garrafa de plástico" OAU      procura na base, com contexto
  python scripts/perguntas_E1.py procura CP meta --inteira              só palavras inteiras (sem «metal», «metade»)
  python scripts/perguntas_E1.py completa tests/questions_E1.jsonl     preenche start, end e sha1 a partir do text
  python scripts/perguntas_E1.py valida tests/questions_E1.jsonl       confirma as regras do grupo

O «procura» não distingue maiúsculas nem acentos («deposito» encontra «depósito») e procura o início
das palavras («trotinete» também encontra «trotinetes»). Mostra quantas vezes cada termo aparece e em
que documentos, e depois cada ocorrência com o contexto (até --max por termo).

No "completa", basta escrever em cada trecho o doc_id e o text copiado do .txt; o script encontra a posição.
Se o mesmo texto aparecer mais de uma vez no documento, escolhe a ocorrência que está mais perto do start
que lá estiver; se não houver start, avisa e mostra as posições.
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TIPOS = {"factual": 8, "multi_doc": 4, "unanswerable": 3}
CAMPOS = ["id", "type", "subtopic", "question", "reference_answer", "evidence", "notes"]
OBRIGATORIOS = ["id", "type", "question", "reference_answer", "evidence"]
MAX_TRECHO = 500  # caracteres (regra do grupo: de preferência menos de 500)


def le_catalogo(caminho):
    docs = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if linha.strip():
            c = json.loads(linha)
            docs[c["doc_id"]] = RAIZ / c["text_file"]
    return docs


class Base:
    """Os .txt da base, lidos uma vez, com o texto exato (sem converter fins de linha) e o SHA-1."""

    def __init__(self, catalogo):
        self.ficheiros = le_catalogo(catalogo)
        self._cache = {}

    def doc(self, doc_id):
        if doc_id not in self._cache:
            caminho = self.ficheiros[doc_id]
            dados = caminho.read_bytes()
            self._cache[doc_id] = (dados.decode("utf-8"), hashlib.sha1(dados).hexdigest())
        return self._cache[doc_id]


def le_perguntas(caminho):
    perguntas = []
    for n, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
        if not linha.strip():
            continue
        try:
            perguntas.append(json.loads(linha))
        except json.JSONDecodeError as e:
            sys.exit(f"{caminho.name}, linha {n}: JSON inválido ({e})")
    return perguntas


def grava_perguntas(caminho, perguntas):
    linhas = []
    for p in perguntas:
        ordenada = {k: p[k] for k in CAMPOS if k in p}
        ordenada.update({k: v for k, v in p.items() if k not in ordenada})
        ordenada["evidence"] = [{k: e[k] for k in ("doc_id", "start", "end", "sha1", "text", "group") if k in e}
                                | {k: v for k, v in e.items() if k not in ("doc_id", "start", "end", "sha1", "text", "group")}
                                for e in ordenada.get("evidence", [])]
        linhas.append(unicodedata.normalize("NFC", json.dumps(ordenada, ensure_ascii=False)))
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linhas) + "\n")


def posicoes(texto, trecho):
    return [m.start() for m in re.finditer(re.escape(trecho), texto)]


def dobra(s):
    """Minúsculas e sem acentos, carácter a carácter, para as posições continuarem a bater com o texto original."""
    return "".join(unicodedata.normalize("NFD", c)[0].lower()[:1] or c for c in s)


def procura(base, termos, contexto=90, inteira=False, maximo=40):
    for termo in termos:
        corpo = r"\s+".join(map(re.escape, dobra(termo).split()))
        rx = re.compile(r"(?<!\w)" + corpo + (r"(?!\w)" if inteira else ""))
        achados = []
        for doc_id in sorted(base.ficheiros):
            texto, _ = base.doc(doc_id)
            achados += [(doc_id, m.start(), m.end()) for m in rx.finditer(dobra(texto))]
        por_doc = Counter(d for d, _, _ in achados)
        lista = ", ".join(f"{d} ({n})" for d, n in sorted(por_doc.items()))
        print(f"=== «{termo}»: {len(achados)} ocorrências em {len(por_doc)} documentos" + (f": {lista}" if lista else ""))
        for doc_id, s, f_ in achados[:maximo]:
            texto, _ = base.doc(doc_id)
            a, b = max(0, s - contexto), min(len(texto), f_ + contexto)
            print(f"  {doc_id} [{s}, {f_})  …{texto[a:b].replace(chr(10), ' ⏎ ')}…")
        if len(achados) > maximo:
            print(f"  … e mais {len(achados) - maximo} (usa --max para ver mais)")
        print()


def completa(base, caminho):
    perguntas = le_perguntas(caminho)
    problemas = 0
    for p in perguntas:
        for i, e in enumerate(p.get("evidence", []), start=1):
            onde = f"{p.get('id', '?')}, trecho {i}"
            if e.get("doc_id") not in base.ficheiros:
                print(f"  {onde}: o doc_id {e.get('doc_id')!r} não está no catálogo")
                problemas += 1
                continue
            texto, sha1 = base.doc(e["doc_id"])
            trecho = unicodedata.normalize("NFC", e.get("text", ""))
            if not trecho:
                print(f"  {onde}: falta o text")
                problemas += 1
                continue
            achados = posicoes(texto, trecho)
            if not achados:
                print(f"  {onde}: o text não aparece tal e qual em {e['doc_id']} (copia-o do .txt, com a mesma pontuação e quebras)")
                problemas += 1
                continue
            if len(achados) > 1 and not isinstance(e.get("start"), int):
                print(f"  {onde}: o text aparece {len(achados)} vezes em {e['doc_id']} (posições {achados[:8]}); "
                      "põe o start da que queres ou alarga o trecho")
                problemas += 1
                continue
            alvo = e["start"] if isinstance(e.get("start"), int) else achados[0]
            inicio = min(achados, key=lambda x: abs(x - alvo))
            e.update({"text": trecho, "start": inicio, "end": inicio + len(trecho), "sha1": sha1})
    grava_perguntas(caminho, perguntas)
    print(f"{caminho.name}: {len(perguntas)} perguntas gravadas" + (f"; {problemas} trechos por resolver" if problemas else "; todos os trechos com posição"))
    return problemas


def valida(base, caminho):
    perguntas = le_perguntas(caminho)
    erros, avisos = [], []
    ids = [p.get("id") for p in perguntas]
    for k, n in Counter(ids).items():
        if n > 1:
            erros.append(f"id repetido: {k}")
    if len(perguntas) != 15:
        erros.append(f"há {len(perguntas)} perguntas (devem ser 15)")
    esperados = [f"E1-{i:02d}" for i in range(1, 16)]
    if sorted(i for i in ids if i) != esperados:
        avisos.append(f"os ids não são exatamente {esperados[0]} … {esperados[-1]}")
    tipos = Counter(p.get("type") for p in perguntas)
    for t, n in TIPOS.items():
        if tipos.get(t, 0) != n:
            erros.append(f"{t}: {tipos.get(t, 0)} perguntas (devem ser {n})")
    for t in tipos:
        if t not in TIPOS:
            erros.append(f"type desconhecido: {t!r}")

    for p in perguntas:
        pid = p.get("id", "?")
        for campo in OBRIGATORIOS:
            if campo not in p:
                erros.append(f"{pid}: falta o campo {campo}")
        for campo in ("question", "reference_answer", "subtopic", "notes"):
            v = p.get(campo)
            if v is not None and (not isinstance(v, str) or (campo in ("question", "reference_answer") and not v.strip())):
                erros.append(f"{pid}: {campo} tem de ser texto não vazio")
            elif isinstance(v, str) and unicodedata.normalize("NFC", v) != v:
                erros.append(f"{pid}: {campo} não está em NFC")
        ev = p.get("evidence", [])
        if not isinstance(ev, list):
            erros.append(f"{pid}: evidence tem de ser uma lista")
            continue
        if p.get("type") == "unanswerable":
            if ev:
                erros.append(f"{pid}: unanswerable tem de ter evidence vazia")
            continue
        if not ev:
            erros.append(f"{pid}: falta a evidence")
            continue
        com_grupo = [e for e in ev if "group" in e]
        if com_grupo and len(com_grupo) != len(ev):
            erros.append(f"{pid}: se um trecho tem group, todos têm de ter")
        if com_grupo and not all(isinstance(e["group"], int) and e["group"] >= 1 for e in ev):
            erros.append(f"{pid}: group tem de ser um inteiro a partir de 1")
        docs = {e.get("doc_id") for e in ev}
        if p.get("type") == "multi_doc":
            if len(docs) < 2:
                erros.append(f"{pid}: multi_doc precisa de trechos de pelo menos 2 documentos")
            if com_grupo:
                docs_por_grupo = {}
                for e in ev:
                    docs_por_grupo.setdefault(e["group"], set()).add(e.get("doc_id"))
                if len(docs_por_grupo) < 2:
                    erros.append(f"{pid}: multi_doc com group precisa de pelo menos 2 grupos")
        for i, e in enumerate(ev, start=1):
            onde = f"{pid}, trecho {i}"
            doc_id = e.get("doc_id")
            if doc_id not in base.ficheiros:
                erros.append(f"{onde}: doc_id {doc_id!r} não está no catálogo")
                continue
            texto, sha1 = base.doc(doc_id)
            s, f_ = e.get("start"), e.get("end")
            if not (isinstance(s, int) and isinstance(f_, int) and 0 <= s < f_ <= len(texto)):
                erros.append(f"{onde}: start/end inválidos ({s}, {f_}); corre o «completa»")
                continue
            if texto[s:f_] != e.get("text"):
                erros.append(f"{onde}: texto[{s}:{f_}] não é igual ao text")
            if e.get("sha1") != sha1:
                erros.append(f"{onde}: o sha1 não bate com o {doc_id} atual (o .txt mudou?); corre o «completa»")
            n = f_ - s
            if n > MAX_TRECHO:
                avisos.append(f"{onde}: trecho com {n} caracteres (de preferência menos de {MAX_TRECHO})")
            if s > 0 and texto[s - 1].isalnum() and texto[s].isalnum():
                avisos.append(f"{onde}: o trecho começa a meio de uma palavra")
            if f_ < len(texto) and texto[f_ - 1].isalnum() and texto[f_].isalnum():
                avisos.append(f"{onde}: o trecho acaba a meio de uma palavra")

    for a in avisos:
        print("  aviso:", a)
    for e in erros:
        print("  ERRO:", e)
    resumo = ", ".join(f"{t} {tipos.get(t, 0)}" for t in TIPOS)
    print(f"{caminho.name}: {len(perguntas)} perguntas ({resumo}); {len(erros)} erros, {len(avisos)} avisos")
    return len(erros)


def main():
    ap = argparse.ArgumentParser(description="Escreve e valida as perguntas de teste do E1.")
    ap.add_argument("acao", choices=["procura", "completa", "valida"])
    ap.add_argument("alvos", nargs="+", help="termos a procurar, ou o ficheiro das perguntas")
    ap.add_argument("--catalogo", type=Path, default=RAIZ / "kb/E1/catalog_E1.jsonl")
    ap.add_argument("--contexto", type=int, default=90, help="caracteres de contexto no «procura»")
    ap.add_argument("--inteira", action="store_true", help="no «procura», só palavras inteiras")
    ap.add_argument("--max", type=int, default=40, help="no «procura», ocorrências mostradas por termo")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    base = Base(args.catalogo)
    if args.acao == "procura":
        procura(base, args.alvos, args.contexto, args.inteira, args.max)
    elif args.acao == "completa":
        sys.exit(1 if completa(base, Path(args.alvos[0])) else 0)
    else:
        sys.exit(1 if valida(base, Path(args.alvos[0])) else 0)


if __name__ == "__main__":
    main()
