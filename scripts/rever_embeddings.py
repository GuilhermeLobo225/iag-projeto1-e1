#!/usr/bin/env python3
"""Revê a seleção do E1 com embeddings: dá a cada parágrafo uma nota de relevância para o tema
e aponta onde a seleção do partes_E1.json pode estar errada. Não altera nada na base.

Como funciona:
  1. Extrai e limpa o texto dos PDF exatamente como o pdf_para_txt.py e parte cada página em parágrafos.
     Os parágrafos seguidos com menos de 15 palavras juntam-se até chegarem às 15.
  2. Marca cada parágrafo como «núcleo», «opcional» ou «fora», conforme as partes do partes_E1.json.
  3. Calcula os embeddings dos parágrafos e das frases do scripts/temas_E1.txt.
     Nota = média das 3 maiores semelhanças às frases E1 − média das 3 maiores às frases OUTRO.
     A nota final é a média com os 2 parágrafos vizinhos de cada lado (a seleção faz-se por secções,
     e um parágrafo isolado com nota diferente das vizinhas é quase sempre ruído).
  4. Escolhe o limiar que melhor separa o núcleo do que ficou fora (índice de Youden, pesado pelas palavras).
     Acima do limiar, o parágrafo conta como relevante.
  5. Junta os desacordos seguidos em casos: núcleo com nota baixa (tirar?) e fora ou opcional com nota alta (juntar?).
     Só os casos com pelo menos 60 palavras vão para a folha de revisão.

Saída em kb/E1/revisao/:
  desacordos.csv   os casos para decidires, dos mais importantes para os menos (coluna «decisao»)
  documentos.csv   palavras por documento: no núcleo, relevantes segundo os embeddings e os cruzamentos
  paragrafos.csv   todos os parágrafos, com o rótulo e a nota
  resumo.md        o método e os números, para o relatório

Uso, na raiz do repositório:
  pip install sentence-transformers
  python scripts/rever_embeddings.py
Corre na GPU se o torch tiver CUDA (poucos minutos); no CPU pode levar mais de uma hora.
O modelo (Qwen/Qwen3-Embedding-0.6B, cerca de 1,2 GB) descarrega-se na primeira vez. Os embeddings dos
parágrafos ficam guardados em cache/; se só mudares as frases do temas_E1.txt, a corrida seguinte é rápida.
Os 8 PDF excluídos não entram: foram excluídos por serem antigos, repetidos ou só imagem, não pelo tema.
"""
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdf_para_txt as base  # noqa: E402  (a mesma extração e limpeza da base de conhecimento)

import numpy as np  # noqa: E402

MIN_PALAVRAS = 15
INSTRUCAO = "Instruct: Given a description of a topic, retrieve passages that discuss this topic\nQuery:"
NOMES = {"nucleo": "núcleo", "opcional": "opcional", "fora": "fora"}


def le_temas(caminho):
    e1, outros = [], []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        rotulo, _, texto = linha.partition(":")
        rotulo, texto = rotulo.strip().upper(), texto.strip()
        if rotulo == "E1" and texto:
            e1.append(texto)
        elif rotulo == "OUTRO" and texto:
            outros.append(texto)
        else:
            sys.exit(f"Linha sem «E1:» nem «OUTRO:» em {caminho.name}: {linha}")
    if len(e1) < 3 or len(outros) < 3:
        sys.exit(f"O {caminho.name} precisa de pelo menos 3 frases E1: e 3 frases OUTRO:.")
    return e1, outros


def rotula_pagina(pars, pagina, partes):
    """Rótulo de cada parágrafo da página: o tipo de parte que cobre a maior parte dele, ou «fora»."""
    texto = "\n".join(pars)
    cobertos = []
    for tipo, (a, b, mi, mf) in partes:
        if not (a <= pagina <= b):
            continue
        ini, fim = 0, len(texto)
        if pagina == a and mi:
            m = base.rx_marcador(mi).search(texto)
            if not m:
                continue
            ini = m.start()
        if pagina == b and mf:
            m = base.rx_marcador(mf).search(texto, ini)
            if not m:
                continue
            fim = m.start()
        cobertos.append((tipo, ini, fim))
    out, pos = [], 0
    for p in pars:
        ini, fim = pos, pos + len(p)
        pos = fim + 1
        conta = Counter()
        for tipo, a, b in cobertos:
            sob = min(fim, b) - max(ini, a)
            if sob > 0:
                conta[tipo] += sob
        tipo, sob = conta.most_common(1)[0] if conta else ("fora", 0)
        out.append((p, tipo if sob >= 0.5 * len(p) else "fora"))
    return out


