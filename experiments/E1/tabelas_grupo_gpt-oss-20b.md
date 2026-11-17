Embeddings (Recall@5 e MRR@5; C = A + BM25 por RRF, k = 60)
Modelo	A: Recall@5	A: MRR@5	B: Recall@5	B: MRR@5	C: Recall@5	C: MRR@5
qwen3-embedding-4b	0,694	0,632	0,597	0,479	0,625	0,597
qwen3-embedding-8b	0,681	0,500	0,625	0,561	0,528	0,576
embeddinggemma-sem-prefixos (variante)	0,611	0,482	0,389	0,417	0,625	0,507
bge-m3	0,569	0,507	0,444	0,429	0,556	0,531
embeddinggemma-titulo (variante)	0,542	0,417	0,486	0,454	0,542	0,514
embeddinggemma	0,514	0,382	0,403	0,454	0,542	0,472
qwen3-embedding-0.6b	0,500	0,396	0,458	0,326	0,583	0,514

LLM, correção em pontos (juiz gpt-oss-20b)
Modelo	A	B	C	Total em 72	Fidelidade	Sem suporte	Citações (0 a 2)	Segundos por resposta
Gemma 4 12B	18	14	12	44	0,97	3	1,88	3,0
Qwen3.5 9B	15	16	13	44	0,93	8	1,82	2,7
AMALIA 9B	17	14	13	44	0,78	20	1,33	2,9
Ministral 3 14B	19	12	12	43	0,94	7	1,84	4,0

Números para a leitura:
A: 69 pontos somando os 4 LLM; perguntas sem nenhum 2: E1-01 (1/1/1/1), E1-03 (1/1/1/1), E1-05 (0/0/0/0)
B: 56 pontos somando os 4 LLM; perguntas sem nenhum 2: E1-08 (0/0/0/0), E1-09 (0/1/1/1), E1-10 (0/0/0/0)
C: 50 pontos somando os 4 LLM; perguntas sem nenhum 2: E1-01 (1/1/1/1), E1-03 (1/0/0/0), E1-05 (0/0/0/0), E1-09 (0/0/0/1), E1-11 (1/1/1/1), E1-12 (0/0/0/0)
Gemma 4 12B − Qwen3.5 9B: 0 pontos; diferenças por pergunta: E1-02 na C -2, E1-09 na A +1, E1-10 na A +1, E1-11 na A +1, E1-02 na B -1, E1-03 na B -1, E1-09 na B -1, E1-11 na B +1, E1-03 na C +1
Gemma 4 12B: só a frase de abstenção em 6 de 9 respostas sem resposta; 2,99 s por resposta; 8,0 GB no Ollama
Qwen3.5 9B: só a frase de abstenção em 2 de 9 respostas sem resposta; 2,70 s por resposta; 6,6 GB no Ollama
AMALIA 9B: só a frase de abstenção em 0 de 9 respostas sem resposta; 2,85 s por resposta; 5,6 GB no Ollama
Ministral 3 14B: só a frase de abstenção em 6 de 9 respostas sem resposta; 3,97 s por resposta; 9,1 GB no Ollama
