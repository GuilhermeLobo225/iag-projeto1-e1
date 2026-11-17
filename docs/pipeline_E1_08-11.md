# Pipeline RAG do E1: o que foi feito a 8/11/2026

Trabalho feito com o Claude (Anthropic) no Claude desktop, no PC do Lobo. Continua o `pipeline_E1_06-11.md`. Nada foi commitado.

## 1. Juiz gpt-oss-120b pelo Groq

- `rag/cliente_groq.py`: API do Groq (compatível com a da OpenAI). A chave lê-se do `.env` e nunca é escrita. Cada resposta fica em `cache/groq/` e cada pedido pago em `cache/groq/uso.jsonl`. Espera 2,5 s entre pedidos e espera quando faltam tokens no minuto; no erro 429 respeita o `retry-after`; no limite diário para de forma limpa.
- Limites confirmados nos cabeçalhos: 1 000 pedidos/dia e 8 000 tokens/min. O limite de 200 000 tokens/dia só aparece no erro 429.
- O mesmo prompt e os mesmos esquemas do juiz v0.1 (SHA-1 `6d60494c90eb`), temperatura 0, `reasoning_effort` «medium» e `response_format` com o esquema JSON.
- Avaliou primeiro as 20 respostas do piloto e depois o resto. Com o limite diário, as 60 da A só ficaram completas a 9/11 à 01:04 (`--espera`). Cada resposta gasta cerca de 6 000 tokens, cerca de 33 respostas por dia.
- Na A, o 120b e o 20b dão a mesma correção em 53 das 60 respostas (kappa quadrático 0,87) e a mesma nota de citações em 43 de 56 (0,80). O 120b nunca precisou de repetir um pedido.
- A maior diferença é a do Ministral na E1-02 (2 no 20b, 0 no 120b). A resposta manda copos e pratos para os ecocentros, e a referência diz resíduos indiferenciados. O 120b apanhou a contradição e o 20b não.

| LLM (juiz 120b) | Correção (com resposta) | Correção (sem resposta) | Fidelidade | Não suportadas | Citações | Abstenções certas | Latência (s) |
|---|---|---|---|---|---|---|---|
| gemma4:12b | 1,42 | 1,33 | 0,96 | 1 | 1,83 | 2/3 | 3,2 |
| qwen3.5:9b | 1,33 | 2,00 | 0,87 | 9 | 1,67 | 3/3 | 2,9 |
| amalia-9b | 1,25 | 1,33 | 0,78 | 11 | 1,07 | 1/3 | 2,6 |
| ministral-3:14b | 1,25 | 2,00 | 0,90 | 4 | 1,50 | 3/3 | 4,3 |

## 2. Embeddings: regra do E2, Qwen3-Embedding 4B e EmbeddingGemma com título

Recall@5 com as duas regras (são iguais: só 8 de 1 750 pares de excerto e trecho mudam, e nenhum muda o Recall@5) e o MRR de cada regra. Tudo na mesma versão do Ollama (0.40.15).

| Modelo | A: Recall@5 | A: MRR@5 (E1) | A: MRR@10 (E2) | B: Recall@5 | B: MRR@5 (E1) | B: MRR@10 (E2) |
|---|---|---|---|---|---|---|
| qwen3-embedding:8b | 0,681 | 0,500 | 0,514 | 0,625 | 0,561 | 0,572 |
| **qwen3-embedding:4b** | **0,694** | **0,632** | **0,632** | 0,597 | 0,479 | 0,479 |
| qwen3-embedding:0.6b | 0,500 | 0,396 | 0,410 | 0,458 | 0,326 | 0,336 |
| bge-m3 | 0,569 | 0,507 | 0,526 | 0,444 | 0,429 | 0,443 |
| embeddinggemma | 0,514 | 0,382 | 0,401 | 0,403 | 0,454 | 0,481 |
| embeddinggemma, sem prefixos | 0,611 | 0,482 | 0,482 | 0,389 | 0,417 | 0,510 |
| embeddinggemma, título real | 0,542 | 0,417 | 0,438 | 0,486 | 0,454 | 0,531 |

