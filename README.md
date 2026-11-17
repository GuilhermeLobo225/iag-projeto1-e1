# IAG 2026/27, Projeto 1: pipeline RAG do E1

Componente individual do Elemento 1 (Guilherme Lobo Pinto): resíduos e economia circular em Guimarães, incluindo a separação e o encaminhamento de resíduos, a reutilização e a reparação.
O repositório tem a base de conhecimento, as 15 perguntas de teste, o pipeline RAG (excertos, embeddings, base vetorial, pesquisa densa e híbrida, geração e juiz) e os resultados das experiências.

## Instalação

Precisa de Windows ou Linux, Python 3.11, uma placa NVIDIA com pelo menos 16 GB (para os LLM de 12 a 14 B e o juiz local) e o [Ollama](https://ollama.com).

```
py -3.11 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

O tokenizador do bge-m3 (cerca de 17 MB, revisão fixa) e as stopwords de português do NLTK descarregam-se sozinhos na primeira utilização, para a cache do Hugging Face e para `cache/nltk_data`.

### Modelos do Ollama

Com o Ollama a correr, descarregar os modelos com as tags exatas. Os digests são os que constam dos `config.json`.

| Uso | Tag | Digest | Quantização |
|---|---|---|---|
| Embeddings | `qwen3-embedding:8b` | `64b933495768` | Q4_K_M |
| Embeddings | `qwen3-embedding:4b` | `df5bd2e3c74c` | por omissão do Ollama |
| Embeddings | `qwen3-embedding:0.6b` | `ac6da0dfba84` | Q8_0 |
| Embeddings | `bge-m3` | `790764642607` | F16 |
| Embeddings | `embeddinggemma` | `85462619ee72` | BF16 |
| LLM | `gemma4:12b` | `6114515d63c1` | Q4_K_M |
| LLM | `qwen3.5:9b` | `56671c2ab938` | Q4_K_M |
| LLM | `hf.co/teex-pt/AMALIA-9B-0626-DPO-GGUF:Q4_K_M` | `d54f5ea76d3d` | Q4_K_M |
| LLM | `ministral-3:14b` | `4760c35aeb9d` | Q4_K_M |
| Juiz local | `gpt-oss:20b` | `f38aa0c53da5` | MXFP4 |

```
ollama pull qwen3-embedding:8b
```

(e o mesmo para cada uma das outras tags). São cerca de 52 GB no total. Modelos fechados pelo grupo a 15/11: `qwen3-embedding:8b`, `gemma4:12b` e o juiz `openai/gpt-oss-120b` (Groq). Para as experiências finais chegam esses dois do Ollama.

### Chaves (`.env`)

O juiz principal é o `openai/gpt-oss-120b` pela API gratuita do Groq. Copiar o `.env.example` para `.env` e preencher a chave:

```
GROQ_API_KEY=...
```

O `.env` nunca vai para o git. As respostas do Groq ficam em `cache/groq/`, para nenhum pedido se pagar duas vezes, e os tokens gastos ficam em `cache/groq/uso.jsonl`.

## Reproduzir

Na raiz do repositório, com o Ollama a correr. Os passos 1 a 3 já estão feitos e os resultados estão no repositório; o índice do ChromaDB (`indices/`) refaz-se no passo 3.

```
.venv\Scripts\python -m pytest
.venv\Scripts\python scripts\perguntas_E1.py valida tests\questions_E1.jsonl
```

1. Excertos A (500/50 tokens) e B (200/20), com a verificação do texto e do máximo, e o teto do Recall@5:
   ```
   .venv\Scripts\python rag\excertos.py
   .venv\Scripts\python rag\metricas.py teto experiments\E1\excertos_A.jsonl experiments\E1\excertos_B.jsonl
   ```
2. Teste dos embeddings (todos os modelos, A e B; cria as coleções do ChromaDB) e da pesquisa híbrida:
   ```
   .venv\Scripts\python rag\avalia_embeddings.py
   .venv\Scripts\python rag\avalia_hibrida.py
   ```
3. Teste dos LLM e dos juízes (prompt v1 congelado; contexto fixo do Qwen3-Embedding 8B na A):
   ```
   .venv\Scripts\python rag\testa_prompt.py
   .venv\Scripts\python rag\avalia_llm.py
   .venv\Scripts\python rag\avalia_juiz.py --juiz gpt-oss-120b
   .venv\Scripts\python rag\avalia_juiz.py --juiz gpt-oss-20b
   ```
   Com o Groq, o juiz para de forma limpa no limite diário (200 000 tokens): basta voltar a correr no dia seguinte. Com `--espera`, fica à espera do tempo que o Groq indica e continua sozinho.

   O mesmo teste na B e na C usa os 5 primeiros excertos das experiências B e C (passo 5), por isso corre-se depois delas. As respostas do Gemma 4 vêm das experiências, porque o prompt e os excertos são os mesmos:
   ```
   .venv\Scripts\python rag\avalia_llm.py --config B
   .venv\Scripts\python rag\avalia_llm.py --config C
   .venv\Scripts\python rag\avalia_juiz.py --juiz gpt-oss-120b --config B --espera
   .venv\Scripts\python rag\avalia_juiz.py --juiz gpt-oss-120b --config C --espera
   ```
   As tabelas para o grupo, no formato do E3 (embeddings em A, B e C; LLM com a correção em pontos em cada configuração e o total em 72), saem em `experiments\E1\tabelas_grupo_<juiz>.md`:
   ```
   .venv\Scripts\python rag\tabelas_grupo.py --juiz gpt-oss-120b
   ```
4. Piloto do juiz (folha às cegas; depois de preenchida, a concordância com os juízes):
   ```
   .venv\Scripts\python rag\piloto.py cria
   .venv\Scripts\python rag\piloto.py compara experiments\E1\piloto\folha_piloto.csv
   ```
5. Experiências finais. Cada pasta tem um `config.json` com o embedding, o LLM, o juiz, a frase de abstenção e o formato das citações. A e B antes da C, que escolhe os excertos pela regra do plano:
   ```
   .venv\Scripts\python rag\experiencia.py experiments\E1\A\config.json experiments\E1\B\config.json experiments\E1\C\config.json
   .venv\Scripts\python rag\experiencia.py experiments\E1\A\config.json experiments\E1\B\config.json experiments\E1\C\config.json --so-juiz --espera
   .venv\Scripts\python rag\analise_erros.py
   ```
   O `--so-juiz` avalia as respostas já geradas, e as que já foram avaliadas no teste dos LLM com a mesma pergunta, os mesmos excertos e a mesma resposta saem da cache do Groq.
6. Tabelas e figuras para o relatório, só a partir dos ficheiros de resultados (não corre modelos nem juízes). As figuras marcadas na secção 8 do notebook guardam-se em `docs\figuras\` (PNG a 300 dpi e PDF):
   ```
   .venv\Scripts\python -m jupyterlab analise\exploracao.ipynb
   .venv\Scripts\python -m nbconvert --to notebook --execute --inplace analise\exploracao.ipynb
   ```

### Reconstruir a base de conhecimento

O texto limpo está em `kb/E1/text/` (UTF-8, NFC, LF; congelado desde 25/10, e as posições dos trechos dependem dele). Para o refazer a partir dos originais: descarregar os PDF dos URL de `kb/E1/catalog_E1.jsonl` para `kb/E1/raw/` (como em `kb/E1/sources_E1.md`) e correr `python scripts\pdf_para_txt.py`, que extrai as partes de `scripts/partes_E1.json` e diz «igual» quando o `.txt` coincide. O processo está descrito em `docs/processo_E1.md`.

## Estrutura

```
kb/E1/                       base de conhecimento: text/ (36 .txt), catalog_E1.jsonl, sources_E1.md, revisao/
tests/questions_E1.jsonl     as 15 perguntas (8 factual, 4 multi_doc, 3 unanswerable)
tests/test_*.py              testes da métrica, do RRF e do BM25
scripts/                     construção da base e das perguntas (pdf_para_txt.py, perguntas_E1.py, rever_embeddings.py)
rag/                         o pipeline
  comum.py                     caminhos, catálogo, tokenizador
  excertos.py                  excertos A e B
  metricas.py                  Recall@5 e MRR@5 (regra do E1) e a regra do E2, só para comparar
  embeddings.py, indice.py     embeddings pelo Ollama e base vetorial ChromaDB
  bm25.py, pesquisa.py         BM25 e pesquisa densa, lexical e híbrida (RRF)
  prompt_geracao.py            prompt v1, frase de abstenção e formatos de citação (num só sítio)
  geracao.py                   LLM pelo Ollama e verificações em código
  prompt_juiz.py, juiz.py      prompt e esquemas do juiz (grelha comum) e chamadas ao juiz
  cliente_groq.py              API do Groq com cache, esperas e limites
  avalia_embeddings.py, avalia_hibrida.py, avalia_llm.py, avalia_juiz.py, testa_prompt.py   testes dos modelos
  piloto.py                    folha às cegas e concordância com os juízes
  experiencia.py               experiências finais A, B e C a partir do config.json
  analise_erros.py             análise de erros por pergunta e experiência
  tabelas_grupo.py             tabelas para o grupo, no formato do E3
experiments/E1/
  excertos_A.jsonl, excertos_B.jsonl (+ .json com os parâmetros e as estatísticas)
  modelos/embeddings/<modelo>_<A|B>/   config.json, results.jsonl; resumo.md
  modelos/hibrida/                     configuração C com cada embedding; resumo.md
  modelos/llm/<modelo>/                config.json, results.jsonl, juiz_<juiz>.jsonl; contexto.jsonl; resumo*.md
  modelos/llm_B/, modelos/llm_C/       o mesmo teste com os excertos das experiências B e C
  piloto/                              folha_piloto.csv e chave_piloto.json
  A/, B/, C/                           config.json, results.jsonl, juiz_<juiz>.jsonl, resumo.md
  resumo_ABC.md, analise_erros.md, analise_erros.csv, tabelas_grupo_<juiz>.md
analise/exploracao.ipynb     tabelas e figuras para o relatório (lê os resultados acima)
docs/                        processo da base (processo_E1.md), resumos do trabalho e figuras/ (exportadas do notebook)
```

Fora do git: `.env`, `.venv/`, `indices/`, `cache/`, `kb/E1/raw/` e `kb/E1/pdf/`.
