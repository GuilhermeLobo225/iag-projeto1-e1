#!/usr/bin/env python3
"""Converte os PDF de kb/E1/raw em texto limpo (.txt) e conta as palavras.

Para cada PDF, o script:
  1. extrai o texto página a página com o PyMuPDF;
  2. limpa o texto: tira cabeçalhos e rodapés repetidos, números de página, linhas de índice,
     texto rodado e notas de alteração da legislação consolidada; junta as linhas em parágrafos
     e as palavras partidas no fim da linha; corrige ligaduras e acentos soltos;
  3. grava em kb/E1/text/<doc_id>.txt só as partes definidas em scripts/partes_E1.json,
     pela ordem do documento e separadas por uma linha em branco (UTF-8, NFC, fins de linha LF);
  4. escreve kb/E1/catalog_E1.jsonl e kb/E1/relatorio_palavras.csv, e mostra as contagens.
     No catálogo, "parts" é null quando o documento entra inteiro; senão, é um texto com as páginas
     e o porquê do corte («páginas 6-46: ...»), tirado do campo "motivo_partes" do partes_E1.json;
  5. copia o PDF de cada documento da base para kb/E1/pdf/<doc_id>.pdf (o mesmo nome do .txt),
     para conferires lado a lado; tira dessa pasta as cópias de PDF que já não entram.

Uso, na raiz do repositório:
  python scripts/pdf_para_txt.py              só as partes do núcleo
  python scripts/pdf_para_txt.py --opcional   núcleo e partes opcionais
  python scripts/pdf_para_txt.py --completo   guarda também cada PDF inteiro em kb/E1/completo/
  python scripts/pdf_para_txt.py --ocr        faz OCR dos PDF em imagem (precisa do Tesseract com português)
  python scripts/pdf_para_txt.py --forcar     substitui os .txt que já existam e tenham mudado
  python scripts/pdf_para_txt.py --limites    mostra o início e o fim de cada parte, para conferir os cortes
  python scripts/pdf_para_txt.py --cabecalhos mostra as linhas que saíram como cabeçalho ou rodapé
  python scripts/pdf_para_txt.py --so 001,105 só mostra esses PDF, sem gravar nada (para testar as partes)

As páginas de partes_E1.json são as do PDF (a primeira é a 1), não as impressas. Cada parte é
[página_inicial, página_final, marcador_inicial, marcador_final]: o texto começa no marcador inicial
e acaba antes do marcador final (null = página inteira).
Os PDF em imagem («ocr»: true) usam o texto de kb/E1/ocr/<n.º>.txt, que o --ocr cria e que podes
corrigir à mão; nesses documentos entra o texto todo do OCR.
As palavras contam-se com len(texto.split()), como combinado no grupo.
Precisa de Python 3.9 ou mais recente e do PyMuPDF (pip install pymupdf).
"""
import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        sys.exit("Falta o PyMuPDF. Instala com: pip install pymupdf")

AREA = "E1"  # como no exemplo de catálogo do grupo
RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- caracteres

TROCAS = {
    **dict.fromkeys(map(ord, "\u00a0\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u202f\u205f\u3000"), " "),
    **dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff"), None),
    ord("\u2010"): "-", ord("\u2011"): "-", ord("\u2212"): "-",
    ord("\ufb00"): "ff", ord("\ufb01"): "fi", ord("\ufb02"): "fl", ord("\ufb03"): "ffi", ord("\ufb04"): "ffl",
    ord("\ufb05"): "st", ord("\ufb06"): "st",
}
# Acentos soltos dos PDF feitos em LaTeX («Guimar˜aes», «V´ıtor», «c¸»).
ACENTOS = {"\u00b4": "\u0301", "\u02dc": "\u0303", "`": "\u0300", "\u02c6": "\u0302", "\u00a8": "\u0308"}
RX_ACENTO = re.compile(r"([\u00b4\u02dc`\u02c6\u00a8]) ?([A-Za-z\u0131])")
RX_CEDILHA = re.compile(r"\u00b8 ?([cC])|([cC]) ?\u00b8")
RX_HIFEN_DR = re.compile(r"(?<=\w) -(?=\w)")  # «decreto -lei», «102 -D/2020» do Diário da República


def limpa_chars(s):
    s = s.translate(TROCAS)
    s = "".join("•" if "\ue000" <= c <= "\uf8ff" else c for c in s)  # símbolos de fontes (marcadores)
    s = "".join(c for c in s if c in "\t\n\u00ad" or unicodedata.category(c)[0] != "C")
    s = re.sub(r"(?m)^\ufffd", "•", s)  # marcadores de lista sem código Unicode
    return unicodedata.normalize("NFC", s)