Pela regra do plano, a melhor passa a ser o Qwen3-Embedding 4B na A, com as duas regras de acerto.

## 3. Configuração C

BM25 Okapi com k1 = 1,5, b = 0,75 e o IDF do Lucene; minúsculas, tokens `\w+`, as 207 stopwords de português do NLTK e o stemmer Snowball (NLTK 3.10.4). Junta-se à pesquisa densa por RRF com k = 60 e os 50 primeiros de cada lista; os empates resolvem-se pela posição na densa. O exemplo de 20/10 dá o resultado esperado (`tests/test_pesquisa.py`).

| Na A | Recall@5 densa | Recall@5 C | MRR@5 densa | MRR@5 C |
|---|---|---|---|---|
| BM25 sozinho | — | 0,375 | — | 0,444 |
| qwen3-embedding:8b | 0,681 | 0,528 | 0,500 | 0,576 |
| qwen3-embedding:4b | 0,694 | 0,625 | 0,632 | 0,597 |
| qwen3-embedding:0.6b | 0,500 | 0,583 | 0,396 | 0,514 |
| bge-m3 | 0,569 | 0,556 | 0,507 | 0,531 |
| embeddinggemma, sem prefixos | 0,611 | 0,625 | 0,482 | 0,507 |

A pesquisa híbrida baixa o Recall@5 dos Qwen 8B e 4B e ajuda os embeddings mais fracos. O BM25 sozinho é fraco nestas perguntas.

## 4. Experiências A, B e C (provisórias)

`rag/experiencia.py` corre cada experiência de ponta a ponta a partir do `config.json` da pasta: embedding, LLM, juiz, frase de abstenção, formato das citações e k. Escolha provisória: Qwen3-Embedding 8B e Gemma 4 12B, sem o juiz. A C escolheu os excertos A pela regra do plano.

| Exp. | Pesquisa | Recall@5 | MRR@5 | Cobertura multi_doc | Abstenção correta | Falsa abstenção | Respostas com citação | Latência (s) |
|---|---|---|---|---|---|---|---|---|
| A | densa | 0,681 | 0,500 | 0,50 | 2/3 | 0/10 | 12/12 | 3,2 |
| B | densa | 0,625 | 0,561 | 0,25 | 2/3 | 0/9 | 11/11 | 2,4 |
| C | híbrida (A) | 0,528 | 0,576 | 0,25 | 2/3 | 1/9 | 11/11 | 3,3 |

## 5. Análise de erros

`rag/analise_erros.py` junta, por pergunta e experiência, os 5 excertos (com os acertos), os quase-acertos do 6.º ao 10.º lugar, a resposta, os problemas detetados em código e as notas do juiz (`experiments/E1/analise_erros.md` e `.csv`).

E1-03 e E1-05 (revistas a 8/11):
- **E1-03 (sofá).** Nenhum dos excertos recuperados responde. O E1-004 define «monstros», mas sem dizer como se recolhem nem quanto custa; o E1-003 fala de volumosos em campanhas e nos ecocentros, sem preço; o E1-001 fala de reparação gratuita. Proposta: não acrescentar trechos.
- **E1-05 (desconto de 2026).** O PAPERSU (E1-001) descreve um «reembolso de 50% da tarifa variável, em dezembro de 2024», para quem faz compostagem ou leva sacos de orgânicos: valor igual, mas de 2024 e com outras condições. Proposta: não acrescentar como trecho alternativo e tratá-lo na análise de erros como informação parecida noutro documento. **Decisão do Lobo (8/11): não acrescentar; a E1-05 fica como está e entra na análise de erros.**

## 6. Decisões novas e desvios ao plano

