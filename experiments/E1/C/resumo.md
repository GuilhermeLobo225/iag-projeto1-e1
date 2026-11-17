# Experiência C (E1)

2026-11-08. Embedding `qwen3-embedding-8b`, LLM `gemma4-12b`, juiz `gpt-oss-120b` (avaliado). Frase de abstenção: «Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.». Citações: formato «doc». k = 5.

| Exp. | Excertos | Pesquisa | Recall@5 | MRR@5 | Cobertura multi_doc | Recall@5 (E2) | MRR@10 (E2) | Abstenção correta | Falsa abstenção | Respostas com citação | Correção (juiz) | Fidelidade (juiz) | Citações (juiz) | Latência (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C | A | hybrid | 0,528 | 0,576 | 0,25 | 0,528 | 0,597 | 2/3 | 1/9 | 11/11 | 0,75 | 0,96 | 1,82 | 3,3 |

Excertos escolhidos pela regra do plano: A ({"A": {"recall_at_5": 0.6805555555555556, "mrr_at_5": 0.5, "juiz_correcao_mais_fidelidade": null}, "B": {"recall_at_5": 0.625, "mrr_at_5": 0.5611111111111111, "juiz_correcao_mais_fidelidade": null}}).
