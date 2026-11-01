# Revisão da seleção do E1 com embeddings

Data: 30/10/2026. Modelo: `Qwen/Qwen3-Embedding-0.6B`. Frases do tema: 32 do E1 e 20 de outros temas (`scripts/temas_E1.txt`).

Método: cada parágrafo do texto limpo (com pelo menos 15 palavras, juntando os mais curtos) recebe a nota «média das 3 maiores semelhanças de cosseno às frases do E1 menos a média das 3 maiores às frases dos outros temas», suavizada com os 2 parágrafos vizinhos de cada lado. O limiar é o que melhor separa o núcleo atual do texto que ficou fora (índice de Youden, pesado pelas palavras). Os desacordos entre a nota e a seleção foram revistos à mão.

| | Valor |
|---|---|
| Parágrafos analisados | 20 079 (47 documentos; os 8 excluídos não entram) |
| Limiar da nota | 0.1076 |
| Palavras do núcleo acima do limiar | 72% |
| Palavras de fora do núcleo acima do limiar | 39% |
| **Palavras relevantes segundo os embeddings** | **357 131** |
| ... dentro do núcleo | 147 283 |
| ... nas partes opcionais | 49 410 |
| ... fora da seleção | 160 438 |
| Palavras do núcleo com nota baixa | 58 168 |
| Casos de desacordo com 60 palavras ou mais | 783 (221 para tirar?, 562 para juntar?); os 80 maiores estão no `desacordos.csv` |
| Desacordos mais pequenos, não revistos | 327 (9 509 palavras) |
