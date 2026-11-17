# Relatório individual do E1: esqueleto

Secções pedidas no ponto 9 do enunciado e, em cada uma, o material que já existe (atualizado a 16/11). Limite de 30 páginas, sem os elementos pré-textuais, as referências e os anexos; letra NewsGotT com pelo menos 10 pt. Entrega a 23/11 às 23:59.

## 0. Elementos pré-textuais
Capa, resumo, índice. Não contam para as 30 páginas.

## 1. Introdução
- Enquadramento: Guimarães, Capital Verde Europeia 2026; a área E1 (resíduos e economia circular: separação, encaminhamento, reutilização e reparação).
- Objetivo da componente individual e organização do relatório.
- Material: enunciado (secções «Enquadramento» e «Componente individual»).

## 2. Base de conhecimento: recolha, seleção e construção
- Números: 55 PDF lidos (2 932 páginas, 845 482 palavras); 36 documentos na base (21 de Guimarães, 15 nacionais), 216 272 palavras; 8 excluídos e porquê.
- Pesquisa das fontes, escolha das partes úteis, extração e limpeza, OCR de 2 PDF, revisão da seleção com embeddings (80 maiores desacordos), atualização do 104 (UNILEX), texto congelado a 25/10.
- Formatos: UTF-8, NFC, LF; metadados do enunciado no catálogo.
- Material: `docs/processo_E1.md` (cronologia e decisões), `kb/E1/sources_E1.md`, `kb/E1/catalog_E1.jsonl`, `kb/E1/revisao/resumo.md` e `decisoes_30-10.csv`, `kb/E1/relatorio_palavras.csv`, `scripts/pdf_para_txt.py` e `partes_E1.json`.

## 3. Conjunto de teste
- 15 perguntas: 8 factual, 4 multi_doc, 3 unanswerable («quase-respostas»); resposta de referência; trechos marcados por posição no texto original, com SHA-1 do `.txt`; grupos de trechos alternativos (E1-04).
- Regras de 20/10 para os trechos; validação automática (0 erros, 1 aviso: trecho de 607 caracteres na E1-10); revisão cruzada; perguntas sem resposta das outras áreas testadas na base do E1.
- Material: `tests/questions_E1.jsonl`, `scripts/perguntas_E1.py` (`valida`, `procura`), `docs/processo_E1.md` (secção 12).
- E1-05: decidido a 8/11 não acrescentar o PAPERSU como trecho alternativo (é de 2024 e com outras condições); ver a secção 8.
- Referências e juiz (revisto a 15/11): na E1-03, a referência só tem a recolha gratuita pela Vitrus (E1-014), mas o regulamento (E1-004, art. 38.º) também manda levar os volumosos aos ecocentros da Resinorte. As respostas que vão por aí levavam 0 por «contradizer» a referência, como na E2-02. Decidido a 15/11 (versão final, que não volta a mudar): «Há duas formas, e qualquer uma basta: contactar a Vitrus Ambiente para agendar a recolha, que é gratuita, ou levá-lo a um ecocentro», sem nomear a entidade, para valer tanto para os ecocentros de Aldão e Ponte como para os da Resinorte. As respostas à E1-03 foram reavaliadas pelos dois juízes; comparar as notas de antes e de depois (`docs/pipeline_E1_15-11.md`). Limitação dos juízes: os dois leem as duas formas como obrigatórias, apesar do «qualquer uma basta». Na experiência B, a resposta só com a Vitrus e a recolha gratuita desce de 2 para 1 com o 120b (e o mesmo acontece com o 20b no teste dos LLM). Na E1-10, a referência fica como está, mas tem pormenores que a pergunta não pede (os 120 dias de transição), e a falta deles tira 1 ponto, por igual, a quase todas as respostas.

