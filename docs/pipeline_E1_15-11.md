# Pipeline RAG do E1: o que foi feito a 15/11/2026

Continua o `pipeline_E1_08-11.md`. Trabalho feito com o Claude (Anthropic) no Claude desktop. Nada foi commitado.

## 1. Decisões novas

1. **Modelos fechados pelo grupo:** Qwen3-Embedding 8B, Gemma 4 12B e o juiz gpt-oss-120b, que eram a escolha provisória de 8/11. A frase de abstenção e o formato das citações (por documento, `[E1-003]`) ficam como a 20/10.
2. **`.gitignore`:** a regra `modelos/` passou a `/modelos/`. Era para pesos de modelos na raiz, que não existem, e apanhava também `experiments/E1/modelos/`. Essa pasta, com os testes dos embeddings, da híbrida e dos LLM e as avaliações dos dois juízes (122 ficheiros, 2,4 MB, sem chaves), passa a ir para o git. O `.env`, o `cache/` e o `indices/` continuam de fora.
3. **Experiências finais:** os `config.json` de A, B e C ficaram com `"provisional": false` e com uma nota que regista a decisão do grupo. As respostas são as de 8/11, que já usavam estes modelos.
4. **`experiencia.py --so-juiz --espera`:** no limite diário do Groq, espera e continua, como o `avalia_juiz.py`.
5. **Prioridade no Groq:** primeiro as experiências A, B e C e depois o teste dos LLM (A, B e C), no mesmo processo.
6. **Resposta de referência da E1-03 completada** (secção 3).
7. **Desvio: o Ollama atualizou-se sozinho para a 0.40.16** a 14/11, às 14:31 (`%LOCALAPPDATA%\Ollama\app-1.log`).
   - Os embeddings e as respostas não mudam: são todos da 0.40.14 (teste dos LLM na A, 6/11) ou da 0.40.15 (experiências e teste na B e na C, 8/11), como fica no `config.json` de cada um.
   - As avaliações do 20b feitas a partir daí, pelo menos as 12 da E1-03 (15/11), correram na 0.40.16. Os ficheiros do juiz não guardam a versão do Ollama.

## 2. Juiz 120b nas experiências A, B e C

- **B e C:** as 30 avaliações saíram todas da cache do Groq (60 pedidos da cache, 0 novos), porque as respostas e os excertos são os do teste dos LLM.
- **A:** 1 avaliação saiu da cache (E1-01) e as outras 14 precisam de avaliação nova. O teste dos LLM na A usou o contexto de 6/11 (Ollama 0.40.14), e a experiência A o de 8/11 (0.40.15).
  - Os 5 excertos são os mesmos em todas as perguntas, mas em 6 vêm por outra ordem.
  - O Recall@5 fica em 0,681, e o MRR@5 passa de 0,493 para 0,500.
  - O Gemma 4 deu outra resposta em 8 das 15 perguntas, 5 delas com os mesmos excertos pela mesma ordem.
- **Groq:** com o limite de 200 000 tokens por 24 horas, cabem cerca de 33 respostas por dia. As 29 respostas que faltam na C do teste dos LLM (AMALIA e Ministral) acabam amanhã.
- **Feito a 15/11, às 22:35:** as 45 respostas das três experiências estão avaliadas pelo 120b, todas com a referência final da E1-03 (`experiments/E1/resumo_ABC.md`).

  | Exp. | Recall@5 | MRR@5 | Correção (média nas 12 com resposta) | Correção (pontos nas 15) | Fidelidade | Citações | Latência (s) |
  |---|---|---|---|---|---|---|---|
  | A | 0,681 | 0,500 | 1,33 | 20 | 0,97 | 1,92 | 3,2 |
  | B | 0,625 | 0,561 | 1,17 | 20 | 0,88 | 1,54 | 2,4 |
  | C | 0,528 | 0,576 | 0,75 | 13 | 0,96 | 1,82 | 3,3 |

  - A A fica à frente da B nas 12 perguntas com resposta (16 pontos contra 14) e empata nas 15, por causa da E1-14 (valor do depósito, sem resposta na base). Nas duas, o Gemma 4 descreve o regime do depósito (E1-104). Na B acaba com a frase de abstenção «para indicar o valor exato» e leva 2; na A não a diz e leva 0.
  - A C tem 0 a mais do que a A na E1-02, E1-03, E1-08 e E1-12; na E1-12 é uma falsa abstenção (1 de 9).
  - Na B, a fidelidade é a mais baixa: há afirmações não suportadas em 9 perguntas.

