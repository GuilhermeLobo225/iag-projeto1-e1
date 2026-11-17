# Teste dos LLM (E1) pela grelha comum, com o juiz gpt-oss-20b

15/11/2026. As 15 perguntas com os mesmos 5 excertos (qwen3-embedding-8b_B (dense, excertos B)), prompt de geração v1. Juiz `gpt-oss:20b` (ollama, raciocínio «medium», temperatura 0, 1 corrida), prompt do juiz v0.1. Em 2 das 60 respostas, o 1.º pedido não deu JSON válido e repetiu-se com temperatura 0,5.

| LLM | Correção (com resposta, 0–2) | Correção (sem resposta, 0–2) | Fidelidade (0–1) | Afirmações não suportadas | Citações (0–2) | Abstenções certas | Abstenções indevidas | Português europeu | Latência média (s) | Tokens/s |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-12b | 1,17 | 2,00 | 1,00 | 0 | 2,00 | 2/3 | 2/12 | 100% | 2,4 | 100 |
| qwen3.5-9b | 1,33 | 2,00 | 0,92 | 2 | 1,82 | 3/3 | 1/12 | 100% | 2,5 | 66 |
| amalia-9b | 1,17 | 1,33 | 0,76 | 7 | 1,40 | 0/3 | 0/12 | 100% | 2,3 | 64 |
| ministral-3-14b | 1,00 | 2,00 | 0,95 | 1 | 1,91 | 3/3 | 1/12 | 100% | 3,2 | 44 |

Correção: média das 12 perguntas com resposta; nas 3 sem resposta, 2 se diz que a informação não está nas fontes. Fidelidade, afirmações não suportadas e citações: nas respostas que não se abstêm (frase fixa, medida em código). Abstenções indevidas: nas perguntas com resposta, incluindo aquelas em que a pesquisa não trouxe o trecho certo.