1. A chave do Groq estava no `.env.example`, que vai para o git. Foi passada para o `.env` sem a mostrar, e o `.env.example` ficou só com o nome da variável.
2. Cada juiz guarda as avaliações em `juiz_<juiz>.jsonl`, e as do 20b saíram dos `results.jsonl` sem mudarem.
3. Groq: esquema JSON não estrito. O Groq valida o JSON e devolve um erro quando falha, e isso conta como tentativa falhada. A ordem «justificação antes da nota» não é garantida no JSON, mas o raciocínio vem sempre antes.
4. Regra de acerto do E2 acrescentada só para comparar entre áreas; a do E1 não muda.
5. Acrescentados o Qwen3-Embedding 4B e o EmbeddingGemma com o título real do documento (`title: {título} | text: `, como admite o model card).
6. O Ollama atualizou-se de 0.40.14 para 0.40.15. Com os excertos de uma versão e as perguntas da outra, excertos com pontuações quase iguais trocavam de lugar (o MRR@5 do 8B na B passou de 0,561 para 0,519). Tudo foi refeito na 0.40.15, cada coleção guarda a versão e a pesquisa recusa-se a correr com versões diferentes. A tabela de 6/11 está em `resumo_ollama-0.40.14.md`.
7. O teste dos LLM fica com o contexto com que foi feito (8B na A), mesmo com o 4B a ser agora o melhor.
8. BM25 implementado à mão (Okapi, IDF do Lucene), com as stopwords e o stemmer do NLTK, para os parâmetros ficarem todos à vista.
9. A frase de abstenção e o formato das citações ficam num só sítio (`prompt_geracao.py`) e escolhem-se no `config.json`. Há o formato «excerto» (`[E1-003_A0012]`), proposto pelo E2. Com os valores de 20/10, o prompt v1 fica igual (SHA-1 `6334930e8cdc`).
10. A C escolhe os excertos pela regra do plano, a partir dos resultados de A e de B.
11. Piloto: kappa de Cohen com pesos quadráticos (para comparar com o E3); o `cria` não substitui uma folha que já exista.

## 6b. Noite de 8/11: os 4 LLM em A, B e C

- `avalia_llm.py --config B|C`: os 4 LLM com os 5 primeiros excertos das experiências B e C do Qwen3-Embedding 8B (`experiments/E1/modelos/llm_B` e `llm_C`). As respostas do Gemma 4 foram reaproveitadas das experiências B e C, porque o prompt e os excertos são os mesmos. A A é o teste de 6/11.
- O juiz gpt-oss-20b avaliou as 120 respostas da B e da C, com o mesmo prompt e os mesmos parâmetros. É indicativo, porque o Groq chegou ao limite diário.
- `avalia_juiz.py --espera`: com o Groq, no limite diário espera o tempo que o Groq indica e continua (o 120b ficou a acabar a A durante a noite).
- `tabelas_grupo.py`: tabelas no formato do E3 para a mensagem ao grupo (`experiments/E1/tabelas_grupo_gpt-oss-20b.md`).
- Resultado com o 20b, correção em pontos (A, B, C, total em 72): Ministral 18, 14, 12, 44; Gemma 4 17, 15, 11, 43; Qwen3.5 14, 16, 13, 43; AMALIA 16, 14, 13, 43. A pior configuração é a C (49 pontos somando os 4), e os quatro falham nas mesmas perguntas.
- Na A, o 120b e o 20b deram a mesma correção em 53 das 60 respostas. Pontos na A com o 120b: Gemma 4 17, Qwen3.5 16, AMALIA 15, Ministral 15 (com o 20b: 17, 14, 16, 18). Tabela em `experiments/E1/tabelas_grupo_gpt-oss-120b.md`.
- 14/11: o 120b na B e na C, com o Gemma 4 primeiro (`--espera`, cerca de 3 dias para as 120 respostas). Gemma 4 com o 120b: A 17, B 15, C 9, total 41 em 72 (com o 20b, 43). É igual ao 20b nas 15 da B e em 14 das 15 da C. A diferença é a E1-08 na C (2 no 20b, 0 no 120b): a resposta diz que o valor da coima não está nos excertos e atribui os 25 € a 250 € a outra infração.

## 7. Pendente

- As tuas notas na folha do piloto; depois, `rag/piloto.py compara` com o 20b e o 120b.
- O 120b na B e na C (120 respostas, cerca de 4 dias com o limite do Groq), se o grupo quiser essa comparação.
- A decisão do grupo sobre os modelos, a regra de acerto, a frase de abstenção e o formato das citações; depois, A, B e C com os modelos finais e o juiz.
