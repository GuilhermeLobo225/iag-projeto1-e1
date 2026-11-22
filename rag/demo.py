#!/usr/bin/env python3
"""Demonstração do pipeline RAG do E1 para a apresentação de 24/11: pergunta, excertos recuperados, resposta e fontes.

Só leitura: usa os parâmetros do config.json de uma experiência (por omissão, a A), como o rag/experiencia.py, e as
mesmas funções do pipeline: pesquisa.recupera (com a verificação da versão do Ollama), geracao.responde e
geracao.verifica. Não chama o juiz nem o Groq e não grava nenhum ficheiro.

Sem argumentos, corre a E1-08 (factual), a E1-12 (multi_doc) e a E1-13 (sem resposta na base). Antes da primeira,
aquece o embedding e o LLM com uma chamada que não aparece no ecrã, como o experiencia.py.

Ecrã pensado para gravar em vídeo com letra grande (cerca de 32 linhas por 100 colunas):
  - depois de carregar os modelos e antes de cada pergunta, limpa o ecrã e espera por Enter;
  - cada pergunta cabe em 32 linhas, até ao pedido de Enter (se não couber, saem as linhas em branco);
  - cada excerto ocupa uma linha (posição, documento, título e pontuação);
  - a pergunta e a resposta partem-se à largura do terminal, no máximo 100 colunas, sem partir palavras.
    As verificações são feitas sobre o texto original da resposta.
Com --detalhado, cada excerto mostra também a entidade, as posições no texto e os primeiros 200 caracteres (já não
cabe em 32 linhas). Com --sem-pausa, não há pausas nem se limpa o ecrã.

Uso, na raiz do repositório (com o Ollama a correr):
  .venv\\Scripts\\python rag/demo.py
  .venv\\Scripts\\python rag/demo.py --id E1-14 E1-03
  .venv\\Scripts\\python rag/demo.py --pergunta "Onde posso deixar um sofá velho em Guimarães?"
  .venv\\Scripts\\python rag/demo.py --sem-pausa --detalhado --config experiments/E1/C/config.json
"""
import argparse
import os
import shutil
import sys
import textwrap
import time

import comum
import embeddings
import experiencia
import geracao
import pesquisa

PERGUNTAS_DEMO = ["E1-08", "E1-12", "E1-13"]
TIPOS = {"factual": "factual", "multi_doc": "multi_doc (vários documentos)",
         "unanswerable": "sem resposta na base (o sistema deve abster-se)"}
MODOS = {"dense": "densa", "bm25": "BM25", "hybrid": "híbrida"}
ALTURA, LARGURA_MAX = 32, 100  # o ecrã da gravação: linhas e colunas

COR = sys.stdout.isatty() and "NO_COLOR" not in os.environ
if COR and os.name == "nt":
    os.system("")  # liga as cores ANSI na consola do Windows


def estilo(texto, codigo):
    return f"\033[{codigo}m{texto}\033[0m" if COR else texto


titulo = lambda t: estilo(t, "1;36")   # negrito, ciano
destaque = lambda t: estilo(t, "1")    # negrito
fraco = lambda t: estilo(t, "2")       # esbatido


def largura():
    """No máximo 100 colunas. Fica uma de folga: na consola do Windows, uma linha que enche a largura toda passa o
    cursor para a linha seguinte, e o fim de linha a seguir deixava uma linha em branco."""
    return max(40, min(LARGURA_MAX, shutil.get_terminal_size((LARGURA_MAX, ALTURA)).columns - 1))


def num(x, casas):
    return f"{x:.{casas}f}".replace(".", ",")


def milhares(n):
    return f"{n:,}".replace(",", " ")


def parte(texto, w):
    """Linhas de no máximo w colunas, sem partir palavras; as quebras de linha do texto mantêm-se."""
    return [linha for paragrafo in texto.split("\n")
            for linha in (textwrap.wrap(paragrafo, w, break_long_words=False, break_on_hyphens=False) or [""])]