def agrupa(rotulados):
    """Junta parágrafos seguidos com o mesmo rótulo até terem pelo menos MIN_PALAVRAS palavras."""
    out, buf, rot = [], [], None
    for p, r in rotulados:
        if buf and r != rot:
            out.append((rot, "\n".join(buf)))
            buf = []
        buf.append(p)
        rot = r
        if len(" ".join(buf).split()) >= MIN_PALAVRAS:
            out.append((rot, "\n".join(buf)))
            buf = []
    if buf:
        out.append((rot, "\n".join(buf)))
    return out


def unidades(config, docs, vocab, ocr_dir, avisos):
    out = []
    for d in config:
        if d["excluir"] or d["ficheiro"] not in docs:
            continue
        k = d["ficheiro"][:-4]
        partes = [("nucleo", tuple(p)) for p in d["nucleo"]] + [("opcional", tuple(p)) for p in d["opcional"]]
        if d["ocr"]:
            f = ocr_dir / f"{k}.txt"
            if not f.exists():
                avisos.append(f"{d['ficheiro']}: falta o texto do OCR em {base.rel(f)}")
                continue
            tipo = "nucleo" if d["nucleo"] else "opcional"
            paginas = [(1, [(p, tipo) for p in base.paragrafos_ocr(f.read_text(encoding="utf-8"), vocab)])]
        else:
            paginas = []
            for i, pg in enumerate(docs[d["ficheiro"]]["paginas"], start=1):
                pars = base.paragrafos(pg, vocab)
                if pars:
                    paginas.append((i, rotula_pagina(pars, i, partes)))
        for pagina, rotulados in paginas:
            for rotulo, texto in agrupa(rotulados):
                out.append({"doc_id": d["doc_id"], "ficheiro": d["ficheiro"], "titulo": d["title"], "pagina": pagina,
                            "rotulo": rotulo, "texto": texto, "palavras": len(texto.split())})
    return out


def semelhancas(textos, e1, outros, modelo, dispositivo, lote, cache, max_tokens):
    """Matrizes de semelhança (cosseno) de cada parágrafo às frases E1 e às frases OUTRO."""
    if modelo == "tfidf":  # só para testar o script sem descarregar o modelo
        from sklearn.feature_extraction.text import TfidfVectorizer
        vec = TfidfVectorizer(strip_accents="unicode", sublinear_tf=True, ngram_range=(1, 2), min_df=2)
        m = vec.fit_transform(textos + e1 + outros)
        d, f = m[:len(textos)], m[len(textos):]
        s = (d @ f.T).toarray()
        return s[:, :len(e1)], s[:, len(e1):]
    from sentence_transformers import SentenceTransformer
    if not dispositivo:
        import torch
        dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"A carregar o modelo {modelo} ({dispositivo})...")
    if dispositivo == "cpu":
        print("Aviso: sem GPU, os embeddings de ~20 mil parágrafos podem levar mais de uma hora. Para usar a GPU,\n"
              "instala o torch com CUDA (em pytorch.org/get-started, escolhe Windows, Pip e CUDA) e volta a correr.")
    st = SentenceTransformer(modelo, device=dispositivo)
    st.max_seq_length = max_tokens  # chega para perceber o tema; os parágrafos maiores só são cortados aqui
    chave = hashlib.sha1(f"{modelo}\x00{max_tokens}\x00{chr(0).join(textos)}".encode("utf-8")).hexdigest()
    emb = None
    if cache.exists():
        guardado = np.load(cache, allow_pickle=False)
        if str(guardado["chave"]) == chave:
            emb = guardado["emb"]
            print("Embeddings dos parágrafos lidos da cache.")
    if emb is None:
        print(f"A calcular os embeddings de {len(textos)} parágrafos (no CPU pode levar vários minutos)...")
        emb = st.encode(textos, batch_size=lote, normalize_embeddings=True, show_progress_bar=True, convert_to_numpy=True)
        cache.parent.mkdir(parents=True, exist_ok=True)
        np.savez(cache, chave=np.array(chave), emb=emb)
    fe1 = st.encode(e1, prompt=INSTRUCAO, normalize_embeddings=True, convert_to_numpy=True)
    fout = st.encode(outros, prompt=INSTRUCAO, normalize_embeddings=True, convert_to_numpy=True)
    return emb @ fe1.T, emb @ fout.T