## 4. Arquitetura e implementação do pipeline
- Diagrama do pipeline: excertos → embeddings (Ollama) → ChromaDB → pesquisa densa / BM25 / RRF → prompt → LLM → verificações em código → juiz.
- Excertos: regras (frases inteiras, cortes nas linhas e nos fins de frase, sobreposição por frases inteiras), tokenizador do bge-m3 com revisão fixa; estatísticas de A e B (774 e 2 014 excertos; média de 465 e 174 tokens; na B, a sobreposição efetiva é de 4 tokens em média) e o teto do Recall@5 (1 em A e B).
- Base vetorial: ChromaDB, cosseno, HNSW igual à pesquisa exata nas 150 pesquisas; metadados (título, entidade, URL); versão do Ollama guardada em cada coleção.
- Pesquisa híbrida: BM25 Okapi (k1 = 1,5; b = 0,75; IDF do Lucene; stopwords e stemmer Snowball do NLTK), RRF com k = 60 e os 50 primeiros de cada lista.
- Geração: prompt v1 (contrato de 20/10), teste com 2 perguntas inventadas e porque se retirou o lembrete; parâmetros (temperatura 0, semente, sem raciocínio, penalizações a zero); frase de abstenção e formato das citações num só sítio.
- Verificações em código: abstenção com a frase fixa, citações no formato, ids fora dos excertos.
- Material: `README.md`, `rag/*.py` (cabeçalhos explicam cada decisão), `experiments/E1/excertos_*.json`, `tests/`.

## 5. Escolha e comparação dos modelos
- Critérios do enunciado: qualidade, latência, custo e privacidade (todos locais pelo Ollama, custo zero; o juiz pelo Groq, gratuito).
- Escolha do grupo (15/11): Qwen3-Embedding 8B, Gemma 4 12B e juiz gpt-oss-120b, iguais nos quatro elementos; frase de abstenção e citações por documento, como a 20/10. O Gemma 4 foi confirmado a 16/11, com as tabelas do 120b das quatro áreas.
- **Matriz de decisão do grupo** (Luís, 17/11, «para justificarmos as escolhas dos modelos»). São números do grupo, com as quatro áreas juntas. Os pesos são do grupo, porque o enunciado dá os critérios (secção 8) mas não os pesos. Tudo na escala de 0 a 10.
  - **LLM:** correção 35 % (pontos em 288), fidelidade 35 % (× 10), citações 20 % (× 5) e abstenção 10 % (respostas só com a frase, em 18, porque só o E1 e o E3 a contaram). Dá Gemma 4 8,12, Ministral 7,71, Qwen3.5 7,49 e AMALIA 6,04.
  - **Correção por área** (E1, E2, E3, E4 → total em 288): Qwen3.5 50, 38, 60, 55 → 203; Ministral 41, 38, 64, 49 → 192; Gemma 4 41, 35, 59, 46 → 181; AMALIA 47, 32, 58, 40 → 177. O Gemma 4 tem menos pontos de correção, mas é o melhor na fidelidade, nas citações e nas afirmações sem suporte nas quatro áreas (no E4, empata com o Qwen3.5 nas afirmações sem suporte).
  - **Embeddings** (A e B; em cada coluna, o melhor modelo fica com 10): Recall@5 40 %, consistência 30 % (soma das posições em cada tema e métrica), MRR 20 % e estabilidade 10 % (quanto o Recall@5 varia entre a A, a B e a C). Dá 8B 9,64, 4B 8,95, EmbeddingGemma 8,07, bge-m3 7,74 e 0.6B 6,36.
  - **Sensibilidade:**
    - Nos LLM, sem a abstenção (40/40/20), o Gemma 4 e o Qwen3.5 empatam (8,13 e 8,14).
    - Nos embeddings, o que separa o 8B do 4B é a consistência: sem ela, fica 9,49 contra 9,42. Com o Recall@5 e o MRR a pesar o mesmo, passa à frente o 4B (9,86 contra 9,76).
  - **Fora da nota:**
    - Latência: cada um põe os seus tempos no relatório. A ordem dos LLM muda de PC para PC (no do Lobo, o mais rápido é o Qwen3.5), e só o Ministral é o mais lento nos três que mediram.
    - Custo: igual nos quatro, porque todos correm localmente.
    - Afirmações sem suporte: já estão na fidelidade. Nas quatro áreas: Gemma 4 14, Qwen3.5 31, Ministral 39 e AMALIA 92.
  - Falta o Luís dizer como reportamos a matriz, para ficar igual nos quatro relatórios.