## 3. Respostas de referência e notas do juiz

Revistas as respostas com fidelidade de pelo menos 0,75 e correção abaixo de 2, no teste dos LLM e nas experiências.

- **E1-03 (sofá): a referência está incompleta, como a da E2-02.**
  - A referência só diz para contactar a Vitrus, que recolhe de graça (E1-014).
  - O regulamento municipal (E1-004, art. 38.º) diz que o detentor leva os volumosos aos ecocentros da Resinorte (n.º 2). Se não tiver meios, pede a remoção ao Município com pelo menos 7 dias de antecedência (n.º 3).
  - As respostas que mandam levar o sofá a um ecocentro têm apoio na base, mas levam 0 por «contradizer» a referência (Gemma 4 e AMALIA no teste na A). Com uma referência completa, levariam 1, por não dizerem que a recolha é gratuita.
  - Correção ao 8/11: o excerto do E1-004 que a pesquisa traz (`E1-004_A0015`) só define os «monstros», mas o art. 38.º do mesmo documento diz como se recolhem.
  - **Decisões do Lobo (15/11), em dois passos:**
    - Intermédia: acrescentar «ou levá-lo a um ecocentro da Resinorte».
    - Final: o fim da referência passou a «Há duas formas, e qualquer uma basta: contactar a Vitrus Ambiente para agendar a recolha, que é gratuita, ou levá-lo a um ecocentro.» Fica sem «da Resinorte», para valer tanto para os ecocentros de Aldão e Ponte (E1-001) como para os da Resinorte (E1-004), e para uma resposta só com a Vitrus não perder pontos. **Esta referência não volta a mudar.**
    - Em `tests/questions_E1.jsonl` só mudou esse campo, e a validação dá 0 erros e 1 aviso, o mesmo de antes.
    - Os trechos da E1-03 ficam os do E1-014, por isso o Recall@5 não muda. O art. 38.º do E1-004 não entra como trecho alternativo, e nenhuma pesquisa o trouxe nos 5 primeiros.
    - Na folha do piloto (item P05), também mudou só a resposta de referência; as notas continuam vazias.
  - **Reavaliação:** as avaliações da E1-03 dos dois juízes, no teste dos LLM e nas experiências, refazem-se com a referência final.
  - **Correção da E1-03 com o 20b** (teste dos LLM; original → intermédia → final):

    | LLM | A | B | C |
    |---|---|---|---|
    | Gemma 4 | 0 → 0 → 1 | 2 → 2 → 1 | 0 → 0 → 1 |
    | Qwen3.5 | 0 → 0 → 1 | 2 → 2 → 2 | 0 → 0 → 0 |
    | AMALIA | 0 → 0 → 1 | 2 → 2 → 2 | 0 → 0 → 0 |
    | Ministral | 0 → 1 → 1 | 2 → 1 → 0 | 0 → 0 → 0 |
    | **Soma** | 0 → 1 → 4 | 8 → 7 → 5 | 0 → 0 → 1 |

    - Na A, as quatro respostas que mandam o sofá para um ecocentro passam de 0 a 1. É o que se esperava: dizem como, mas não quanto custa.
    - **O 20b não segue o «qualquer uma basta».** O Gemma na B responde só com a Vitrus e a recolha gratuita, que é a resposta certa, e desce de 2 para 1, por «faltar a opção do ecocentro». O Ministral na B desce para 0, porque diz que a recolha é gratuita e depois que não encontrou informação sobre o custo.
    - Na C, nenhuma resposta fala de ecocentros nem da Vitrus, e o Gemma sobe para 1.
  - **Correção da E1-03 com o 120b** (teste dos LLM e experiências; original → final):
    - Notas originais no teste: na A, 0 para os 4 LLM; na B, 2, exceto o Ministral, com 1; na C, 0 para o Gemma, o Qwen e o AMALIA (o Ministral na C ainda não tinha sido avaliado). Nas experiências: B 2 e C 0.
    - Nas experiências (o Gemma 4):

      | Exp. | Original | Intermédia | Final | Resposta |
      |---|---|---|---|---|
      | A | — | 0 | 1 | Ecocentros de Aldão e Ponte; não encontra o custo |
      | B | 2 | — | 1 | Só a Vitrus, com recolha gratuita |
      | C | 0 | — | 0 | Tarifa de resíduos por alojamento, não a do sofá |

    - **O 120b também não segue o «qualquer uma basta».** Na B, a resposta tem a forma e o custo (Vitrus, gratuita) e desce de 2 para 1, por omitir «a alternativa de levar o sofá a um ecocentro». Na A, o 1 justifica-se por faltar o custo, mas o juiz diz que falta a Vitrus, «que é essencial na referência».
    - Os dois juízes leem as duas formas como obrigatórias, por isso a mudança da referência ajuda as respostas que vão aos ecocentros e castiga as que só têm a Vitrus, ao contrário do que se queria. A referência não volta a mudar (decisão do Lobo); fica como limitação dos juízes.
    - Só o pedido de correção é novo (1 por resposta, cerca de 900 tokens); o de fidelidade não depende da referência e sai da cache.
    - No teste dos LLM (16/11, quando o 120b acabou; original → final; «—» é uma resposta que ainda não tinha sido avaliada):

      | LLM | A | B | C |
      |---|---|---|---|
      | Gemma 4 | 0 → 1 | 2 → 1 | 0 → 0 |
      | Qwen3.5 | 0 → 1 | 2 → 2 | 0 → 0 |
      | AMALIA | 0 → 1 | 2 → 2 | 0 → 0 |
      | Ministral | 0 → 1 | 1 → 0 | — → 0 |
      | **Soma** | 0 → 4 | 7 → 5 | 0 → 0 |

    - As notas finais do 120b são as mesmas do 20b em 11 das 12 respostas. A exceção é o Gemma na C, com 0 no 120b e 1 no 20b. Na B, o Gemma (só a Vitrus) desce de 2 para 1 e o Ministral de 1 para 0, como com o 20b.
  - **Concordância 20b–120b na correção, com a referência final** (`rag/piloto.py`, função `kappa`; final a 16/11): na A, 53 de 60 (kappa quadrático 0,84; era 0,87 antes da E1-03 nova); na B, 49 de 60 (0,77); na C, 53 de 60 (0,89). No total, 155 de 180.
    - O `avalia_juiz.py` e o `experiencia.py` passam a guardar o SHA-1 da resposta de referência em cada avaliação (`reference_sha1`) e a refazê-la quando a referência muda. As avaliações anteriores, sem esse campo, contam como feitas com a referência atual.
