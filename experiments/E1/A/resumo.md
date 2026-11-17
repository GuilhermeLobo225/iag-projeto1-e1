# Experiência A (E1)

2026-11-08. Embedding `qwen3-embedding-8b`, LLM `gemma4-12b`, juiz `gpt-oss-120b` (avaliado). Frase de abstenção: «Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.». Citações: formato «doc». k = 5.

| Exp. | Excertos | Pesquisa | Recall@5 | MRR@5 | Cobertura multi_doc | Recall@5 (E2) | MRR@10 (E2) | Abstenção correta | Falsa abstenção | Respostas com citação | Correção (juiz) | Fidelidade (juiz) | Citações (juiz) | Latência (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | A | dense | 0,681 | 0,500 | 0,50 | 0,681 | 0,514 | 2/3 | 0/10 | 12/12 | 1,33 | 0,97 | 1,92 | 3,2 |