- Embeddings: tabela com as duas regras (E1 e E2), incluindo o 4B e as variantes do EmbeddingGemma; as duas regras dão o mesmo Recall@5 (só 8 de 1 750 pares mudam); a sensibilidade do MRR a trocas de posição entre pontuações quase iguais (versão do Ollama).
- No E1, o melhor embedding na A é o Qwen3-Embedding 4B (Recall@5 0,694 e MRR@5 0,632, contra 0,681 e 0,500 do 8B); na B é o 8B (0,625 e 0,561). Discutir porque o grupo ficou com o 8B (um modelo comum às quatro áreas) e o que se perde no E1.
- LLM: os 4 LLM em A, B e C (15 perguntas × 3 configurações cada), com os excertos do 8B; verificações automáticas e latência; grelha com o juiz 20b (as 180 respostas) e com o 120b; o efeito da primeira resposta depois de carregar o modelo.
- Tabelas do grupo, no formato do E3 (refeitas a 16/11, com a referência final da E1-03): correção em pontos por configuração (24 em cada) e total em 72, fidelidade, afirmações sem suporte, citações, segundos por resposta e tamanho no Ollama.
  - Com o 20b (completo): Gemma 4 44 (A 18, B 14, C 12), Qwen3.5 44 (15, 16, 13), AMALIA 44 (17, 14, 13), Ministral 43 (19, 12, 12), ou seja, 1 ponto de diferença.
  - Com o 120b (completo a 16/11): Qwen3.5 50 (17, 18, 15), AMALIA 47 (16, 18, 13), Gemma 4 41 (18, 14, 9), Ministral 41 (16, 12, 13).
- Juízes: problemas encontrados no 20b (esquema JSON, citações inventadas, ciclos) e como se resolveram. Concordância 20b–120b, com a referência final da E1-03: na A, a mesma correção em 53 de 60 respostas (kappa quadrático 0,84; 0,87 antes da E1-03 nova); na B, 49 de 60 (0,77); na C, 53 de 60 (0,89). O 120b apanha contradições que o 20b deixa passar (Ministral na E1-02). Concordância com as notas humanas no piloto, quando houver.
- Material: `experiments/E1/modelos/embeddings/resumo.md` (e `resumo_ollama-0.40.14.md`), `modelos/hibrida/resumo.md`, `modelos/llm/resumo.md`, `modelos/llm*/resumo_grelha_gpt-oss-20b.md` e `resumo_grelha_gpt-oss-120b.md` (A, B e C), `experiments/E1/tabelas_grupo_gpt-oss-20b.md` e `tabelas_grupo_gpt-oss-120b.md`, `piloto/concordancia.md` (quando houver as notas humanas).

