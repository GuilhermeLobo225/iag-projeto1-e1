# Teste dos modelos de embeddings (E1)

08/11/2026. 12 perguntas com resposta (8 factual, 4 multi_doc); as 3 sem resposta não entram. Regra do E1: acerto a partir de 50% do mais curto (excerto ou trecho), Recall@5 e MRR@5. Regra do E2, só para comparar com as outras áreas: acerto com pelo menos 1 carácter, Recall@5 e MRR@10. Com estes excertos, o teto do Recall@5 (regra do E1) é 1 em A e em B. Tempos numa NVIDIA GeForce RTX 5060 Ti, 16311 MiB, Ollama 0.40.15, depois de um aquecimento com textos de 2 a 80 palavras (a GPU compila kernels na primeira utilização).

| Modelo | Config. | Recall@5 (E1) | MRR@5 (E1) | Cobertura total das multi_doc (E1) | Recall@5 factual (E1) | Recall@5 multi_doc (E1) | Recall@5 (E2) | MRR@10 (E2) | Indexação (s) | Por pergunta (ms) |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3-embedding-8b | A | 0,681 | 0,500 | 0,50 | 0,625 | 0,792 | 0,681 | 0,514 | 140,6 | 57 |
| qwen3-embedding-8b | B | 0,625 | 0,561 | 0,25 | 0,729 | 0,417 | 0,625 | 0,572 | 157,2 | 50 |
| **qwen3-embedding-4b** | A | 0,694 | 0,632 | 0,50 | 0,688 | 0,708 | 0,694 | 0,632 | 84,0 | 41 |
| qwen3-embedding-4b | B | 0,597 | 0,479 | 0,25 | 0,625 | 0,542 | 0,597 | 0,479 | 97,6 | 41 |
| qwen3-embedding-0.6b | A | 0,500 | 0,396 | 0,25 | 0,521 | 0,458 | 0,500 | 0,410 | 22,1 | 26 |
| qwen3-embedding-0.6b | B | 0,458 | 0,326 | 0,00 | 0,542 | 0,292 | 0,458 | 0,336 | 33,7 | 24 |
| bge-m3 | A | 0,569 | 0,507 | 0,25 | 0,646 | 0,417 | 0,569 | 0,526 | 16,9 | 26 |
| bge-m3 | B | 0,444 | 0,429 | 0,00 | 0,479 | 0,375 | 0,444 | 0,443 | 28,4 | 24 |
| embeddinggemma | A | 0,514 | 0,382 | 0,25 | 0,646 | 0,250 | 0,514 | 0,401 | 16,8 | 24 |
| embeddinggemma | B | 0,403 | 0,454 | 0,00 | 0,479 | 0,250 | 0,403 | 0,481 | 26,4 | 22 |
| embeddinggemma-sem-prefixos | A | 0,611 | 0,482 | 0,25 | 0,688 | 0,458 | 0,611 | 0,482 | 16,6 | 23 |
| embeddinggemma-sem-prefixos | B | 0,389 | 0,417 | 0,00 | 0,542 | 0,083 | 0,389 | 0,510 | 25,9 | 22 |
| embeddinggemma-titulo | A | 0,542 | 0,417 | 0,25 | 0,688 | 0,250 | 0,542 | 0,438 | 17,8 | 24 |
| embeddinggemma-titulo | B | 0,486 | 0,454 | 0,00 | 0,604 | 0,250 | 0,486 | 0,531 | 27,3 | 23 |

A negrito, a melhor pela regra do plano (Recall@5, depois MRR@5, depois B) com a regra de acerto do E1: qwen3-embedding-4b na A. Com a regra do E2: qwen3-embedding-4b na A.

| Modelo | No Ollama | Digest | Quantização | Dimensões | Prefixo das perguntas | Prefixo dos excertos |
|---|---|---|---|---|---|---|
| qwen3-embedding-8b | `qwen3-embedding:8b` | `64b933495768` | Q4_K_M | 4096 | `Instruct: Given a web search query, retrieve relevant passages that answer the query⏎Query:` | — |
| qwen3-embedding-4b | `qwen3-embedding:4b` | `df5bd2e3c74c` | Q4_K_M | 2560 | `Instruct: Given a web search query, retrieve relevant passages that answer the query⏎Query:` | — |
| qwen3-embedding-0.6b | `qwen3-embedding:0.6b` | `ac6da0dfba84` | Q8_0 | 1024 | `Instruct: Given a web search query, retrieve relevant passages that answer the query⏎Query:` | — |
| bge-m3 | `bge-m3:latest` | `790764642607` | F16 | 1024 | — | — |
| embeddinggemma | `embeddinggemma:latest` | `85462619ee72` | BF16 | 768 | `task: search result \| query: ` | `title: none \| text: ` |
| embeddinggemma-sem-prefixos | `embeddinggemma:latest` | `85462619ee72` | BF16 | 768 | — | — |
| embeddinggemma-titulo | `embeddinggemma:latest` | `85462619ee72` | BF16 | 768 | `task: search result \| query: ` | `title: {title} \| text: ` |

O embeddinggemma-sem-prefixos é um desvio ao plano, decidido a 6/11: num teste prévio com os 25 trechos das perguntas, o EmbeddingGemma do Ollama acertou 7 em 12 com os prefixos do model card e 10 em 12 sem eles. O qwen3-embedding-4b e o embeddinggemma-titulo (título real do documento no prefixo dos excertos, como admite o model card) foram acrescentados a 8/11, para comparar com os testes do E2.