def corta(texto, n):
    return texto if len(texto) <= n else texto[:max(0, n - 1)].rstrip() + "…"


def limpa():
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def espera(texto):
    try:
        input(fraco(texto))
    except EOFError:
        print()


def linha_config(cfg):
    r = cfg["retrieval"]
    return (f"Experiência {cfg['experiment']} · pesquisa {MODOS.get(r['mode'], r['mode'])} · "
            f"{r.get('embedding') or 'sem embedding'} · {cfg['llm']} · k = {r['k']}")


def le_config(caminho):
    """Os parâmetros do config.json, como no experiencia.py (incluindo o best_of_AB da C)."""
    cfg = experiencia.le(caminho)
    chunks, _ = experiencia.escolhe_excertos(cfg)
    return cfg, chunks


def corre_pergunta(cfg, chunks, pergunta):
    """Pesquisa, resposta e verificações, com os tempos (o que o experiencia.py faz por pergunta)."""
    r, frase, formato = cfg["retrieval"], cfg["prompt"]["abstention_phrase"], cfg["prompt"]["citation_format"]
    t = time.perf_counter()
    topo = pesquisa.recupera(r["mode"], r.get("embedding"), chunks, pergunta, 10)[:r["k"]]
    t_pesquisa = time.perf_counter() - t
    por_id = {x["chunk_id"]: x for x in pesquisa.excertos(chunks)}
    contexto = [por_id[c["chunk_id"]] for c in topo]
    resposta = geracao.responde(cfg["llm"], pergunta, contexto, frase, formato)
    return topo, contexto, resposta, geracao.verifica(resposta["answer"], contexto, frase, formato), t_pesquisa


def ecra(n, total, item, cfg, topo, contexto, resposta, verif, t_pesquisa, catalogo, detalhado, w):
    """As linhas de uma pergunta; None é uma linha em branco que sai se a pergunta não couber no ecrã."""
    linhas = [fraco(corta(linha_config(cfg), w)), fraco("═" * w)]
    cabeca = f"Pergunta {n} de {total}"
    if item.get("id"):
        cabeca += f" · {item['id']} · {TIPOS.get(item['type'], item['type'])}"
    linhas.append(titulo(corta(cabeca, w)))
    linhas += [destaque(x) for x in parte(item["question"], w)]

    linhas += [None, titulo(f"Excertos recuperados · pesquisa {num(t_pesquisa, 2)} s")]
    for c, x in zip(topo, contexto):
        doc = catalogo.get(c["doc_id"], {})
        inicio, fim = f"{c['rank']}. {c['doc_id']} · ", f" · {num(c['score'], 4)}"
        linhas.append(inicio + corta(doc.get("title", "(fora do catálogo)"), w - len(inicio) - len(fim)) + fim)
        if detalhado:
            linhas.append(fraco(corta(f"   {doc.get('entity', '—')} · caracteres {milhares(c['start'])} a "
                                      f"{milhares(c['end'])}", w)))
            texto = " ".join(x["text"].split())
            linhas += ["   " + y for y in parte("«" + texto[:200] + ("…»" if len(texto) > 200 else "»"), w - 3)]

    linhas += [None, titulo(f"Resposta ({cfg['llm']}) · {num(resposta['latency_s'], 1)} s · "
                            f"{resposta['tokens_out']} tokens")]
    linhas += parte(resposta["answer"], w)

    linhas += [None, titulo("Fontes citadas")]
    for d in verif["cited_doc_ids"]:
        doc = catalogo.get(d, {})
        extra = f" · {doc.get('entity', '—')}" if detalhado else ""
        linhas.append(corta(f"[{d}] {doc.get('title', '(fora do catálogo)')}{extra}", w))
    if not verif["cited_doc_ids"]:
        linhas.append("nenhuma")

    frase = "sim, no início" if verif["abstained"] else ("sim, a meio da resposta" if verif["abstention_phrase_elsewhere"] else "não")
    linhas += [None, titulo("Verificações em código"),
               f"Frase de abstenção: {frase}",
               corta(f"Citações fora dos excertos: {', '.join(verif['citations_outside_context']) or 'nenhuma'}", w),
               corta(f"Citações mal escritas: {', '.join(verif['malformed_citations']) or 'nenhuma'}", w)]
    return linhas


