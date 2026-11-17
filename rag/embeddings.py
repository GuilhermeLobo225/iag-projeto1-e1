"""Modelos de embeddings do E1, pelo Ollama, com os prefixos dos model cards (plano de 2/11).

O Ollama não acrescenta nenhum prefixo (o template destes modelos é só o texto), por isso são postos aqui.
Os vetores vêm normalizados pelo Ollama; a semelhança é o cosseno.
"""
import numpy as np
import ollama

import comum

QWEN3 = "Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:"

# Nome da experiência → modelo no Ollama, prefixo das perguntas e prefixo dos excertos.
MODELOS = {
    "qwen3-embedding-8b": {"ollama": "qwen3-embedding:8b", "query_prefix": QWEN3, "document_prefix": ""},
    # Acrescentado a 8/11: o E2 testou-o e, na A, ficou à frente do 8B.
    "qwen3-embedding-4b": {"ollama": "qwen3-embedding:4b", "query_prefix": QWEN3, "document_prefix": ""},
    "qwen3-embedding-0.6b": {"ollama": "qwen3-embedding:0.6b", "query_prefix": QWEN3, "document_prefix": ""},
    "bge-m3": {"ollama": "bge-m3", "query_prefix": "", "document_prefix": ""},
    "embeddinggemma": {"ollama": "embeddinggemma", "query_prefix": "task: search result | query: ",
                       "document_prefix": "title: none | text: "},
    # Desvio ao plano, decidido a 6/11: no teste com os 25 trechos das perguntas, o EmbeddingGemma do Ollama
    # acertou 7 em 12 com os prefixos e 10 em 12 sem eles. Reportam-se as duas variantes.
    "embeddinggemma-sem-prefixos": {"ollama": "embeddinggemma", "query_prefix": "", "document_prefix": ""},
    # Acrescentado a 8/11: o E2 usou «title: …»; o model card admite o título real do documento em vez de «none».
    "embeddinggemma-titulo": {"ollama": "embeddinggemma", "query_prefix": "task: search result | query: ",
                              "document_prefix": "title: {title} | text: "},
}
LOTE = 32  # textos por pedido ao Ollama


def info(nome):
    """Versão exata do modelo no Ollama, para o config.json."""
    m = MODELOS[nome]["ollama"]
    etiqueta = m if ":" in m else m + ":latest"
    digest = next((x.digest for x in ollama.list().models if x.model == etiqueta), None)
    s = ollama.show(m)
    arq = s.modelinfo["general.architecture"]
    return {"name": nome, "ollama_model": etiqueta, "digest": digest, "quantization": s.details.quantization_level,
            "parameters": s.details.parameter_size, "dimensions": s.modelinfo.get(f"{arq}.embedding_length"),
            "context_length": s.modelinfo.get(f"{arq}.context_length"),
            "query_prefix": MODELOS[nome]["query_prefix"], "document_prefix": MODELOS[nome]["document_prefix"],
            "ollama_version": comum.versao_ollama()}


def embeda(nome, textos, tipo, titulos=None):
    """Vetores (float32, um por linha) de uma lista de textos; tipo é "query" ou "document".
    titulos: o título do documento de cada texto, para os prefixos com {title} (sem títulos, fica «none»)."""
    m = MODELOS[nome]
    prefixo = m["query_prefix"] if tipo == "query" else m["document_prefix"]
    entradas = [prefixo.format(title=t) if "{title}" in prefixo else prefixo
                for t in (titulos or ["none"] * len(textos))]
    entradas = [p + t for p, t in zip(entradas, textos)]
    vetores = []
    for i in range(0, len(entradas), LOTE):
        # truncate=False: dá erro em vez de cortar em silêncio um texto maior do que o contexto do modelo.
        r = ollama.embed(model=m["ollama"], input=entradas[i:i + LOTE], truncate=False)
        vetores += r.embeddings
    return np.array(vetores, dtype=np.float32)