## 6. Configuração das experiências e resultados (A, B e C)
- Protocolo: o mesmo embedding e o mesmo LLM nas três; k = 5; regra para escolher a melhor de A e B fixada antes; a C sobre a melhor.
- Tabela: Recall@5, MRR@5, cobertura das multi_doc, verificações em código, grelha do juiz e latência.
- Material: `experiments/E1/A|B|C/config.json` (parâmetros e versões completos), `results.jsonl`, `juiz_gpt-oss-120b.jsonl`, `resumo.md`, `experiments/E1/resumo_ABC.md`.
- Modelos fechados a 15/11 (`"provisional": false`). As respostas são as de 8/11, já com esses modelos, e o juiz é o 120b, com as 45 respostas avaliadas a 15/11. Na B e na C, as avaliações saíram da cache do teste dos LLM, exceto a correção da E1-03, refeita com a referência final.
- Resultados (`resumo_ABC.md`): Recall@5 A 0,681, B 0,625, C 0,528; MRR@5 0,500, 0,561, 0,576; correção média nas 12 perguntas com resposta 1,33, 1,17 e 0,75 (20, 20 e 13 pontos nas 15); fidelidade 0,97, 0,88 e 0,96; latência 3,2, 2,4 e 3,3 s. A e B empatam nas 15 por causa da E1-14 (a B acaba com a frase de abstenção, a A não).
- **Nota de reprodutibilidade:**
  - Entre o Ollama 0.40.14 (teste dos LLM, 6/11) e o 0.40.15 (experiência A, 8/11), a ordem dos 5 excertos da A mudou em 6 das 15 perguntas (E1-02, E1-04, E1-11, E1-13, E1-14 e E1-15). Os 5 excertos são sempre os mesmos.
  - Isso quase não mexe nas métricas: o Recall@5 fica em 0,681, e o MRR@5 passa de 0,493 para 0,500 (só a E1-02, que passa de 0,25 para 0,33).
  - Mesmo assim, o Gemma 4 deu outra resposta em 8 das 15 perguntas, e em 5 delas com os mesmos excertos pela mesma ordem. Por isso, os números do Gemma na A do teste e na experiência A não coincidem, e as avaliações do juiz não se puderam reaproveitar.
  - Daí guardar a versão do Ollama em cada coleção e em cada `config.json`, e não misturar versões numa mesma tabela.

## 7. Análise comparativa das configurações
- A contra B: Recall@5 maior na A em todos os modelos; contexto dado ao LLM (cerca de 3 000 tokens na A e 1 550 na B) e latência.
- C: a híbrida baixa o Recall@5 dos embeddings mais fortes (o BM25 sozinho tem 0,375 na A) e ajuda os mais fracos; discussão do RRF sem pesos.
- Pelos LLM: somando os 4 com o 20b, a A tem 69 pontos, a B 56 e a C 50 (com o 120b, a A 67, a B 62 e a C 50). Os quatro falham nas mesmas perguntas, por isso a configuração pesa mais do que o LLM.
- Limitações: 12 perguntas com resposta (uma factual vale 0,083 no Recall@5).

## 8. Análise de erros
- Falhas de recuperação: E1-05 (nenhum embedding; o PAPERSU descreve uma medida parecida de 2024), E1-03 (o folheto da Vitrus não aparece); quase-acertos entre o 6.º e o 10.º.
- Respostas incorretas ou não fundamentadas, erros de citação, perguntas sem resposta (abstenção por outras palavras no AMALIA; resposta lateral do Gemma na E1-14).
- Contagem por tipo de falha (notebook, secção 7, juiz 120b):
  - Nas experiências A, B e C: recuperação 6, 6 e 8 de 12; resposta sem suporte 1 de 12, 5 de 11 e 2 de 11; citação errada nas mesmas respostas; abstenção indevida 1, 2 e 2 de 12, e só uma delas (na C) com o trecho certo nos excertos.
  - No teste dos LLM (A + B + C): o AMALIA tem 21 de 43 respostas sem suporte e 28 com citações erradas (5 sem nenhuma citação), contra 8 a 10 e 9 a 13 nos outros, e nenhuma abstenção indevida (os outros têm 3 a 5 de 36).
- Material: `experiments/E1/analise_erros.md` e `analise_erros.csv` (problemas por tipo), `rag/analise_erros.py`, `analise/exploracao.ipynb` (secção 7, figura `7_falhas_por_tipo`).

## 9. Conclusões e trabalho futuro

## Referências
- Enunciado; decisões do grupo (20/10 e 30/10); grelha comum; model cards (Qwen3-Embedding, bge-m3, EmbeddingGemma); Cormack et al. (2009) para o RRF; Zheng et al. (2023) e Panickssery et al. (2024) para o juiz.

## Anexos
- **Declaração de Utilização de Ferramentas de IA** (obrigatório): a partir do doc «Registo de uso de IA (IAG E1)».
- Grelha do juiz e prompts (`rag/prompt_geracao.py`, `rag/prompt_juiz.py`).
- As 15 perguntas com as respostas de referência.
