"""Base vetorial do E1 em ChromaDB: uma coleção por modelo de embeddings e configuração (A ou B).

Fica em indices/chroma, fora do git, porque se refaz a partir dos excertos. Cada excerto leva como metadados
o doc_id, o start e o end no .txt, os tokens e o título, a entidade e o URL do catálogo.
"""
import chromadb

import comum

PASTA = comum.RAIZ / "indices/chroma"
# Pesquisa por cosseno. Com ef altos e poucos milhares de excertos, o HNSW dá o mesmo que a pesquisa exata
# (confirmado em cada corrida pelo avalia_embeddings.py).
HNSW = {"space": "cosine", "ef_construction": 200, "ef_search": 200}


def cliente():
    return chromadb.PersistentClient(path=str(PASTA))


def nome_colecao(modelo, config):
    return f"E1_{modelo}_{config}"


def cria(cli, nome, excertos, vetores, metadados):
    """Cria a coleção de raiz (apaga a anterior com o mesmo nome) com os excertos e os seus vetores."""
    if nome in [c.name for c in cli.list_collections()]:
        cli.delete_collection(nome)
    col = cli.create_collection(nome, embedding_function=None, configuration={"hnsw": HNSW}, metadata=metadados)
    lote = cli.get_max_batch_size()
    for i in range(0, len(excertos), lote):
        parte = excertos[i:i + lote]
        col.add(ids=[x["chunk_id"] for x in parte], embeddings=vetores[i:i + lote], documents=[x["text"] for x in parte],
                metadatas=[{k: "" if x[k] is None else x[k] for k in ("doc_id", "start", "end", "tokens", "title", "entity", "url")}
                           for x in parte])  # o ChromaDB não aceita None nos metadados
    return col


def pesquisa(col, vetor, k=10):
    """Os k excertos mais semelhantes, por ordem, com o cosseno como score."""
    r = col.query(query_embeddings=[vetor], n_results=k, include=["metadatas", "distances"])
    return [{"rank": i, "chunk_id": cid, "doc_id": m["doc_id"], "start": m["start"], "end": m["end"],
             "score": round(1 - d, 4)}
            for i, (cid, m, d) in enumerate(zip(r["ids"][0], r["metadatas"][0], r["distances"][0]), start=1)]