def corrige_acentos(s):
    s = RX_ACENTO.sub(lambda m: ("i" if m.group(2) == "\u0131" else m.group(2)) + ACENTOS[m.group(1)], s)
    return unicodedata.normalize("NFC", RX_CEDILHA.sub(lambda m: (m.group(1) or m.group(2)) + "\u0327", s))


# ---------------------------------------------------------------- extração

def extrai_pagina(page):
    """Blocos da página e altura útil; cada bloco é uma lista de linhas {t, x0, y0, x1, y1}.

    Fica só o texto na direção dominante da página (nas tabelas em paisagem o texto corre na vertical)
    e as coordenadas passam para o sentido de leitura. O texto noutras direções (eixos de gráficos,
    carimbos) é ignorado.
    """
    brutos, peso = [], Counter()
    for b in page.get_text("dict", flags=pymupdf.TEXT_MEDIABOX_CLIP)["blocks"]:
        if b.get("type", 0) != 0:
            continue
        linhas = []
        for l in b["lines"]:
            dx, dy = l["dir"]
            if max(abs(dx), abs(dy)) < 0.9:  # texto oblíquo
                continue
            t = limpa_chars("".join(s["text"] for s in l["spans"])).strip()
            if t:
                d = (round(dx), round(dy))
                linhas.append((d, l["bbox"], t))
                peso[d] += len(t)
        if linhas:
            brutos.append(linhas)
    r = page.rect * page.derotation_matrix
    if not peso:
        return [], abs(r.y1 - r.y0)
    dx, dy = peso.most_common(1)[0][0]

    def roda(x, y):
        return x * dx + y * dy, -x * dy + y * dx

    cantos = [roda(x, y) for x in (r.x0, r.x1) for y in (r.y0, r.y1)]
    ox, oy = min(c[0] for c in cantos), min(c[1] for c in cantos)
    altura = max(c[1] for c in cantos) - oy
    blocos = []
    for linhas in brutos:
        bl = []
        for d, (x0, y0, x1, y1), t in linhas:
            if d != (dx, dy):
                continue
            pts = [roda(x, y) for x in (x0, x1) for y in (y0, y1)]
            bl.append({"t": t, "x0": min(p[0] for p in pts) - ox, "y0": min(p[1] for p in pts) - oy,
                       "x1": max(p[0] for p in pts) - ox, "y1": max(p[1] for p in pts) - oy})
        if bl:
            blocos.append(bl)
    return blocos, altura


# ---------------------------------------------------------------- cabeçalhos, rodapés e lixo

RX_PAGINA = re.compile(r"^[\s\-–—|·•(\[]*(p[áa]g(ina)?\.?\s*)?\d{1,4}(\s*(/|de|of)\s*\d{1,4})?[\s\-–—|·•)\]]*$", re.I)
RX_TITULO_LEGAL = re.compile(r"^(artigo|cap[íi]tulo|sec[çc][ãa]o|subsec[çc][ãa]o|t[íi]tulo|anexo|parte)\b", re.I)
RX_LIXO = re.compile(r"^([\s_\-–—.·=~|/\\]+|.{2,}?(\s?\.){4,}\s*\d{1,4}|.{2,}?\u2026{2,}\s*\d{1,4}|\d{6,})$")
ZONA, ZONA_LARGA = 0.12, 0.20  # fração da altura da página, em cima e em baixo