def suaviza(us, notas, janela=2):
    """Média pesada da nota com os vizinhos do mesmo documento (peso = palavras, até 200)."""
    out = np.empty_like(notas)
    docs = [u["doc_id"] for u in us]
    pesos = np.minimum([u["palavras"] for u in us], 200).astype(float)
    for i in range(len(us)):
        idx = [j for j in range(max(0, i - janela), min(len(us), i + janela + 1)) if docs[j] == docs[i]]
        out[i] = np.average(notas[idx], weights=pesos[idx])
    return out


def media_top(s, k=3):
    k = min(k, s.shape[1])
    return np.sort(s, axis=1)[:, -k:].mean(axis=1)


def limiar(notas, rotulos, pesos):
    """Limiar que maximiza o índice de Youden (TPR − FPR), núcleo contra fora, pesado pelas palavras."""
    sel = np.isin(rotulos, ["nucleo", "fora"])
    s, y, w = notas[sel], rotulos[sel] == "nucleo", pesos[sel]
    if y.all() or not y.any():
        return float(np.median(notas)), float("nan"), float("nan")
    ordem = np.argsort(-s, kind="stable")
    s, y, w = s[ordem], y[ordem], w[ordem]
    tp, fp = np.cumsum(w * y), np.cumsum(w * ~y)
    tpr, fpr = tp / tp[-1], fp / fp[-1]
    fim_de_grupo = np.r_[s[1:] != s[:-1], True]  # só se corta entre notas diferentes
    j = np.where(fim_de_grupo, tpr - fpr, -np.inf)
    i = int(np.argmax(j))
    return float(s[i]), float(tpr[i]), float(fpr[i])


def casos(us, t):
    """Junta em casos os desacordos seguidos do mesmo documento e do mesmo tipo."""
    out, atual = [], None
    for u in us:
        if u["rotulo"] == "nucleo" and u["nota"] < t:
            tipo = "núcleo com nota baixa (tirar?)"
        elif u["rotulo"] != "nucleo" and u["nota"] >= t:
            tipo = f"{NOMES[u['rotulo']]} com nota alta (juntar?)"
        else:
            atual = None
            continue
        if atual and atual["doc_id"] == u["doc_id"] and atual["tipo"] == tipo:
            atual["us"].append(u)
        else:
            atual = {"doc_id": u["doc_id"], "ficheiro": u["ficheiro"], "tipo": tipo, "us": [u]}
            out.append(atual)
    for c in out:
        pal = sum(u["palavras"] for u in c["us"])
        c["palavras"] = pal
        c["nota"] = sum(u["nota"] * u["palavras"] for u in c["us"]) / max(pal, 1)
        c["peso"] = pal * abs(c["nota"] - t)
        a, b = c["us"][0]["pagina"], c["us"][-1]["pagina"]
        c["paginas"] = f"p. {a}" if a == b else f"pp. {a}-{b}"
        texto = " ⏎ ".join(u["texto"].replace("\n", " ⏎ ") for u in c["us"])
        c["inicio"], c["fim"] = texto[:220], texto[-160:] if len(texto) > 220 else ""
    return sorted(out, key=lambda c: -c["peso"])


def escreve_csv(caminho, linhas, campos):
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)


def n(x):
    return f"{int(round(x)):,}".replace(",", " ")


