# Pipeline RAG do E1: o que foi feito a 6/11/2026

Trabalho feito com o Claude (Anthropic) no Claude desktop, com a pasta do repositório ligada. Tudo correu no PC do Lobo. Nada foi commitado.

## 1. Ambiente

- Python 3.11.9, NVIDIA RTX 5060 Ti com 16 GB (driver 595.97) e Ollama 0.40.14.
- `.venv` com Python 3.11 e `requirements.txt` com versões fixas: tokenizers, huggingface_hub, numpy, chromadb, ollama, python-dotenv e pytest. O torch não é preciso, porque os embeddings e os LLM correm no Ollama.
- O `.gitattributes` não existia no repositório e foi criado: força LF nos `.txt` e nos `.jsonl`. Sem ele, como o Git do PC tem `core.autocrlf=true`, um clone novo vinha com CRLF e as posições dos trechos deixavam de bater.
- Esta versão do Ollama não traz código compilado para a placa. Na primeira utilização de cada tamanho de entrada, a GPU compila kernels (até 4 s de cada vez). Os tempos medem-se sempre depois de um aquecimento.

## 2. Módulo 1: excertos e métrica

Ficheiros: `rag/comum.py`, `rag/excertos.py`, `rag/metricas.py` e `tests/test_metricas.py`.

**Excertos.** O texto parte-se em unidades: primeiro nas mudanças de linha, depois no fim das frases. Uma frase maior do que o máximo é cortada por tokens. Cada excerto junta unidades inteiras enquanto couberem no máximo. A sobreposição são as últimas unidades do excerto anterior que caibam em 50 (A) ou 20 (B) tokens. Os tokens contam-se com o tokenizador do bge-m3 (revisão `5617a9f`), sem tokens especiais. Cada excerto guarda `doc_id`, `start` e `end` no `.txt`, sem alterar o texto.

| | A (500/50) | B (200/20) |
|---|---|---|
| Excertos | 774 | 2 014 |
| Tokens (mínimo / média / máximo) | 65 / 465 / 500 | 25 / 174 / 200 |
| Pares seguidos com sobreposição | 73%, média de 26 tokens | 34%, média de 4 tokens |
| Frases cortadas por tokens | 0 | 4 |

A verificação relê os ficheiros e confirma o texto, o máximo e que nada fica de fora: passa nas duas. Na B, a sobreposição por frases inteiras quase desaparece, porque poucas frases cabem em 20 tokens. Isto tem de ser explicado no relatório.

**Métrica.** Um excerto acerta num trecho se for do mesmo documento e se a sobreposição for pelo menos 50% do mais curto. O Recall@5 conta cada grupo de trechos uma vez. O MRR@5 usa a posição do primeiro acerto. As perguntas sem resposta ficam de fora das duas. Os 4 casos de teste de 20/10 dão os valores certos, e há mais 4 testes. O comando `teto` mostra que todos os trechos podem ser apanhados por algum excerto, tanto na A como na B.

## 3. Módulo 2: embeddings, índice e teste

Ficheiros: `rag/embeddings.py`, `rag/indice.py` e `rag/avalia_embeddings.py`. Resultados em `experiments/E1/modelos/embeddings/`.

- Quatro modelos pelo Ollama, cerca de 7 GB: `qwen3-embedding:8b` (Q4_K_M), `qwen3-embedding:0.6b` (Q8_0), `bge-m3` (F16) e `embeddinggemma` (BF16).
- Prefixos dos model cards: o Qwen3 só nas perguntas, com `Query:` sem espaço no fim, como no model card; o EmbeddingGemma com `task: search result | query: ` e `title: none | text: `; o bge-m3 sem prefixos.
- Índice: ChromaDB local em `indices/` (fora do git), com cosseno e uma coleção por modelo e configuração, num total de 10. O HNSW deu os mesmos 10 primeiros excertos que a pesquisa exata nas 150 pesquisas.