def mostra(linhas, reservadas=0):
    """Escreve as linhas; se, com as reservadas (o pedido de Enter), passarem de ALTURA, tira as linhas em branco."""
    if len(linhas) + reservadas > ALTURA:
        linhas = [x for x in linhas if x is not None]
    print("\n".join("" if x is None else x for x in linhas), flush=True)


def main():
    ap = argparse.ArgumentParser(description="Demonstração do pipeline RAG do E1 (só leitura; sem juiz).")
    qual = ap.add_mutually_exclusive_group()
    qual.add_argument("--id", nargs="+", metavar="ID", help="um ou mais ids de tests/questions_E1.jsonl (ex.: E1-14)")
    qual.add_argument("--pergunta", help="uma pergunta livre")
    ap.add_argument("--sem-pausa", action="store_true", help="não espera por Enter nem limpa o ecrã")
    ap.add_argument("--detalhado", action="store_true",
                    help="em cada excerto, também a entidade, as posições no texto e os primeiros 200 caracteres")
    ap.add_argument("--config", default=str(comum.EXPERIENCIAS / "A" / "config.json"),
                    help="config.json da experiência (por omissão, a A)")
    args = ap.parse_args()
    comum.prepara_consola()

    if args.pergunta:
        itens = [{"question": args.pergunta}]
    else:
        teste = {p["id"]: p for p in comum.le_jsonl(comum.PERGUNTAS)}
        ids = args.id or PERGUNTAS_DEMO
        desconhecidos = [i for i in ids if i not in teste]
        if desconhecidos:
            sys.exit(f"Ids que não existem: {', '.join(desconhecidos)}. Os do teste vão de {min(teste)} a {max(teste)}.")
        itens = [teste[i] for i in ids]

    cfg, chunks = le_config(args.config)
    catalogo = {d["doc_id"]: d for d in comum.le_catalogo()}
    r = cfg["retrieval"]
    print(destaque(linha_config(cfg)))
    print("A carregar os modelos...", flush=True)
    try:
        # Aquecimento, como no experiencia.py: o embedding e uma resposta à primeira pergunta, deitada fora.
        if r["mode"] != "bm25":
            embeddings.embeda(r["embedding"], ["aquecimento"], "query")
        corre_pergunta(cfg, chunks, itens[0]["question"])
        if not args.sem_pausa:
            limpa()
            print(fraco(linha_config(cfg)) + "\n")
            espera("Modelos carregados. Enter para começar...")

        for n, item in enumerate(itens, start=1):
            topo, contexto, resposta, verif, t_pesquisa = corre_pergunta(cfg, chunks, item["question"])
            linhas = ecra(n, len(itens), item, cfg, topo, contexto, resposta, verif, t_pesquisa, catalogo,
                          args.detalhado, largura())
            if args.sem_pausa:
                print()
                mostra(linhas)
            else:
                limpa()
                mostra(linhas + [None], reservadas=1)
                espera("Enter para a pergunta seguinte..." if n < len(itens) else "Fim da demonstração. Enter para sair...")
    except RuntimeError as e:  # por exemplo, a coleção criada com outra versão do Ollama (pesquisa._colecao)
        sys.exit(f"\nErro: {e}")
    except (ConnectionError, OSError) as e:
        sys.exit(f"\nErro: não consegui falar com o Ollama ({e}). Está a correr?")


if __name__ == "__main__":
    main()
