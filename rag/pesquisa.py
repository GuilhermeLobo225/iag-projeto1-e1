"""Recuperação do E1 sobre os excertos de uma configuração: densa (ChromaDB), lexical (BM25) ou híbrida (RRF).

RRF (Cormack et al., 2009; decisões de 20/10, ponto 7.4): pontuação(c) = Σ 1 / (60 + posição de c em cada lista),
com os 50 primeiros de cada pesquisa; empates resolvidos pela posição na pesquisa densa e depois na do BM25.
"""
import functools

import bm25
import comum
import embeddings
import indice

RRF_K, CANDIDATOS = 60, 50
MODOS = ("dense", "bm25", "hybrid")


@functools.cache
def excertos(config):
    return comum.le_jsonl(comum.EXPERIENCIAS / f"excertos_{config}.jsonl")


@functools.cache
def _bm25(config):
    return bm25.BM25([x["text"] for x in excertos(config)])


@functools.cache
def _colecao(embedding, config):
    """A coleção tem de ter sido criada com a mesma versão do Ollama com que se codificam as perguntas: a 8/11, com
    os excertos da 0.40.14 e as perguntas da 0.40.15, excertos com pontuações muito próximas trocaram de lugar."""
    col = indice.cliente().get_collection(indice.nome_colecao(embedding, config))
    criada, agora = (col.metadata or {}).get("ollama_version"), comum.versao_ollama()
    if criada != agora:
        raise RuntimeError(f"a coleção {col.name} foi criada com o Ollama {criada} e agora está o {agora}: refaz-a com "
                           f"rag/avalia_embeddings.py --modelo {embedding} --config {config}")
    return col


def densa(embedding, config, pergunta, n):
    return indice.pesquisa(_colecao(embedding, config), embeddings.embeda(embedding, [pergunta], "query")[0], n)


def lexical(config, pergunta, n):
    xs = excertos(config)
    return [{"rank": r, "chunk_id": xs[i]["chunk_id"], "doc_id": xs[i]["doc_id"], "start": xs[i]["start"],
             "end": xs[i]["end"], "score": round(s, 4)} for r, (i, s) in enumerate(_bm25(config).topo(pergunta, n), start=1)]


def rrf(densa_, lexical_, k=RRF_K):
    """Junta as duas listas (cada uma por ordem, com rank) numa só, pela pontuação RRF."""
    pontos, por_id = {}, {}
    posicao = {"dense": {x["chunk_id"]: x["rank"] for x in densa_}, "bm25": {x["chunk_id"]: x["rank"] for x in lexical_}}
    for lista in (densa_, lexical_):
        for x in lista:
            pontos[x["chunk_id"]] = pontos.get(x["chunk_id"], 0.0) + 1 / (k + x["rank"])
            por_id.setdefault(x["chunk_id"], x)
    fora = float("inf")
    ordem = sorted(pontos, key=lambda c: (-pontos[c], posicao["dense"].get(c, fora), posicao["bm25"].get(c, fora)))
    return [{"rank": r, "chunk_id": c, **{k_: por_id[c][k_] for k_ in ("doc_id", "start", "end")}, "score": round(pontos[c], 6),
             "rank_dense": posicao["dense"].get(c), "rank_bm25": posicao["bm25"].get(c)} for r, c in enumerate(ordem, start=1)]


def recupera(modo, embedding, config, pergunta, n=10):
    """Os n primeiros excertos (rank, chunk_id, doc_id, start, end, score) para a pergunta."""
    if modo == "dense":
        return densa(embedding, config, pergunta, n)
    if modo == "bm25":
        return lexical(config, pergunta, n)
    return rrf(densa(embedding, config, pergunta, CANDIDATOS), lexical(config, pergunta, CANDIDATOS))[:n]


def parametros(modo, embedding, config):
    """Para o config.json."""
    p = {"mode": modo, "chunks": config}
    if modo != "bm25":
        p["embedding"] = embedding
    if modo != "dense":
        p["bm25"] = bm25.parametros()
    if modo == "hybrid":
        p["fusion"] = {"method": "RRF", "k": RRF_K, "candidates_per_list": CANDIDATOS,
                       "ties": "posição na pesquisa densa, depois no BM25"}
    return p