| Modelo | Config. | Recall@5 | MRR@5 | Cobertura multi_doc | Indexação (s) | Por pergunta (ms) |
|---|---|---|---|---|---|---|
| qwen3-embedding:8b | A | **0,681** | 0,493 | **0,50** | 147 | 49 |
| qwen3-embedding:8b | B | 0,625 | **0,561** | 0,25 | 166 | 48 |
| qwen3-embedding:0.6b | A | 0,500 | 0,396 | 0,25 | 21 | 22 |
| qwen3-embedding:0.6b | B | 0,458 | 0,326 | 0,00 | 34 | 21 |
| bge-m3 | A | 0,569 | 0,507 | 0,25 | 17 | 26 |
| bge-m3 | B | 0,444 | 0,429 | 0,00 | 29 | 22 |
| embeddinggemma | A | 0,514 | 0,382 | 0,25 | 17 | 23 |
| embeddinggemma | B | 0,403 | 0,454 | 0,00 | 26 | 21 |
| embeddinggemma, sem prefixos | A | 0,611 | 0,482 | 0,25 | 17 | 21 |
| embeddinggemma, sem prefixos | B | 0,389 | 0,417 | 0,00 | 26 | 24 |

- Pela regra do plano (Recall@5, depois MRR@5, depois B), a melhor é o **Qwen3-Embedding 8B na A**. A A ganha à B no Recall@5 em todos os modelos.
- Com 12 perguntas, uma factual vale 0,083 no Recall@5, por isso as diferenças abaixo de 0,1 são uma ou duas perguntas.
- O EmbeddingGemma sem prefixos é um desvio ao plano. Num teste prévio com os 25 trechos das perguntas, acertou 7 em 12 com os prefixos e 10 em 12 sem eles. Na avaliação completa, sem prefixos é melhor na A e um pouco pior na B.
- A E1-05 falha em todos os modelos e a E1-03 em 9 de 10. São as primeiras candidatas para a análise de erros.

## 4. Módulo 3: LLM e prompt de geração

Ficheiros: `rag/prompt_geracao.py`, `rag/geracao.py`, `rag/testa_prompt.py` e `rag/avalia_llm.py`. Resultados em `experiments/E1/modelos/llm/`.

- Quatro LLM pelo Ollama, todos em Q4_K_M, cerca de 29 GB: `gemma4:12b`, `qwen3.5:9b`, AMALIA 9B (`hf.co/teex-pt/AMALIA-9B-0626-DPO-GGUF:Q4_K_M`) e `ministral-3:14b`. Todos correm 100% na GPU com contexto de 8 192.
- Parâmetros iguais para todos: temperatura 0, semente 42, contexto de 8 192, até 600 tokens de resposta e `think=False` nos que têm raciocínio (Qwen3.5 e Gemma 4). As penalizações de repetição ficaram a zero, por decisão de 6/11: o Qwen3.5 traz `presence_penalty 1.5`, que com temperatura 0 continua a castigar repetir citações.
- A primeira resposta depois de carregar o modelo pode sair diferente das seguintes. Por isso, cada modelo faz um aquecimento com a 1.ª pergunta, e essa resposta deita-se fora.
- Os 4 LLM recebem os mesmos 5 excertos (do Qwen3-Embedding 8B na A), guardados em `contexto.jsonl`.

**Prompt v1.** Segue o contrato do grupo: português europeu, só os excertos, `[E1-003]` no fim de cada frase com um facto, frase fixa de abstenção, cabeçalho `[id] Título — Entidade` e ignorar instruções dentro dos excertos. Foi testado com 2 perguntas inventadas (o compostor gratuito e o Repair Café):
- sem nada depois da pergunta, 7 das 8 respostas cumpriram o contrato;
- com um lembrete das regras no fim, ficou pior: o Ministral absteve-se na pergunta com resposta e o AMALIA copiou o `[E1-003]` do exemplo;
- ficou a versão sem lembrete, congelada a 6/11.

Verificações automáticas nas 15 perguntas: nenhum modelo citou documentos que não estivessem nos excertos, escreveu citações mal formatadas ou ficou com a resposta cortada. A falsa abstenção conta-se só quando o trecho estava nos excertos, e aí nenhum modelo se absteve. As abstenções na E1-03 e na E1-05 são corretas, porque a pesquisa não trouxe o trecho certo.

## 5. Módulo 4: juiz e piloto

Ficheiros: `rag/prompt_juiz.py`, `rag/juiz.py`, `rag/avalia_juiz.py` e `rag/piloto.py`.

- O juiz é o **gpt-oss-20b** local (MXFP4, 13 GB, 100% na GPU), a alternativa local da grelha. Não precisa de chaves.
- O prompt e os esquemas JSON seguem a grelha comum: (A) correção, com a pergunta, a referência e a resposta; (B) fidelidade e citações, com a pergunta, os excertos e a resposta. A fidelidade e as afirmações não suportadas calculam-se em código a partir da lista de afirmações do juiz. É a versão v0.1, para o piloto.

