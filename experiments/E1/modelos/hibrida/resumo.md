# Configuração C (E1): pesquisa híbrida, densa + BM25 por RRF

08/11/2026. 12 perguntas com resposta. BM25: Okapi BM25, IDF do Lucene, k1 = 1,5, b = 0,75; minúsculas, tokens `\w+`, stopwords NLTK, português (207 palavras), Snowball do NLTK, português (NLTK 3.10.4). RRF com k = 60 e os 50 primeiros de cada pesquisa; empates pela posição na densa. A densa é a do teste dos embeddings, sobre os mesmos excertos.

| Embedding | Excertos | Recall@5 densa | MRR@5 densa | Recall@5 C | MRR@5 C | Cobertura multi_doc C | Recall@5 C (E2) | MRR@10 C (E2) |
|---|---|---|---|---|---|---|---|---|
| BM25 sozinho | A | — | — | 0,375 | 0,444 | 0,25 | 0,375 | 0,470 |
| BM25 sozinho | B | — | — | 0,319 | 0,315 | 0,00 | 0,319 | 0,327 |
| qwen3-embedding-8b | A | 0,681 | 0,500 | 0,528 | 0,576 | 0,25 | 0,528 | 0,597 |
| qwen3-embedding-8b | B | 0,625 | 0,561 | 0,361 | 0,424 | 0,00 | 0,361 | 0,462 |
| qwen3-embedding-4b | A | 0,694 | 0,632 | 0,625 | 0,597 | 0,50 | 0,625 | 0,617 |
| qwen3-embedding-4b | B | 0,597 | 0,479 | 0,403 | 0,444 | 0,00 | 0,403 | 0,467 |
| qwen3-embedding-0.6b | A | 0,500 | 0,396 | 0,583 | 0,514 | 0,50 | 0,583 | 0,523 |
| qwen3-embedding-0.6b | B | 0,458 | 0,326 | 0,403 | 0,438 | 0,00 | 0,403 | 0,449 |
| bge-m3 | A | 0,569 | 0,507 | 0,556 | 0,531 | 0,25 | 0,556 | 0,531 |
| bge-m3 | B | 0,444 | 0,429 | 0,403 | 0,433 | 0,00 | 0,403 | 0,456 |
| embeddinggemma | A | 0,514 | 0,382 | 0,542 | 0,472 | 0,25 | 0,542 | 0,484 |
| embeddinggemma | B | 0,403 | 0,454 | 0,444 | 0,412 | 0,00 | 0,444 | 0,440 |
| embeddinggemma-sem-prefixos | A | 0,611 | 0,482 | 0,625 | 0,507 | 0,50 | 0,625 | 0,517 |
| embeddinggemma-sem-prefixos | B | 0,389 | 0,417 | 0,486 | 0,422 | 0,00 | 0,486 | 0,434 |
| embeddinggemma-titulo | A | 0,542 | 0,417 | 0,542 | 0,514 | 0,25 | 0,542 | 0,514 |
| embeddinggemma-titulo | B | 0,486 | 0,454 | 0,486 | 0,422 | 0,00 | 0,486 | 0,436 |