- **E1-10: a referência tem mais do que a pergunta pede.** Os 120 dias de transição não respondem a «quando estava previsto começar». Mesmo assim, o juiz dá 1 a quase todas as respostas que não os referem. Com o 120b, nenhuma resposta à E1-10 tem 2, e só uma das 10 que não se abstêm refere os 120 dias (o AMALIA na A). Conferido a 16/11 com as 12 respostas do teste dos LLM já avaliadas. **Decisão do Lobo (15/11): a referência fica como está.** Registado na análise de erros (`NOTAS_REFERENCIA` em `rag/analise_erros.py`): a falta dos 120 dias tira 1 ponto, por igual, a quase todas as respostas.
- **Sem problema na referência:**
  - E1-02: o E1-014 põe a loiça partida nos indiferenciados, e as respostas que a mandam para os ecocentros estão erradas.
  - E1-08: os 250 € a 1 500 € são de outras infrações (art. 18.º, n.º 2).
  - E1-09: os −34% e +126% estão no E1-029. As respostas com quilos por habitante usam os números de 2022.
  - E1-01 e E1-06: faltam pormenores nas respostas, não na referência.

## 4. Análise de erros

`rag/analise_erros.py` refeito a 15/11 às 22:40, com as notas do 120b nas três experiências (45 linhas).
- Problemas mais frequentes: afirmações não suportadas na B (9 perguntas), correção 0 na C (7), pesquisa parcial na C (5), citações 1 na B (5), pesquisa parcial na A (4) e correção 1 na A (4).
- Na A: correção 0 em 3 perguntas (E1-05, E1-09 e E1-14) e afirmações não suportadas em 4.
- Cada pergunta com uma decisão sobre a referência tem agora uma «Nota sobre a referência»: a E1-03 (completada), a E1-05 (PAPERSU não entra) e a E1-10 (120 dias).

