# Experiências A, B e C (E1)

Embedding `qwen3-embedding-8b`, LLM `gemma4-12b`, juiz `gpt-oss-120b` (avaliado). Frase de abstenção: «Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.». Citações: formato «doc». k = 5.

| Exp. | Excertos | Pesquisa | Recall@5 | MRR@5 | Cobertura multi_doc | Recall@5 (E2) | MRR@10 (E2) | Abstenção correta | Falsa abstenção | Respostas com citação | Correção (juiz) | Fidelidade (juiz) | Citações (juiz) | Latência (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | A | dense | 0,681 | 0,500 | 0,50 | 0,681 | 0,514 | 2/3 | 0/10 | 12/12 | 1,33 | 0,97 | 1,92 | 3,2 |
| B | B | dense | 0,625 | 0,561 | 0,25 | 0,625 | 0,572 | 2/3 | 0/9 | 11/11 | 1,17 | 0,88 | 1,54 | 2,4 |
| C | A | hybrid | 0,528 | 0,576 | 0,25 | 0,528 | 0,597 | 2/3 | 1/9 | 11/11 | 0,75 | 0,96 | 1,82 | 3,3 |