Problemas encontrados e resolvidos:
- **Raciocínio.** Não dá para o desligar. Com «low», o juiz ignorou o esquema JSON e deu nota a mais. Ficou «medium».
- **Corridas repetidas.** Com temperatura 0, a 1.ª corrida era sempre diferente e a 2.ª igual à 3.ª, o que aponta para a cache de prompts do Ollama. A mediana de 3 corridas não acrescentava nada, por isso ficou 1 corrida, como diz a grelha.
- **Citações.** O juiz punha ids nas citações de respostas que não citavam nada. Agora recebe a lista de ids encontrados em código, e a regra «0 se não cita» é aplicada em código.
- **Ciclos.** Às vezes repetia a mesma frase até gastar os tokens. A 1.ª tentativa usa temperatura 0 e, se falhar, as seguintes usam 0,5. Foi preciso em 9 das 60 respostas.

Resultados pela grelha (provisórios até ao piloto):

| LLM | Correção (com resposta) | Correção (sem resposta) | Fidelidade | Não suportadas | Citações | Abstenções certas | Abst. indevidas | PT-PT | Latência (s) | Tokens/s |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma4:12b | 1,42 | 1,33 | 0,93 | 2 | 1,83 | 2/3 | 1/12 | 100% | 3,2 | 94 |
| qwen3.5:9b | 1,17 | 2,00 | 0,87 | 7 | 1,67 | 3/3 | 0/12 | 100% | 2,9 | 66 |
| AMALIA 9B | 1,33 | 1,33 | 0,83 | 5 | 1,21 | 1/3 | 0/12 | 100% | 2,6 | 61 |
| ministral-3:14b | 1,50 | 2,00 | 0,89 | 5 | 1,70 | 3/3 | 2/12 | 100% | 4,3 | 42 |

Na E1-02, o juiz deu 0 ao Gemma, quando pela grelha devia ser 1. O piloto serve para medir desacordos destes.

**Piloto.** `experiments/E1/piloto/folha_piloto.csv` tem 20 respostas às cegas: 5 por LLM, 4 de perguntas sem resposta, sorteadas com a semente 42. A `chave_piloto.json` liga cada item ao modelo e não se abre antes de avaliar. O `piloto.py compara` calcula a concordância com o juiz e entre avaliadores; foi testado com uma folha preenchida com as notas do próprio juiz, que deu 100%.

## 6. Decisões e desvios ao plano

1. Criado o `.gitattributes`, que faltava.
2. EmbeddingGemma testado também sem prefixos (10 coleções em vez de 8).
3. Prefixo do Qwen3 com `Query:` sem espaço no fim, como no model card.
4. Aquecimento dos embeddings com textos de 2 a 80 palavras; aquecimento dos LLM com uma resposta completa, deitada fora.
5. Penalizações de repetição a zero nos 4 LLM.
6. Lembrete das regras no fim da mensagem testado e retirado do prompt v1.
7. Juiz local gpt-oss-20b em vez dos juízes por API, porque não há chaves; só vale se passar no piloto.
8. Juiz com raciocínio «medium», 1 corrida, regra «0 se não cita» em código e repetição com temperatura 0,5 quando o JSON falha.

## 7. Pendente

- Preencher a folha do piloto (de preferência com um 2.º avaliador do grupo) e correr o `compara`.
- Explicar os 4 módulos em 2 ou 3 frases cada, para as linhas do registo de IA.
- 8/11: escolha dos modelos no grupo e grelha v1.0 congelada.
- 9 a 15/11: experiências A, B e C (C = melhor de A/B + BM25 com RRF, ainda por escrever).
- Commit no GitHub Desktop.

## 8. Comandos para reproduzir

Na raiz do repositório, com o Ollama a correr:

```
.venv\Scripts\python rag\excertos.py
.venv\Scripts\python -m pytest
.venv\Scripts\python rag\metricas.py teto experiments\E1\excertos_A.jsonl experiments\E1\excertos_B.jsonl
.venv\Scripts\python rag\avalia_embeddings.py
.venv\Scripts\python rag\testa_prompt.py
.venv\Scripts\python rag\avalia_llm.py
.venv\Scripts\python rag\avalia_juiz.py
.venv\Scripts\python rag\piloto.py cria
.venv\Scripts\python rag\piloto.py compara experiments\E1\piloto\folha_piloto.csv
```