def chave(t):
    t = re.sub(r"(?<!\d)\d{1,3}(?!\d)", "#", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def zona(l, h):
    """2 = margem estreita, 1 = margem larga, 0 = corpo da página."""
    if l["y1"] <= ZONA * h or l["y0"] >= (1 - ZONA) * h:
        return 2
    if l["y1"] <= ZONA_LARGA * h or l["y0"] >= (1 - ZONA_LARGA) * h:
        return 1
    return 0


def tira_cabecalhos(paginas, alturas):
    """Tira os números de página, as linhas de lixo e as linhas repetidas nas margens de muitas páginas.

    De cada linha repetida fica só a primeira ocorrência (um título ou um contacto no rodapé não se perde).
    As repetidas com pelo menos duas palavras saem também do corpo da página («Voltar ao Índice»).
    """
    n = len(paginas)
    estreita, larga = Counter(), Counter()
    for blocos, h in zip(paginas, alturas):
        e, g = set(), set()
        for b in blocos:
            for l in b:
                z = zona(l, h)
                if z:
                    k = chave(l["t"])
                    g.add(k)
                    if z == 2:
                        e.add(k)
        estreita.update(e)
        larga.update(g)

    def conta(k):  # cabeçalho tem letras e não é um título de artigo ou capítulo (os números de tabela ficam)
        return re.search(r"[^\W\d_]", k) and not (RX_TITULO_LEGAL.match(k) and len(k.split()) <= 4)

    if n >= 3:
        rep_estreita = {k for k, c in estreita.items() if c >= max(3, 0.3 * n) and conta(k)}
        rep_larga = {k for k, c in larga.items() if c >= max(3, 0.6 * n) and conta(k)}
    else:  # 2 páginas: só o que se repete nas duas e tem letras
        rep_estreita = {k for k, c in estreita.items() if n == 2 and c == 2 and re.search(r"[^\W\d_]{3}", k) and conta(k)}
        rep_larga = set()
    em_todo_lado = {k for k in rep_estreita | rep_larga if len(k.split()) >= 2 and len(re.findall(r"[^\W\d_]", k)) >= 6}
    removidas, vistas, novas = Counter(), set(), []
    for blocos, h in zip(paginas, alturas):
        por_y = sorted((l for b in blocos for l in b), key=lambda l: l["y0"])
        pontas = {id(l) for l in por_y[:2] + por_y[-2:]}  # o número de página é a primeira ou a última linha
        nb = []
        for b in blocos:
            fica = []
            for l in b:
                z, k = zona(l, h), chave(l["t"])
                repetida = (z == 2 and k in rep_estreita) or (z and k in rep_larga) or k in em_todo_lado
                pagina = z == 2 and id(l) in pontas and RX_PAGINA.match(l["t"])
                if RX_LIXO.match(l["t"]) or pagina or (repetida and k in vistas):
                    removidas[k] += 1
                    continue
                if repetida:
                    vistas.add(k)
                fica.append(l)
            if fica:
                nb.append(fica)
        novas.append(nb)
    return novas, removidas


# ---------------------------------------------------------------- parágrafos

MARCAS = "•▪●◦■□○►➢✓✔➤◆◇*·"
RX_ITEM = re.compile(r"^([•▪●◦■□○►➢✓✔➤◆◇*·]|[-–—]\s|\(?\d{1,3}(\.\d{1,3})*[.)]\s|\d{1,3}\s?[—–]\s|\(?[a-z]\)\s|\(?[ivx]{1,4}\)\s)")
RX_FIM_FRASE = re.compile(r"[.:;!?][\"'»”’)\]]*$")
RX_ANOTACAO = re.compile(r"^(Alterações|(Alterado|Aditado|Retificado|Revogado|Republicado|Renumerado)\s+pelo/a\b)")
LIGACAO = {"a", "o", "as", "os", "e", "ou", "de", "da", "do", "das", "dos", "em", "na", "no", "nas", "nos", "para", "por",
           "pela", "pelo", "com", "sem", "que", "um", "uma", "à", "ao", "às", "aos", "entre", "sobre"}
CLITICOS = {"se", "me", "te", "lhe", "lhes", "o", "a", "os", "as", "lo", "la", "los", "las", "no", "na", "nos", "nas", "vos"}
PREFIXOS = {"pré", "pós", "pró", "ex", "vice", "recém", "além", "aquém", "sem", "bem", "mal", "grã", "grão"}
RX_PALAVRA = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")


def mesma_linha(a, b):
    sob = min(a["y1"], b["y1"]) - max(a["y0"], b["y0"])
    return sob > 0.5 * min(a["y1"] - a["y0"], b["y1"] - b["y0"]) and b["x0"] >= a["x1"] - 1


RX_MARCA_LISTA = re.compile(r"^(\(?\d{1,3}(\.\d{1,3})*[.)º]?|\(?[a-zA-Z][.)]|[ivxIVX]{1,4}[.)]|[•▪●◦■□○►➢✓✔➤◆◇*·\-–—])$")
RX_NUMERO = re.compile(r"^[-+]?\d{1,3}(?:[ .]\d{3})*(?:,\d+)?\s?%?$")


def junta_horizontal(a, b):
    grande = b["x0"] - a["x1"] > 1.5 * (a["y1"] - a["y0"])  # espaço grande = outra célula da tabela
    sep = "\t" if grande and not RX_MARCA_LISTA.match(a["t"]) else " "
    return {"t": a["t"] + sep + b["t"], "x0": a["x0"], "y0": min(a["y0"], b["y0"]), "x1": b["x1"], "y1": max(a["y1"], b["y1"])}


def linhas_visuais(blocos):
    """Junta as linhas que estão à mesma altura (no bloco e em blocos seguidos de uma linha, como células de tabela)."""
    out = []
    for b in blocos:
        vis = []
        for l in b:
            if vis and mesma_linha(vis[-1], l):
                vis[-1] = junta_horizontal(vis[-1], l)
            else:
                vis.append(l)
        if out and len(vis) == 1 and len(out[-1]) == 1 and mesma_linha(out[-1][0], vis[0]):
            out[-1][0] = junta_horizontal(out[-1][0], vis[0])
        else:
            out.append(vis)
    return out


def cola(a, b, vocab):
    """Junta duas linhas: tira o hífen de translineação quando a palavra existe inteira no corpus."""
    if len(a) <= 2 and a[-1] in MARCAS + "-–—":
        return a + " " + b
    if a.endswith("\u00ad"):
        return a[:-1] + b
    if a.endswith("-"):
        antes = a[:-1]
        if antes.endswith(" "):  # «decreto -» + «lei»
            return antes.rstrip() + "-" + b
        if not b[:1].islower():  # «Decreto-» + «Lei», «COVID-» + «19»
            return a + b
        esq, dir_ = re.search(r"[^\W\d_]+$", antes), RX_PALAVRA.match(b)
        if esq and dir_:
            e, d = esq.group(0).lower(), dir_.group(0).lower()
            junto, hifen = e + d.split("-")[0], e + "-" + d
            if vocab[junto] > vocab[hifen]:
                return antes + b
            if vocab[hifen] or (d.split("-")[0] in CLITICOS and vocab[e]) or e in PREFIXOS:
                return a + b
        return antes + b
    return a + " " + b


def quebra(a, prev, b, xmax, largura):
    """Decide se a linha b começa um parágrafo novo."""
    if len(a) <= 2 and a[-1] in MARCAS + "-–—":
        return False
    if RX_ITEM.match(b) or "\t" in b or "\t" in prev["t"]:  # itens de lista e linhas de tabela ficam sozinhos
        return True
    if a.rsplit(None, 1)[-1] in LIGACAO:  # acaba em «de», «e», «ou»...: a frase continua
        return False
    curta = prev["x1"] < xmax - 0.15 * largura
    novo = b[:1].isupper() or b[:1].isdigit() or b[:1] in "«\"“(["
    if RX_FIM_FRASE.search(a) and (curta or novo):
        return True
    if curta and novo:
        return True
    return a.isupper() and len(a) < 120 and not b.isupper()


def continua(a, b):
    """O parágrafo b (início de bloco ou de página) continua a frase de a?"""
    if len(a) <= 2 and a[-1] in MARCAS + "-–—":
        return True
    if RX_ITEM.match(b):
        return False
    if a.endswith(("-", "\u00ad", ",")) or a.rsplit(None, 1)[-1] in LIGACAO:
        return True
    return not RX_FIM_FRASE.search(a) and b[:1].islower()


def paragrafos(blocos, vocab):
    pars = []
    for vis in linhas_visuais(blocos):
        xmax, xmin = max(l["x1"] for l in vis), min(l["x0"] for l in vis)
        largura = max(xmax - xmin, 1.0)
        atual = vis[0]["t"]
        if pars and continua(pars[-1], atual):
            atual = cola(pars.pop(), atual, vocab)
        for prev, l in zip(vis, vis[1:]):
            if quebra(atual, prev, l["t"], xmax, largura):
                pars.append(atual)
                atual = l["t"]
            else:
                atual = cola(atual, l["t"], vocab)
        pars.append(atual)
    pars = [f for f in (final(p) for p in pars) if f and not RX_ANOTACAO.match(f) and f.strip(MARCAS + "-–— ")]
    return tira_eixos(pars)


def valor(x):
    return float(x.replace(" ", "").replace(".", "").replace(",", ".").rstrip("%").strip())


def progressao(cel):
    """Números em progressão aritmética (marcas de eixo: 0%, 20%, 40%...), sem contar sequências de anos."""
    if len(cel) < 4 or not all(RX_NUMERO.match(c) for c in cel):
        return False
    v = [valor(c) for c in cel]
    d = {round(b - a, 6) for a, b in zip(v, v[1:])}
    anos = all(1900 <= x <= 2100 for x in v)
    return len(d) == 1 and 0 not in d and not anos


def tira_eixos(pars):
    """Tira as marcas de eixo dos gráficos, em coluna (uma por linha) ou em linha (separadas por tabulação)."""
    out, i = [], 0
    while i < len(pars):
        j = i
        while j < len(pars) and RX_NUMERO.match(pars[j]):
            j += 1
        if j - i >= 4 and progressao(pars[i:j]):
            i = j
            continue
        if progressao(pars[i].split("\t")):
            i += 1
            continue
        out.append(pars[i])
        i += 1
    return out


def final(p):
    p = p.replace("\u00ad", "")
    p = re.sub(r" {2,}", " ", p)
    p = re.sub(r" *\t[ \t]*", "\t", p)
    return p.strip(" \t")


def junta_paginas(listas, vocab):
    out = []
    for pars in listas:
        for i, p in enumerate(pars):
            if out and i == 0 and continua(out[-1], p):
                out[-1] = cola(out[-1], p, vocab)
            else:
                out.append(p)
    return out


# ---------------------------------------------------------------- partes

def rx_marcador(m):
    rx = r"\s+".join(re.escape(p) for p in m.split())
    if m[:1].isalnum():
        rx = r"(?<!\w)" + rx
    if m[-1:].isalnum():
        rx += r"(?!\w)"
    return re.compile(rx)


def corta(pars, marcador, inicio):
    """Corta a lista de parágrafos no marcador; None se o marcador não aparecer."""
    texto = "\n".join(pars)
    m = rx_marcador(marcador).search(texto)
    if not m:
        return None
    texto = texto[m.start():] if inicio else texto[:m.start()]
    return [p for p in (final(x) for x in texto.split("\n")) if p]


def descreve(parte):
    a, b, mi, mf = parte
    s = f"pp. {a}-{b}" if a != b else f"p. {a}"
    if mi and mf:
        s += f" (de «{mi}» até antes de «{mf}»)"
    elif mi:
        s += f" (a partir de «{mi}»)"
    elif mf:
        s += f" (até antes de «{mf}»)"
    return s


def paginas_partes(partes):
    """Páginas das partes no formato do grupo: «páginas 9-58,149-152» (intervalos seguidos juntam-se)."""
    juntos = []
    for a, b, *_ in sorted(partes, key=lambda p: (p[0], p[1])):
        if juntos and a <= juntos[-1][1] + 1:
            juntos[-1][1] = max(juntos[-1][1], b)
        else:
            juntos.append([a, b])
    texto = ",".join(f"{a}-{b}" if a != b else f"{a}" for a, b in juntos)
    return ("página " if len(juntos) == 1 and juntos[0][0] == juntos[0][1] else "páginas ") + texto


def texto_parte(paginas, parte, vocab, avisos, nome):
    a, b, mi, mf = parte
    if not (1 <= a <= b <= len(paginas)):
        avisos.append(f"{nome}: parte {descreve(parte)} fora do PDF ({len(paginas)} páginas)")
        return ""
    listas = [list(paginas[p - 1]) for p in range(a, b + 1)]
    for p, lst in zip(range(a, b + 1), listas):
        if not lst:
            avisos.append(f"{nome}: a p. {p} não tem texto (imagem?)")
    if mi:
        cortada = corta(listas[0], mi, True)
        if cortada is None:
            avisos.append(f"{nome}: não encontrei «{mi}» na p. {a}")
            return ""
        listas[0] = cortada
    if mf:
        cortada = corta(listas[-1], mf, False)
        if cortada is None:
            avisos.append(f"{nome}: não encontrei «{mf}» na p. {b}")
            return ""
        listas[-1] = cortada
    return "\n".join(junta_paginas(listas, vocab)).strip()


# ---------------------------------------------------------------- OCR

def tesseract_exe():
    exe = shutil.which("tesseract")
    if not exe:
        for p in (r"C:\Program Files\Tesseract-OCR\tesseract.exe", r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"):
            if Path(p).exists():
                return p
    return exe


def faz_ocr(pdf, destino, tessdata):
    exe = tesseract_exe()
    if not exe:
        return "não encontrei o Tesseract"
    extra = ["--tessdata-dir", str(tessdata)] if tessdata else []
    textos = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, page in enumerate(pymupdf.open(pdf), start=1):
            img = Path(tmp) / f"p{i}.png"
            page.get_pixmap(dpi=300).save(img)
            r = subprocess.run([exe, str(img), "stdout", "-l", "por", *extra], capture_output=True, text=True, encoding="utf-8")
            if r.returncode != 0:
                return "o Tesseract falhou: " + r.stderr.strip()[-300:]
            textos.append(r.stdout.replace("\f", "").strip())
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(unicodedata.normalize("NFC", "\n\n".join(textos)) + "\n", encoding="utf-8", newline="\n")
    return None


def paragrafos_ocr(texto, vocab):
    """Texto de OCR: parágrafos separados por linha em branco; as linhas de cada um juntam-se."""
    pars = []
    for bloco in re.split(r"\n\s*\n", limpa_chars(texto.replace("\r\n", "\n"))):
        linhas = [l.strip() for l in bloco.split("\n") if l.strip() and not RX_LIXO.match(l.strip())]
        if not linhas:
            continue
        atual = linhas[0]
        for l in linhas[1:]:
            if RX_ITEM.match(l):
                pars.append(atual)
                atual = l
            else:
                atual = cola(atual, l, vocab)
        pars.append(atual)
    return [f for f in (final(p) for p in pars) if f]


# ---------------------------------------------------------------- principal

def grava(caminho, texto, forcar):
    """Grava em UTF-8 com LF; não substitui um ficheiro diferente sem --forcar. Devolve o estado."""
    if caminho.exists():
        antigo = caminho.read_text(encoding="utf-8")
        if antigo == texto:
            return "igual"
        if not forcar:
            return "mudou (não substituído: usa --forcar)"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    return "escrito"


def copia_pdf(origem, destino):
    """Copia o PDF original para a pasta dos PDF usados, só se ainda lá não estiver igual."""
    if destino.exists():
        a, b = origem.stat(), destino.stat()
        if a.st_size == b.st_size and int(a.st_mtime) == int(b.st_mtime):
            return
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origem, destino)


def rel(p):
    try:
        return p.resolve().relative_to(RAIZ).as_posix()
    except ValueError:
        return p.as_posix()


def n(x):
    return f"{x:,}".replace(",", " ")


def le_pdfs(config, raw, avisos):
    """1.ª passagem: extrai e limpa as páginas de cada PDF e monta o vocabulário do corpus.

    Também é usada pelo rever_embeddings.py, para os dois scripts partirem o texto da mesma maneira.
    """
    docs, vocab = {}, Counter()
    for d in config:
        pdf = raw / d["ficheiro"]
        if not pdf.exists():
            avisos.append(f"{d['ficheiro']}: não existe em {rel(raw)}")
            continue
        extraidas = [extrai_pagina(p) for p in pymupdf.open(pdf)]
        paginas, alturas = [e[0] for e in extraidas], [e[1] for e in extraidas]
        bruto = " ".join(l["t"] for pg in paginas for b in pg for l in b)
        latex, dr = len(RX_ACENTO.findall(bruto)) >= 5, len(RX_HIFEN_DR.findall(bruto)) >= 10
        for pg in paginas:
            for b in pg:
                for l in b:
                    if latex:
                        l["t"] = corrige_acentos(l["t"])
                    if dr:
                        l["t"] = RX_HIFEN_DR.sub("-", l["t"])
        paginas, removidas = tira_cabecalhos(paginas, alturas)
        for pg in paginas:
            for b in pg:
                for l in b:
                    vocab.update(RX_PALAVRA.findall(l["t"].lower())[1:-1])  # sem as pontas da linha
        docs[d["ficheiro"]] = {"paginas": paginas, "removidas": removidas, "n_pag": len(alturas)}
    return docs, vocab


def main():
    ap = argparse.ArgumentParser(description="Converte os PDF de kb/E1/raw em .txt limpos e conta as palavras.")
    ap.add_argument("--raw", type=Path, default=RAIZ / "kb/E1/raw", help="pasta com os PDF (001.pdf, 002.pdf, ...)")
    ap.add_argument("--partes", type=Path, default=RAIZ / "scripts/partes_E1.json", help="metadados e partes de cada PDF")
    ap.add_argument("--saida", type=Path, default=RAIZ / "kb/E1/text", help="pasta dos .txt da base de conhecimento")
    ap.add_argument("--catalogo", type=Path, default=RAIZ / "kb/E1/catalog_E1.jsonl")
    ap.add_argument("--relatorio", type=Path, default=RAIZ / "kb/E1/relatorio_palavras.csv")
    ap.add_argument("--ocr-dir", type=Path, default=RAIZ / "kb/E1/ocr", help="texto dos PDF em imagem (um .txt por PDF)")
    ap.add_argument("--completo-dir", type=Path, default=RAIZ / "kb/E1/completo")
    ap.add_argument("--pdf-dir", type=Path, default=RAIZ / "kb/E1/pdf", help="cópia dos PDF que entram na base, com o nome do .txt")
    ap.add_argument("--opcional", action="store_true", help="inclui também as partes opcionais")
    ap.add_argument("--completo", action="store_true", help="grava também cada PDF inteiro (com marcas de página)")
    ap.add_argument("--ocr", action="store_true", help="faz OCR dos PDF em imagem que ainda não tenham texto")
    ap.add_argument("--tessdata", type=Path, help="pasta com por.traineddata, se o Tesseract não a encontrar")
    ap.add_argument("--forcar", action="store_true", help="substitui .txt existentes que tenham mudado")
    ap.add_argument("--limites", action="store_true", help="mostra o início e o fim de cada parte")
    ap.add_argument("--cabecalhos", action="store_true", help="mostra as linhas tiradas como cabeçalho ou rodapé")
    ap.add_argument("--so", help="só mostra estes PDF (ex.: 001,105), sem gravar nada")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):  # na consola do Windows, caracteres sem código não rebentam o print
        sys.stdout.reconfigure(errors="replace")

    config = json.loads(args.partes.read_text(encoding="utf-8"))
    if args.so:
        quais = {f"{x.strip()}.pdf" if not x.strip().endswith(".pdf") else x.strip() for x in args.so.split(",")}
        config = [d for d in config if d["ficheiro"] in quais]
    em_config = {d["ficheiro"] for d in config}
    for pdf in sorted(args.raw.glob("*.pdf")):
        if pdf.name not in em_config and not args.so:
            print(f"Aviso: {pdf.name} não está em {args.partes.name}; foi ignorado.")

    # 1.ª passagem: extrair todas as páginas e montar o vocabulário do corpus
    avisos = []
    docs, vocab = le_pdfs(config, args.raw, avisos)

    # 2.ª passagem: parágrafos, partes, ficheiros
    linhas_rel, catalogo, pdfs_usados = [], [], set()
    tot = Counter()
    for d in config:
        nome, k = d["ficheiro"], d["ficheiro"][:-4]
        if nome not in docs:
            continue
        info = docs[nome]
        paginas = [paragrafos(pg, vocab) for pg in info["paginas"]]
        nucleo = [list(p) for p in d["nucleo"]]
        opcional = [list(p) for p in d["opcional"]]
        estado = ""
        if d["ocr"]:
            fich_ocr = args.ocr_dir / f"{k}.txt"
            if not fich_ocr.exists() and args.ocr and not d["excluir"]:
                erro = faz_ocr(args.raw / nome, fich_ocr, args.tessdata)
                if erro:
                    avisos.append(f"{nome}: OCR não feito ({erro})")
            if fich_ocr.exists():
                paginas = [paragrafos_ocr(fich_ocr.read_text(encoding="utf-8"), vocab)]
                nucleo = [[1, 1, None, None]] if nucleo else []
                opcional = [[1, 1, None, None]] if opcional and not nucleo else []
            elif not d["excluir"]:
                estado = f"falta o OCR (usa --ocr ou cria {rel(fich_ocr)})"
        palavras_pdf = sum(len(" ".join(p).split()) for p in paginas)

        textos = {}
        for tipo, partes in (("nucleo", nucleo), ("opcional", opcional)):
            for parte in partes:
                textos[(tipo, tuple(parte))] = "" if estado else texto_parte(paginas, parte, vocab, avisos, nome)
        pal = {t: sum(len(x.split()) for (tt, _), x in textos.items() if tt == t) for t in ("nucleo", "opcional")}

        usar = [] if d["excluir"] or estado else [("nucleo", p) for p in nucleo] + ([("opcional", p) for p in opcional] if args.opcional else [])
        usar.sort(key=lambda tp: (tp[1][0], tp[1][1]))
        corpo = "\n\n".join(x for x in (re.sub(r"\n{2,}", "\n", textos[(t, tuple(p))]) for t, p in usar) if x)
        escritas = len(corpo.split())
        if d["excluir"]:
            estado = "excluído"
        elif not estado and not usar:
            estado = "só tem partes opcionais (usa --opcional)"
        elif not estado and not corpo:
            estado = "sem texto (ver avisos)"
        elif not estado:
            caminho = args.saida / f"{d['doc_id']}.txt"
            estado = grava(caminho, corpo + "\n", args.forcar) if not args.so else "não gravado (--so)"
            linha = {"doc_id": d["doc_id"], "title": d["title"], "entity": d["entity"], "url": d["url"],
                     "access_date": d["access_date"], "area": AREA, "text_file": rel(caminho)}
            inteiro = d["ocr"] or [p for _, p in usar] == [[1, info["n_pag"], None, None]]
            linha["parts"] = None  # regra do grupo: o campo existe sempre e é null quando o documento entra inteiro
            if not inteiro:
                motivo = (d.get("motivo_partes") or "").strip()
                if not motivo:
                    avisos.append(f"{nome}: falta o \"motivo_partes\" no {args.partes.name} (o \"parts\" do catálogo fica só com as páginas)")
                linha["parts"] = paginas_partes([p for _, p in usar]) + (f": {motivo}" if motivo else "")
            catalogo.append(linha)
            if not args.so:
                copia_pdf(args.raw / nome, args.pdf_dir / f"{d['doc_id']}.pdf")
                pdfs_usados.add(f"{d['doc_id']}.pdf")
            tot["docs_escritos"] += 1
            tot["escritas"] += escritas
        if args.completo and not args.so:
            marcado = "\n\n".join(f"[p. {i}]\n" + "\n".join(p) for i, p in enumerate(paginas, start=1))
            grava(args.completo_dir / f"{k}.txt", marcado + "\n", True)
        if args.cabecalhos and info["removidas"]:
            mais = ", ".join(f"«{k[:60]}» ×{c}" for k, c in info["removidas"].most_common(8))
            print(f"  {nome} tirei: {mais}")
        if args.limites and not d["excluir"]:
            for (t, parte), x in textos.items():
                x1 = x.replace("\n", " ⏎ ")
                print(f"  {nome} {t[:3]} {descreve(list(parte))}: {len(x.split())} pal.\n     INÍCIO «{x1[:110]}»\n     FIM    «{x1[-110:]}»")

        tot["pdf"] += 1
        tot["paginas"] += info["n_pag"]
        tot["palavras_pdf"] += palavras_pdf
        if not d["excluir"]:
            tot["nucleo"] += pal["nucleo"]
            tot["opcional"] += pal["opcional"]
            tot["docs_nucleo"] += 1 if pal["nucleo"] else 0
            tot["docs_opcional"] += 1 if pal["opcional"] else 0
        linhas_rel.append({"ficheiro": nome, "doc_id": d["doc_id"], "estado": estado, "paginas": info["n_pag"],
                           "palavras_pdf": palavras_pdf, "palavras_nucleo": pal["nucleo"], "palavras_opcional": pal["opcional"],
                           "palavras_escritas": escritas if estado in ("escrito", "igual") or estado.startswith("mudou") else 0,
                           "partes_nucleo": "; ".join(descreve(p) for p in nucleo) if not d["ocr"] else ("OCR" if nucleo else ""),
                           "partes_opcionais": "; ".join(descreve(p) for p in opcional) if not d["ocr"] else ("OCR" if opcional else ""),
                           "titulo": d["title"], "nota": d["nota"]})
        print(f"{nome}  {info['n_pag']:>4} pág.  PDF {n(palavras_pdf):>8}  núcleo {n(pal['nucleo']):>7}  opcional {n(pal['opcional']):>7}  {estado}")

    # catálogo e relatório
    if args.so:
        print("\n--so: nada foi gravado. Com poucos PDF, a junção de palavras partidas usa menos vocabulário,")
        print("por isso as contagens podem diferir um pouco das de uma corrida completa.")
    else:
        args.catalogo.parent.mkdir(parents=True, exist_ok=True)
        with open(args.catalogo, "w", encoding="utf-8", newline="\n") as f:
            for c in catalogo:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        args.relatorio.parent.mkdir(parents=True, exist_ok=True)
        with open(args.relatorio, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas_rel[0]) if linhas_rel else ["ficheiro"], delimiter=";")
            w.writeheader()
            w.writerows(linhas_rel)
        if args.pdf_dir.exists():  # as cópias de PDF que já não entram na base saem da pasta
            for velho in args.pdf_dir.glob(f"{AREA}-*.pdf"):
                if velho.name not in pdfs_usados:
                    velho.unlink()
        na_base = {c["text_file"].rsplit("/", 1)[-1] for c in catalogo}
        for velho in sorted(args.saida.glob("*.txt")):
            if velho.name not in na_base:
                avisos.append(f"{rel(velho)} já não entra na base (apaga-o à mão se não precisares dele)")

    if avisos:
        print("\nAvisos:")
        for a in avisos:
            print("  -", a)
    modo = "núcleo + opcional" if args.opcional else "só núcleo"
    print(f"\n{tot['pdf']} PDF lidos ({n(tot['paginas'])} páginas): {n(tot['palavras_pdf'])} palavras no total.")
    print(f"Núcleo: {n(tot['nucleo'])} palavras em {tot['docs_nucleo']} documentos. "
          f"Opcional: {n(tot['opcional'])} palavras em {tot['docs_opcional']} documentos.")
    if not args.so:
        print(f"Escrito em {rel(args.saida)} ({modo}): {n(tot['escritas'])} palavras em {tot['docs_escritos']} ficheiros.")
        print(f"PDF usados: {rel(args.pdf_dir)} ({len(pdfs_usados)} ficheiros, com o mesmo nome dos .txt)")
        print(f"Catálogo: {rel(args.catalogo)}   Relatório: {rel(args.relatorio)}")


if __name__ == "__main__":
    main()
