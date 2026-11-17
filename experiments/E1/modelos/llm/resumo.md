# Teste dos LLM (E1): verificações automáticas e latência

06/11/2026. As 15 perguntas, com os mesmos 5 excertos para todos (qwen3-embedding-8b_A). Prompt v1 (SHA-1 `6334930e8cdc`); temperatura 0, semente 42, contexto de 8192 tokens, até 600 de resposta, sem raciocínio, penalizações de repetição a zero. NVIDIA GeForce RTX 5060 Ti, 16311 MiB, Ollama 0.40.14, todos em Q4_K_M, depois de um aquecimento com a 1.ª pergunta.

| LLM | Abstenção correta (sem resposta) | Falsa abstenção (trecho nos excertos) | Abstenção (trecho fora dos excertos) | Respostas com citação | Citações fora dos excertos | Citações mal escritas | Truncadas | Latência média (s) | Tokens/s |
|---|---|---|---|---|---|---|---|---|---|
| gemma4-12b | 2/3 | 0/10 | 1/2 | 12/12 | 0 | 0 | 0 | 3,2 | 94 |
| qwen3.5-9b | 3/3 | 0/10 | 0/2 | 12/12 | 0 | 0 | 0 | 2,9 | 66 |
| amalia-9b | 1/3 | 0/10 | 0/2 | 11/14 | 0 | 0 | 0 | 2,6 | 61 |
| ministral-3-14b | 3/3 | 0/10 | 2/2 | 10/10 | 0 | 0 | 0 | 4,3 | 42 |

Abstenção: a resposta começa com a frase fixa (uma abstenção por outras palavras não conta). Falsa abstenção: nas perguntas com resposta em que algum trecho certo estava nos 5 excertos; quando nenhum estava (Recall@5 = 0), abster-se é o comportamento certo e conta-se à parte. Respostas com citação: das que não se abstêm, as que têm pelo menos uma citação `[E1-003]` válida. A correção, a fidelidade e as citações frase a frase avaliam-se depois com os juízes.
