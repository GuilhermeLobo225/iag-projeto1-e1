"""BM25 sobre os excertos: a pesquisa lexical da configuração C (decisões de 20/10, ponto 7.4).

Pré-processamento: minúsculas, tokens alfanuméricos (\\w+, com acentos), sem as stopwords de português do NLTK e
com o stemmer Snowball para português (NLTK). BM25 Okapi com k1 = 1,5 e b = 0,75 e o IDF do Lucene,
ln(1 + (N − df + 0,5) / (df + 0,5)), que nunca é negativo. Os termos repetidos na pergunta contam as vezes que
aparecem. As stopwords descarregam-se uma vez para cache/nltk_data (fora do git).
"""
import functools
import math
import re
from collections import Counter

import comum

K1, B = 1.5, 0.75
DADOS_NLTK = comum.RAIZ / "cache/nltk_data"


@functools.cache
def _recursos():
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem.snowball import SnowballStemmer
    if str(DADOS_NLTK) not in nltk.data.path:
        nltk.data.path.insert(0, str(DADOS_NLTK))
    try:
        paragem = stopwords.words("portuguese")
    except LookupError:
        nltk.download("stopwords", download_dir=str(DADOS_NLTK), quiet=True)
        paragem = stopwords.words("portuguese")
    return frozenset(paragem), SnowballStemmer("portuguese"), nltk.__version__


def parametros():
    """Para o config.json."""
    paragem, _, versao = _recursos()
    return {"variant": "Okapi BM25, IDF do Lucene", "k1": K1, "b": B, "lowercase": True, "token_pattern": r"\w+",
            "stopwords": f"NLTK, português ({len(paragem)} palavras)", "stemmer": "Snowball do NLTK, português",
            "nltk_version": versao}


def tokens(texto):
    paragem, stemmer, _ = _recursos()
    return [stemmer.stem(t) for t in re.findall(r"\w+", texto.lower()) if t not in paragem]


class BM25:
    def __init__(self, textos):
        self.docs = [Counter(tokens(t)) for t in textos]
        self.tamanhos = [sum(d.values()) for d in self.docs]
        self.media = sum(self.tamanhos) / len(self.tamanhos)
        n, df = len(self.docs), Counter(t for d in self.docs for t in d)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def pontuacoes(self, pergunta):
        q = tokens(pergunta)
        resultado = []
        for d, tamanho in zip(self.docs, self.tamanhos):
            norma = K1 * (1 - B + B * tamanho / self.media)
            resultado.append(sum(self.idf[t] * d[t] * (K1 + 1) / (d[t] + norma) for t in q if t in d))
        return resultado

    def topo(self, pergunta, n):
        """(índice do excerto, pontuação) dos n melhores, sem os de pontuação 0; empates pela ordem dos excertos."""
        s = self.pontuacoes(pergunta)
        return [(i, s[i]) for i in sorted(range(len(s)), key=lambda i: (-s[i], i))[:n] if s[i] > 0]