def main():
    ap = argparse.ArgumentParser(description="Revê a seleção do E1 com embeddings (não altera a base).")
    ap.add_argument("--raw", type=Path, default=base.RAIZ / "kb/E1/raw")
    ap.add_argument("--partes", type=Path, default=base.RAIZ / "scripts/partes_E1.json")
    ap.add_argument("--temas", type=Path, default=base.RAIZ / "scripts/temas_E1.txt")
    ap.add_argument("--ocr-dir", type=Path, default=base.RAIZ / "kb/E1/ocr")
    ap.add_argument("--saida", type=Path, default=base.RAIZ / "kb/E1/revisao")
    ap.add_argument("--cache", type=Path, default=base.RAIZ / "cache/embeddings_E1.npz")
    ap.add_argument("--modelo", default="Qwen/Qwen3-Embedding-0.6B", help="modelo de embeddings (ou «tfidf», só para testar)")
    ap.add_argument("--dispositivo", help="cpu ou cuda (por omissão, a GPU se houver)")
    ap.add_argument("--lote", type=int, default=32, help="parágrafos por lote no cálculo dos embeddings")
    ap.add_argument("--max-tokens", type=int, default=128, help="tokens de cada parágrafo usados no embedding")
    ap.add_argument("--max-casos", type=int, default=80, help="quantos casos pôr no desacordos.csv")
    ap.add_argument("--min-palavras-caso", type=int, default=60, help="tamanho mínimo de um caso para entrar na revisão")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    if args.modelo == "tfidf":
        print("Aviso: o «tfidf» só serve para testar o script. Não percebe sinónimos nem inglês; as notas não servem para decidir.")
    config = json.loads(args.partes.read_text(encoding="utf-8"))
    e1, outros = le_temas(args.temas)
    avisos = []
    print("A extrair o texto dos PDF (como o pdf_para_txt.py)...")
    docs, vocab = base.le_pdfs(config, args.raw, avisos)  # todos os PDF, para o vocabulário ser o mesmo da base
    us = unidades(config, docs, vocab, args.ocr_dir, avisos)
    if not us:
        sys.exit("Não encontrei texto para analisar.")
    s_e1, s_out = semelhancas([u["texto"] for u in us], e1, outros, args.modelo, args.dispositivo, args.lote, args.cache,
                              args.max_tokens)
    bruta = media_top(s_e1) - media_top(s_out)
    notas = suaviza(us, bruta)
    for u, nb, ns in zip(us, bruta, notas):
        u["nota_paragrafo"], u["nota"] = float(nb), float(ns)
    rotulos = np.array([u["rotulo"] for u in us])
    pesos = np.array([u["palavras"] for u in us], dtype=float)
    t, tpr, fpr = limiar(notas, rotulos, pesos)
    for u in us:
        u["relevante"] = "sim" if u["nota"] >= t else "não"

    # palavras por documento
    por_doc = {}
    for u in us:
        r = por_doc.setdefault(u["doc_id"], Counter())
        r["nucleo"] += u["palavras"] if u["rotulo"] == "nucleo" else 0
        r["relevantes"] += u["palavras"] if u["nota"] >= t else 0
        r[f"{u['rotulo']}_{'relevante' if u['nota'] >= t else 'pouco_relevante'}"] += u["palavras"]
    linhas_doc = []
    for d in config:
        if d["doc_id"] in por_doc:
            r = por_doc[d["doc_id"]]
            linhas_doc.append({"doc_id": d["doc_id"], "titulo": d["title"], "palavras_nucleo": r["nucleo"],
                               "palavras_relevantes": r["relevantes"], "nucleo_relevante": r["nucleo_relevante"],
                               "nucleo_pouco_relevante": r["nucleo_pouco_relevante"],
                               "opcional_relevante": r["opcional_relevante"], "fora_relevante": r["fora_relevante"],
                               "pct_nucleo_relevante": f"{100 * r['nucleo_relevante'] / r['nucleo']:.0f}%" if r["nucleo"] else "—"})
    tot = Counter()
    for r in linhas_doc:
        for k, v in r.items():
            if k.startswith(("palavras", "nucleo_", "opcional_", "fora_")):
                tot[k] += v
    todos = casos(us, t)
    cs = [c for c in todos if c["palavras"] >= args.min_palavras_caso]

    # ficheiros
    args.saida.mkdir(parents=True, exist_ok=True)
    escreve_csv(args.saida / "paragrafos.csv",
                [{**u, "rotulo": NOMES[u["rotulo"]], "nota": f"{u['nota']:.4f}", "nota_paragrafo": f"{u['nota_paragrafo']:.4f}",
                  "texto": u["texto"].replace("\n", " ⏎ ")} for u in us],
                ["doc_id", "ficheiro", "pagina", "rotulo", "palavras", "nota", "nota_paragrafo", "relevante", "texto"])
    escreve_csv(args.saida / "documentos.csv", linhas_doc, list(linhas_doc[0]))
    escreve_csv(args.saida / "desacordos.csv",
                [{"caso": i, **c, "nota": f"{c['nota']:.4f}", "decisao": "", "comentario": ""} for i, c in enumerate(cs[:args.max_casos], start=1)],
                ["caso", "doc_id", "ficheiro", "paginas", "tipo", "palavras", "nota", "inicio", "fim", "decisao", "comentario"])
    n_tirar = sum(1 for c in cs if c["tipo"].startswith("núcleo"))
    resumo = [
        "# Revisão da seleção do E1 com embeddings", "",
        f"Data: {date.today():%d/%m/%Y}. Modelo: `{args.modelo}`. Frases do tema: {len(e1)} do E1 e {len(outros)} de outros temas (`scripts/temas_E1.txt`).", "",
        "Método: cada parágrafo do texto limpo (com pelo menos 15 palavras, juntando os mais curtos) recebe a nota "
        "«média das 3 maiores semelhanças de cosseno às frases do E1 menos a média das 3 maiores às frases dos outros temas», "
        "suavizada com os 2 parágrafos vizinhos de cada lado. "
        "O limiar é o que melhor separa o núcleo atual do texto que ficou fora (índice de Youden, pesado pelas palavras). "
        "Os desacordos entre a nota e a seleção ficam no `desacordos.csv`, para decidir caso a caso.", "",
        "| | Valor |", "|---|---|",
        f"| Parágrafos analisados | {n(len(us))} ({len(por_doc)} documentos; os 8 excluídos não entram) |",
        f"| Limiar da nota | {t:.4f} |",
        f"| Palavras do núcleo acima do limiar | {tpr:.0%} |",
        f"| Palavras de fora do núcleo acima do limiar | {fpr:.0%} |",
        f"| **Palavras relevantes segundo os embeddings** | **{n(tot['palavras_relevantes'])}** |",
        f"| ... dentro do núcleo | {n(tot['nucleo_relevante'])} |",
        f"| ... nas partes opcionais | {n(tot['opcional_relevante'])} |",
        f"| ... fora da seleção | {n(tot['fora_relevante'])} |",
        f"| Palavras do núcleo com nota baixa | {n(tot['nucleo_pouco_relevante'])} |",
        f"| Casos de desacordo com {args.min_palavras_caso} palavras ou mais | {len(cs)} ({n_tirar} para tirar?, {len(cs) - n_tirar} para juntar?); "
        f"os {min(len(cs), args.max_casos)} maiores estão no `desacordos.csv` |",
        f"| Desacordos com menos de {args.min_palavras_caso} palavras (fora do `desacordos.csv`) | {len(todos) - len(cs)} ({n(sum(c['palavras'] for c in todos) - sum(c['palavras'] for c in cs))} palavras) |",
    ]
    (args.saida / "resumo.md").write_text("\n".join(resumo) + "\n", encoding="utf-8", newline="\n")

    if avisos:
        print("\nAvisos:")
        for a in avisos:
            print("  -", a)
    print(f"\n{n(len(us))} parágrafos de {len(por_doc)} documentos. Limiar da nota: {t:.4f} "
          f"(acima dele ficam {tpr:.0%} das palavras do núcleo e {fpr:.0%} das de fora).")
    print(f"Palavras do núcleo atual: {n(tot['palavras_nucleo'])}.")
    print(f"Palavras relevantes segundo os embeddings: {n(tot['palavras_relevantes'])} "
          f"(núcleo {n(tot['nucleo_relevante'])}, opcional {n(tot['opcional_relevante'])}, fora {n(tot['fora_relevante'])}).")
    print(f"Casos de desacordo com {args.min_palavras_caso} palavras ou mais: {len(cs)}; "
          f"os {min(len(cs), args.max_casos)} maiores estão em {base.rel(args.saida / 'desacordos.csv')}.")


if __name__ == "__main__":
    main()
