Embeddings (Recall@5 e MRR@5; C = A + BM25 por RRF, k = 60)
Modelo	A: Recall@5	A: MRR@5	B: Recall@5	B: MRR@5	C: Recall@5	C: MRR@5
qwen3-embedding-4b	0,694	0,632	0,597	0,479	0,625	0,597
qwen3-embedding-8b	0,681	0,500	0,625	0,561	0,528	0,576
embeddinggemma-sem-prefixos (variante)	0,611	0,482	0,389	0,417	0,625	0,507
bge-m3	0,569	0,507	0,444	0,429	0,556	0,531
embeddinggemma-titulo (variante)	0,542	0,417	0,486	0,454	0,542	0,514
embeddinggemma	0,514	0,382	0,403	0,454	0,542	0,472
qwen3-embedding-0.6b	0,500	0,396	0,458	0,326	0,583	0,514

LLM, correção em pontos (juiz gpt-oss-120b)
Modelo	A	B	C	Total em 72	Fidelidade	Sem suporte	Citações (0 a 2)	Segundos por resposta
Qwen3.5 9B	17	18	15	50	0,89	16	1,67	2,7
AMALIA 9B	16	18	13	47	0,74	30	1,16	2,9
Gemma 4 12B	18	14	9	41	0,93	8	1,74	3,0
Ministral 3 14B	16	12	13	41	0,90	11	1,59	4,0

Números para a leitura:
A: 67 pontos somando os 4 LLM; perguntas sem nenhum 2: E1-01 (1/1/1/1), E1-03 (1/1/1/1), E1-05 (0/1/0/0), E1-10 (1/1/1/1)
B: 62 pontos somando os 4 LLM; perguntas sem nenhum 2: E1-08 (0/0/0/0), E1-09 (0/1/1/0), E1-10 (0/0/1/0)
C: 50 pontos somando os 4 LLM; perguntas sem nenhum 2: E1-01 (1/1/1/1), E1-03 (0/0/0/0), E1-05 (0/0/0/0), E1-09 (0/1/0/1), E1-10 (1/1/1/1), E1-12 (0/0/0/1)
Qwen3.5 9B − AMALIA 9B: 3 pontos; diferenças por pergunta: E1-02 na A -2, E1-12 na B +2, E1-05 na A +1, E1-06 na A +1, E1-09 na A +1, E1-06 na B -1, E1-10 na B -1, E1-06 na C +1, E1-09 na C +1
Qwen3.5 9B: só a frase de abstenção em 2 de 9 respostas sem resposta; 2,70 s por resposta; 6,6 GB no Ollama
AMALIA 9B: só a frase de abstenção em 0 de 9 respostas sem resposta; 2,85 s por resposta; 5,6 GB no Ollama
Gemma 4 12B: só a frase de abstenção em 6 de 9 respostas sem resposta; 2,99 s por resposta; 8,0 GB no Ollama
Ministral 3 14B: só a frase de abstenção em 6 de 9 respostas sem resposta; 3,97 s por resposta; 9,1 GB no Ollama