## 5. README e esqueleto do relatório

- **README:** os modelos fechados, o `--config B|C` do `avalia_llm.py` e do `avalia_juiz.py` (a correr depois das experiências B e C), o `--espera`, o `tabelas_grupo.py` e as pastas `modelos/llm_B` e `llm_C`.
- **Esqueleto:** a escolha do grupo, os LLM na B e na C, as tabelas do grupo, a concordância 20b–120b, o Qwen3-Embedding 4B como melhor na A no E1 (e o 8B na B), as notas sobre a E1-03 e a E1-10, e a diferença de contexto entre o teste dos LLM e a experiência A.

## 6. Notebook de exploração (`analise/exploracao.ipynb`)

Pedido do Lobo (15/11): tabelas e figuras para o relatório, só a partir dos ficheiros de resultados, sem correr modelos nem juízes. Instalados no `.venv` e fixados no `requirements.txt`: jupyter 1.1.1, pandas 3.1.1 e matplotlib 3.11.2.

- **Secções:** 1 base; 2 embeddings no E1; 3 escolha do embedding no grupo (só tabela); 4 LLM no E1 com os dois juízes; 5 concordância dos juízes; 6 experiências finais; 7 análise de erros por tipo de falha (feita a 16/11, quando o 120b acabou); 8 exportação para `docs/figuras/` (PNG a 300 dpi e PDF) das figuras marcadas em `MARCADAS`.
- **Escolhas feitas no notebook:**
  - Âmbito dos documentos pelo número: E1-0xx é de Guimarães (21) e E1-1xx nacional (15). As palavras contam-se como no `relatorio_palavras.csv` (dá os mesmos 104 017 e 112 255).
  - C no E1 = excertos A com pesquisa híbrida (`modelos/hibrida/<modelo>_A`).
  - Mapa da posição do primeiro acerto: regra do E1, até ao 10.º excerto registado (6.º a 10.º são os quase-acertos). Confere com o `hit_ranks` gravado até ao 5.º.
  - Tabela do grupo: no E1, o EmbeddingGemma é a variante com os prefixos do model card; os números das outras áreas são os da grelha do Pedro (15/11), copiados para o notebook.
  - LLM: as médias seguem as definições do `rag/avalia_juiz.py`. Onde o 120b ainda não avaliou as 15 respostas, as barras levam riscas, e um grupo sem nenhuma avaliação (o Ministral na C) fica sem barra e assinalado no título.
  - Experiências: o embedding, o LLM e o juiz leem-se do `config.json`, e o Recall@5 e o MRR@5 conferem com os gravados.
  - Cores fixas por modelo (paleta categórica validada para daltonismo). Os embeddings e os LLM nunca aparecem na mesma figura, por isso cada família usa as cores pela mesma ordem (o Gemma 4 tem o azul do Qwen3-Embedding 8B).
  - Letra das figuras: Segoe UI, porque a NewsGotT não está instalada neste PC. Se a instalares, o notebook usa-a.
  - Análise de erros (secção 7, juiz 120b): número de respostas por tipo de falha, nas experiências e, por LLM, no teste dos LLM (A + B + C). Uma resposta pode contar em mais do que um tipo.
    - Recuperação: Recall@5 abaixo de 1 nas 12 perguntas com resposta (nenhum trecho certo, ou só parte).
    - Resposta sem suporte: pelo menos uma afirmação sem suporte, nas respostas que não se abstêm.
    - Citação errada: nota de citações abaixo de 2, ou citações fora dos excertos, mal escritas ou nenhuma (detetadas em código), nas que não se abstêm.
    - Abstenção indevida: a frase de abstenção numa pergunta com resposta, separada pelo que estava nos excertos (com ou sem o trecho certo).
    - Na figura, o teste dos LLM fica sem a recuperação, porque os 4 LLM recebem os mesmos excertos.
- O notebook fica no git com as tabelas e as figuras já feitas (cerca de 1,1 MB).
- Corrido outra vez a 16/11, às 06:00, para o zip do relatório (o Ministral na C com 10 das 15 avaliações do 120b), e às 07:25, com o 120b completo e a secção 7. Já não há barras provisórias.

## 7. 16/11: o 120b acabou o teste dos LLM

- As últimas avaliações (Ministral na C) acabaram às 07:13, sem erros. As 180 respostas do teste dos LLM têm as notas dos dois juízes, e as 45 das experiências as do 120b.
- **Tabelas do grupo refeitas** (`rag/tabelas_grupo.py`):
  - 20b: a tabela era de 8/11, de antes da referência final da E1-03. Os totais passaram de A 65, B 59, C 49 para A 69, B 56, C 50. Por LLM: Gemma 4, Qwen3.5 e AMALIA 44, Ministral 43.
  - 120b: Qwen3.5 50, AMALIA 47, Gemma 4 41 e Ministral 41. Por configuração: A 67, B 62, C 50.
  - O `modelos/llm_C/resumo_grelha_gpt-oss-120b.md` refê-lo o `avalia_juiz.py` no fim.
- **Notas finais da E1-03 com o 120b no teste dos LLM e concordância na C:** secção 3. A afirmação sobre a E1-10 (nenhuma resposta com 2) confere.
- **Análise de erros por tipo de falha** (notebook, secção 7):
  - Nas experiências A, B e C: recuperação 6, 6 e 8 de 12; resposta sem suporte 1 de 12, 5 de 11 e 2 de 11; citação errada nas mesmas respostas (1, 5 e 2); abstenção indevida 1, 2 e 2 de 12, e só uma delas (na C) com o trecho certo nos excertos.
  - No teste dos LLM (A + B + C): respostas sem suporte 8 de 34 (Gemma 4), 10 de 33 (Qwen3.5), 21 de 43 (AMALIA) e 9 de 32 (Ministral). Citações erradas 9, 11, 28 e 13, pela mesma ordem: 5 respostas do AMALIA não têm citações, e nenhuma resposta tem citações fora dos excertos ou mal escritas. Abstenções indevidas 5, 3, 0 e 4 de 36.
- O esqueleto do relatório tem os números novos.

## 8. 17/11: depois da conversa do grupo

Revista a conversa do grupo até 17/11 (exportação do WhatsApp) contra o repositório.
- **Regra de 1 carácter:** é a do Pedro Gomes (E2), e o Luís usou-a também no E3, com o MRR até ao 10.º. O E1 e o E4 usam o MRR@5. A nota da secção 3 do notebook só falava do E3 e passou a dizer «E2 e E3». O nome «regra do E2» nos ficheiros estava certo.
- **Matriz de decisão do grupo** (Luís, 17/11): entrou no esqueleto do relatório (secção 5), com os pesos, as notas, a sensibilidade e o que fica fora da nota. O Gemma 4 foi confirmado a 16/11.
- **Formatos:** as perguntas, o catálogo e as pastas seguem o que o grupo combinou (perguntas sem resposta como `unanswerable`, como na atualização de 27/10).

## 9. Pendente

- As tuas notas na folha do piloto; depois, `rag/piloto.py compara`.
- No grupo:
  - mandar as versões dos modelos, que o Pedro Reis pediu a 15/11 (estão na tabela do README, com os digests);
  - esperar que o Luís diga como reportamos a matriz;
  - fazer os slides para a apresentação de 24/11.
- Na entrega (23/11):
  - o registo de uso de IA no anexo do relatório, ou como `IA.md` no zip, como na estrutura do grupo (o `IA.md` saiu do repositório no commit c06c184);
  - os originais de `kb/E1/raw/` (55 ficheiros, fora do git) no zip.
