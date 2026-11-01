# Base de conhecimento do E1: o que foi feito

**Área:** E1, resíduos e economia circular, incluindo a separação e o encaminhamento de resíduos, a reutilização e a reparação.  
**Responsável:** Guilherme Lobo Pinto.  
**Período:** 20 a 30 de outubro de 2026.  
**Estado a 30/10:** a base de conhecimento está fechada, com 36 documentos e 216 272 palavras. As 15 perguntas de teste estão propostas e falta revê-las.

## 1. Resumo

| | Documentos | Palavras |
|---|---|---|
| PDF descarregados e lidos (2 932 páginas) | 55 | 845 482 |
| **Na base de conhecimento** (`kb/E1/text`) | **36** | **216 272** |
| ... de Guimarães / nacionais | 21 / 15 | 104 017 / 112 255 |
| Partes opcionais, que ficaram fora da base | 19 (11 só com partes opcionais) | 74 588 |
| Excluídos | 8 | — |

O enunciado pede pelo menos 20 000 palavras de texto útil por área. As palavras contam-se com `len(texto.split())` no texto já limpo, como combinado no grupo.

## 2. Cronologia

- **20/10 (aula):** decisões do grupo sobre os formatos (catálogo, perguntas e registo da pesquisa), a contagem de palavras, o texto em UTF-8, NFC e fins de linha LF, a marcação dos trechos das perguntas por posições no texto original, o congelamento do texto e os prazos internos.
- **23/10:** pesquisa das fontes, nos sites das entidades e por palavras-chave. Daí saiu uma lista de 81 PDF com link direto, 32 deles de Guimarães. Descarga dos PDF de Guimarães (31 ficheiros).
- **24/10:** alargamento às fontes nacionais (25 links), leitura dos 55 PDF, escolha das partes úteis, extração e limpeza do texto e transcrição dos dois PDF em imagem.
- **25/10:** catálogo, registo da pesquisa (`sources_E1.md`) e registo de uso de IA. A primeira versão da base tinha 33 documentos e 205 448 palavras. Foi depois confirmada no computador do responsável: os 33 `.txt` saíram iguais aos esperados.
- **30/10:** revisão da seleção com embeddings, decisão dos 80 maiores desacordos, troca do 104 pela versão em vigor e pasta com os PDF usados. Nova corrida no computador do responsável: os 36 `.txt` saíram iguais aos esperados. No mesmo dia, o grupo fixou o formato das perguntas e do campo `"parts"`; o catálogo passou para o formato novo e ficou pronta a proposta das 15 perguntas (secção 12).

## 3. Como foi feita a pesquisa

A pesquisa foi feita com o apoio do Claude (Anthropic) e seguiu dois caminhos: a consulta direta dos sites das entidades e a pesquisa por palavras-chave num motor de pesquisa. Mais tarde, a 30/10, a seleção foi revista com embeddings (secção 6).

### 3.1 Sites das entidades

O ponto de partida foram as entidades que o enunciado indica: o Município de Guimarães, a Capital Verde Europeia 2026, a Agência Portuguesa do Ambiente e outras entidades públicas. Os sites consultados diretamente foram:

- a Câmara Municipal de Guimarães (secção «Economia circular e gestão de resíduos», planos e estratégias, ecocentros, regulamentos);
- a Vitrus Ambiente, o Laboratório da Paisagem (publicações), a revista Guimarães 26, o RRRCICLO e a Resinorte;
- a APA, a ERSAR e o Diário da República;
- a Comissão Europeia (página de Guimarães 2026 e CIRCABC) e a OCDE;
- os repositórios académicos RepositóriUM, Universidade Fernando Pessoa e Universidade de Coimbra.

### 3.2 Pesquisa por palavras-chave

A pesquisa também foi feita por palavras-chave: 80 pesquisas, 75 entre 23 e 24/10 e 5 a 30/10, todas no anexo A. Cada pesquisa juntava palavras de alguns destes grupos:

- **entidade ou lugar:** Guimarães, Vitrus Ambiente, Laboratório da Paisagem, Resinorte, APA, ERSAR;
- **tema do E1:** recolha seletiva, ecopontos, biorresíduos, PAYT, monos, têxteis, reparação, reutilização, desperdício alimentar, sistema de depósito;
- **tipo de documento e formato:** regulamento, plano, relatório, guia, `pdf`;
- **número oficial**, quando se procurava um diploma ou plano concreto: `Decreto-Lei 102-D/2020`, `Resolução do Conselho de Ministros 30/2023`;
- às vezes, o **domínio do site** (`cm-guimaraes.pt`, `ersar.pt`), **expressões exatas** entre aspas e **alternativas** com `OR`.

Três exemplos:

```text
Guimarães PAYT "pay as you throw" tarifário resíduos Vitrus sacos
Decreto-Lei 152-D/2017 pdf versão consolidada unilex embalagens REEE pilhas óleos
cm-guimaraes.pt uploads pdf compostagem doméstica OR economia circular OR biorresíduos Guimarães
```

As pesquisas foram feitas em quatro fases:

1. fontes de Guimarães, nacionais e europeias (37 pesquisas, 23/10);
2. links diretos para os PDF (24 pesquisas, 23/10);
3. fontes nacionais (5 pesquisas) e alternativas aos links que deixaram de funcionar (9 pesquisas), a 24/10;
4. a versão em vigor do UNILEX (5 pesquisas, 30/10).

### 3.3 Da pesquisa aos 55 PDF

- **Guimarães (001 a 031):** os links de Guimarães foram descarregados com um script de PowerShell (`descarregar_guimaraes.ps1`). Os 4 de repositórios universitários falharam no script e foram descarregados à mão. A dissertação da Universidade do Minho de 2019 (n.º 29 da lista de links) não foi descarregada, por isso há 31 ficheiros de Guimarães: o 029 é o link 30, o 030 é o link 32 e o 031 é o link 31.
- **Nacionais (101 a 126):** 25 links, 21 da lista dos 81 e 4 encontrados a 24/10. O script (`descarregar_nacionais.ps1`) descarregou 19; os outros 6 já não funcionavam:
  - três foram substituídos pelos PDF oficiais do Diário da República (102, 111 e 112);
  - o guia PAYT da ERSAR deu lugar ao guia técnico do Governo dos Açores (105);
  - dois ficaram de fora por não haver alternativa em PDF (113 e 122, secção 7.3).

  Juntou-se ainda o Documento Orientador da APA (126), com as metas por município.
- **104:** a 30/10, o responsável descarregou do Diário da República a versão consolidada em vigor do Decreto-Lei n.º 152-D/2017, que substituiu a de 2021 (secção 6.3).

## 4. Critérios de seleção

- **Tema do E1:** separação, recolha e encaminhamento de resíduos, reutilização, reparação e economia circular. O que é das outras áreas (água, energia, clima, mobilidade, espaços verdes e eventos) fica de fora, para não haver duplicados na base integrada do grupo.
- **Fontes públicas e oficiais primeiro:** Câmara, Vitrus, APA, Governo e Diário da República. Os trabalhos académicos entram só como complemento.
- **Atualidade:** entre versões do mesmo documento fica a mais recente (o tarifário de 2026 em vez do de 2025, o RARU 2025 em vez do de 2024) e, na legislação, a versão consolidada em vigor.
- **Nacional também conta:** um documento nacional entra quando se aplica hoje a Guimarães e não repete nem contradiz o que já está na base.
- **Português primeiro.** Entram três textos em inglês, todos sobre Guimarães (018, 021 e 029).
- **Só as partes relevantes** nos documentos longos (planos, relatórios e legislação). No catálogo, o campo `"parts"` tem as páginas usadas e o porquê do corte (por exemplo, `"páginas 6-46: O plano todo, sem a capa, o índice e as referências."`); quando o documento entra inteiro, é `null`.

## 5. Extração e limpeza do texto

O `scripts/pdf_para_txt.py` converte os PDF de `kb/E1/raw` em texto limpo. Para cada PDF:

1. extrai o texto página a página com o PyMuPDF, incluindo as páginas rodadas;
2. tira os cabeçalhos e rodapés repetidos, os números de página, as linhas de índice, os eixos dos gráficos e as notas de alteração da legislação consolidada;
3. junta as linhas em parágrafos e as palavras partidas no fim da linha, e corrige ligaduras e acentos soltos;
4. guarda as tabelas com uma linha por fila e as células separadas por tabulações;
5. grava em `kb/E1/text/<doc_id>.txt` só as partes definidas em `scripts/partes_E1.json`, pela ordem do documento e separadas por uma linha em branco;
6. escreve o catálogo (`kb/E1/catalog_E1.jsonl`), o relatório de palavras (`kb/E1/relatorio_palavras.csv`) e, desde 30/10, uma cópia de cada PDF usado em `kb/E1/pdf/<doc_id>.pdf`, com o mesmo nome do `.txt`.

O texto fica em UTF-8, NFC e fins de linha LF, para os offsets das perguntas (`texto[start:end]`) valerem em qualquer computador. O script não substitui um `.txt` que tenha mudado sem a opção `--forcar`. Os dois PDF em imagem (014 e 015) foram transcritos para `kb/E1/ocr/`, com os erros do original («revistam», «Indeferenciados»).

## 6. Revisão da seleção (30/10)

### 6.1 Método

A seleção de 24/10 foi revista com embeddings, com o `scripts/rever_embeddings.py`. O modelo `Qwen/Qwen3-Embedding-0.6B` correu no GPU do responsável e deu uma nota a cada parágrafo do texto limpo:

- a nota é a semelhança às frases que descrevem o E1 menos a semelhança às frases dos outros temas (`scripts/temas_E1.txt`), suavizada com os parágrafos vizinhos;
- o limiar (0,1076) é o que melhor separa o núcleo do texto que tinha ficado fora.

Os embeddings não decidem. Só apontam os sítios onde a nota e a seleção discordam, para rever caso a caso.

| | Valor |
|---|---|
| Parágrafos analisados (47 documentos; os 8 excluídos não entram) | 20 079 |
| Palavras do núcleo acima do limiar / de fora do núcleo acima do limiar | 72% / 39% |
| **Palavras relevantes segundo os embeddings** | **357 131** |
| ... dentro do núcleo / nas partes opcionais / fora da seleção | 147 283 / 49 410 / 160 438 |
| Casos de desacordo com 60 palavras ou mais | 783 (221 «tirar?» e 562 «juntar?») |
| Casos revistos um a um (os 80 maiores) | 80 |
| **Palavras na base depois da revisão** | **216 272** |

As palavras relevantes segundo os embeddings são muitas mais do que as da base: a nota também fica alta em texto do tema que não serve ao cidadão, como regras para operadores ou dados antigos. Por isso cada caso foi revisto.

### 6.2 Critério e decisões

O critério da revisão foi este:

- **juntar** o que se aplica hoje a Guimarães, responde a uma dúvida do cidadão ou explica uma regra, e não repete nem contradiz a base;
- **não juntar** dados antigos já superados, casos de outras regiões, texto só para operadores nem repetições;
- **tirar** só o que não é do E1.

O Claude analisou os 80 casos (os títulos, o início e o fim de cada um e, nos duvidosos, o texto todo) e sugeriu uma decisão e o motivo. O responsável aceitou todas as sugestões. O registo caso a caso está em `kb/E1/revisao/decisoes_30-10.csv`.

- **Juntados (6 casos, mais 6 775 palavras):**
  - a nota introdutória (pp. 9-11) e a secção 5 (pp. 43-50) do RARU 2025 (101), com o que acontece aos resíduos depois de recolhidos;
  - o art. 110.º do RGGR (103), que explica a TGR que aparece no tarifário de Guimarães;
  - o 029 inteiro, com os números do primeiro ano do PAYT em Guimarães;
  - o 114 inteiro, com o arranque do sistema de depósito em 2026;
  - o 119 inteiro, com as metas de reciclagem de embalagens.
- **Mantidos no núcleo (7 casos):** tabelas, listas de ações e texto jurídico de Guimarães e do PERSU 2030, com nota baixa por causa do formato. Nenhum caso foi tirado.
- **Deixados de fora (67 casos):** os motivos estão na secção 7.5.

### 6.3 Troca do 104

A revisão mostrou que o 104, a versão de 10/08/2021 do UNILEX, estava desatualizada:

- o Decreto-Lei n.º 24/2024 fez a décima alteração ao UNILEX, e depois vieram os Decretos-Leis n.os 34/2024 e 139-A/2025;
- o art. 23.º-C da versão de 2021 dizia que o depósito de embalagens de bebidas era obrigatório desde 2022 e incluía o vidro, ao contrário da circular de 2026 da APA (114), que dá o arranque a 10/04/2026 e só para plástico, aço e alumínio.

Entrou a versão consolidada de 30/12/2025, descarregada do Diário da República a 30/10/2026. Tem as mesmas secções de antes (disposições gerais, art. 13.º, embalagens, REEE e pilhas) e, de novo:

- o sistema de depósito e reembolso (arts. 30.º-A a 30.º-I, 30.º-T e 30.º-U);
- as secções de mobílias e colchões e de autocuidados de saúde no domicílio (arts. 87.º-A a 87.º-C).

O 104 passou de 15 309 para 19 358 palavras. Com as 6 junções, a base passou de 205 448 para 216 272 palavras. Os outros 30 `.txt` não mudaram.

## 7. O que ficou de fora e porquê

### 7.1 Documentos excluídos (8)

Foram descarregados e lidos, mas nenhuma parte entra na base.

| N.º | Documento | Porquê |
|---|---|---|
| 008 | Edital do tarifário de resíduos urbanos para 2026 | Só anuncia a aprovação do tarifário de 2026, que está no 007. É um PDF em imagem. |
| 009 | Tarifário de gestão de resíduos para o ano de 2025 | Foi substituído pelo tarifário de 2026 (007). |
| 010 | Edital do tarifário de resíduos urbanos para 2025 | Só anuncia a aprovação do tarifário de 2025. É um PDF em imagem. |
| 023 | Spatial accumulation of flood-driven riverside litter in two Northern Atlantic Rivers | Artigo científico sobre lixo nos rios, mais perto do E3 (água). |
| 027 | The Circular Economy in Cities and Regions of the European Union | Guimarães só aparece em tabelas e listas. |
| 030 | Estudo de caso: gestão dos circuitos de recolha de RSU no concelho de Guimarães (monografia) | Dados de 2004. |
| 115 | Relatório Anual de Resíduos Urbanos 2024 (RARU 2024) | Repete o RARU 2025 (101) com dados de outro ano. |
| 124 | Projeto de compostagem doméstica: guia | Repete o guia de compostagem do 125, e o texto extraído parte as palavras com letra capitular. |

### 7.2 Documentos que ficaram só com partes opcionais (11)

As partes opcionais entram com `python scripts/pdf_para_txt.py --opcional`, mas não fazem parte da base.

| N.º | Documento | Porquê |
|---|---|---|
| 012 | Avaliação da qualidade do serviço de resíduos urbanos 2023 (ERSAR) | Dados de 2023; o relatório de qualidade de 2025 (011) é mais recente. |
| 022 | Aqualastic: educar, reduzir e valorizar | Trata de plásticos nos rios; o estudo de microplásticos é do E3. |
| 028 | Implementação do sistema PAYT no Centro Histórico de Guimarães (dissertação) | Estudo de viabilidade com dados de 2013, anterior ao PAYT real de 2016; o caso real está no 105 e no 029. |
| 031 | Análise da recolha seletiva de resíduos urbanos em Portugal e comparação com outros países (dissertação) | Dados até cerca de 2014, superados pelo RARU 2025 e pelo PERSU 2030. Só a secção sobre Guimarães ficou como opcional. |
| 108 | Sistema de Depósito e Reembolso: sessão de esclarecimento da APA (27/11/2025) | Os diapositivos têm um aviso de confidencialidade da SDR Portugal, embora estejam publicados no site da APA. O sistema de depósito entra pelo 114 e pelo 104. |
| 116 | Balanço das atividades do PAEC entre 2018 e 2020 | Balanço de um plano que já terminou. |
| 117 | Plano de Ação para a Economia Circular 2017-2020 (RCM n.º 190-A/2017) | Plano que já terminou. |
| 118 | Regulamento n.º 594/2018 da ERSAR (relações comerciais) | As regras de deposição já estão no regulamento de Guimarães (004), adaptadas ao concelho; o resto é sobre água (E3). |
| 120 | Relatório final da 2.ª fase do programa de apoio a estudos municipais de recolha de biorresíduos | Não fala de Guimarães, e o plano de biorresíduos de Guimarães (002) já está na base. O anexo é imagem. |
| 121 | Relatório da Comissão COM(2023) 304 (Estados-Membros em risco de falhar as metas de 2025) | Avaliação de 2023 com dados de 2020, superada pelos resultados reais de 2025 no RARU 2025 (101). |
| 125 | Guia prático de compostagem (Município de Avis) | Guia genérico de outro concelho; a compostagem em Guimarães está no plano de biorresíduos (002) e no PAPERSU (001). |

### 7.3 Links que não chegaram a ser descarregados

Da lista dos 81 links, 28 não foram descarregados, e 2 dos links nacionais deixaram de funcionar:

| Links | Porquê ficaram de fora |
|---|---|
| Newsletters da Resinorte (n.os 33 a 38 da lista) | Marcadas como opcionais na lista: notícias mensais, que só valeriam a pena se falassem de Guimarães. |
| Errata do RARU 2024, RARU 2023 e nota de imprensa do RARU 2023 (41, 42 e 50) | Edições antigas; o RARU 2025 (101) é o atual. |
| PNGR 2030 em consulta pública (46) | A versão final é a RCM n.º 31/2023, que está na base (112). |
| Estrutura dos PAPERSU, orientações aos municípios (45) | Serve a quem escreve um PAPERSU; o PAPERSU de Guimarães (001) está na base. |
| Notas de imprensa da APA (49 e 51) | Anúncios, sem conteúdo além dos próprios documentos. |
| Legislação e estratégias europeias do EUR-Lex (64 a 78) | A base trata estes temas pela legislação nacional que se aplica ao cidadão (RGGR, UNILEX e Decreto-Lei n.º 84/2021) e pela notícia da diretiva da reparação (109). Os regulamentos europeus de aplicação direta ficam como limitação (secção 11). |
| 113, Reexame da aplicação da política ambiental 2025: Portugal (SWD(2025) 321), e 122, perfil de prevenção de resíduos de Portugal 2025 (Agência Europeia do Ambiente) | Os links deixaram de funcionar e não havia alternativa em PDF. |

Também ficaram de fora:

- **as páginas web** de Guimarães (ecocentros, monos, orgânicos, PAYT, RRRCICLO) e os sites das entidades gestoras (Sociedade Ponto Verde, Electrão, Valormed), porque a base foi construída só com PDF;
- **os documentos da Capital Verde 2026** no CIRCABC (candidatura de Guimarães, apresentação da candidatura, relatório do júri e síntese da avaliação técnica), que só descarregam no browser e não foram descarregados. A economia circular de Guimarães está nos planos municipais (001, 003 e 006) e no 021;
- **a dissertação de 2019** sobre o alargamento do PAYT em Guimarães, que não foi descarregada. O PAYT de Guimarães está no 105, no 029 e nos documentos da Câmara e da Vitrus;
- **o Plano Municipal de Ação Climática**, que é sobretudo do E3 (clima).

### 7.4 Partes deixadas de fora nos documentos da base

Nos documentos longos só entram as partes úteis para o E1. O que fica de fora em cada documento está na secção 8.

As regras gerais foram estas:

- saem a capa, os índices e a bibliografia, que não respondem a perguntas;
- saem os temas das outras áreas e os exemplos de outras cidades;
- sai o texto só para operadores (licenciamento, transporte, financiamento das entidades gestoras);
- sai o que podia contradizer documentos mais recentes, como as projeções de tarifa de 2021 do plano de biorresíduos.

### 7.5 Casos da revisão deixados de fora (67)

| Motivo | Casos |
|---|---|
| Republicação de 2020 do UNILEX dentro do 103, mais antiga do que o 104 | 1, 5, 38, 43, 49, 65, 66, 80 |
| Dissertação de 2013 (028), anterior ao PAYT real de 2016 | 2, 12, 17, 27, 45, 47, 51, 59, 64, 70, 73, 74 |
| Dissertação com dados até cerca de 2014 (031) | 10, 16, 26, 31, 32, 37, 58, 79 |
| Casos de outros concelhos e países (Lousada, São Brás de Alportel, Alemanha e outros) e o plano PAYT para os Açores | 3, 22, 23, 30, 42 |
| Relatórios, planos e balanços superados: avaliação europeia de 2023, balanços do PERSU 2020 e do PNGR anterior e o PAEC 2017-2020, já terminado | 6, 8, 13, 33, 55, 75, 77, 78 |
| Metodologias de cálculo, fichas de indicadores, dados de 2015 a 2019 e metas por fluxo que repetem o 119 e o UNILEX | 4, 19, 25, 35, 56, 60, 69 |
| Glossários, princípios e preâmbulos que repetem o RGGR ou só explicam a motivação dos diplomas | 21, 24, 34, 48, 72 |
| Texto só para operadores: aterros, capacidades das instalações, desenho de um PAYT, requisitos de fabrico, sacos de plástico (fiscal), óleos lubrificantes, estudos de biorresíduos | 7, 14, 28, 36, 40, 54, 61, 63 |
| Resíduos de todos os setores (indústria, construção) ou enquadramento genérico | 18, 46, 53 |
| Regras de deposição da ERSAR que o regulamento de Guimarães (004) já tem | 68 |
| Projeções de tarifa de 2021 que podiam contradizer o tarifário de 2026 | 57 |
| Referências bibliográficas | 39 |

## 8. Documentos na base de conhecimento (36)

| doc_id | Documento (entidade) | O que entra | O que fica de fora e porquê | Palavras |
|---|---|---|---|---|
| E1-001 | PAPERSU Guimarães 2030 (Câmara Municipal de Guimarães) | pp. 6-46 | Capa, índice e referências. | 14 545 |
| E1-002 | Plano de Gestão de Biorresíduos Guimarães 2030 (Câmara) | pp. 4-5, 10-23, 27-35, 41-68 e 72-78 | Índices, enquadramento geográfico, exemplos de outras cidades e bibliografia; a viabilidade económica (pp. 69-71) tem projeções de tarifa de 2021. | 15 410 |
| E1-003 | Compromisso Zero Resíduos do Município de Guimarães (Câmara) | Inteiro | — | 6 463 |
| E1-004 | Regulamento do Serviço de Gestão de Resíduos Urbanos de Guimarães (Câmara) | pp. 1-14, até ao fim do anexo 1 | Os atos vizinhos da mesma página do Diário da República e as minutas. | 14 815 |
| E1-005 | Regulamento Municipal de Limpeza Pública e Higiene Urbana de Guimarães (Câmara) | pp. 1-9, até ao capítulo IV | Disposições finais. | 4 248 |
| E1-006 | Plano de Ação Integrado para a Circularidade Têxtil de Guimarães (Câmara) | pp. 8-123 | Capa, índice e página-modelo final; o anexo das fichas de ação (pp. 127-157) ficou opcional porque repete a parte IV. | 30 154 |
| E1-007 | Tarifário de gestão de resíduos para 2026 (Câmara) | Inteiro | — | 380 |
| E1-011 | Relatório da qualidade do serviço de resíduos urbanos 2025 (Câmara) | Inteiro | — | 805 |
| E1-013 | Normas do Mercado das Trocas, edição equipamentos elétricos e eletrónicos (Câmara) | Inteiro | — | 759 |
| E1-014 | «Nunca fiz a separação. Como devo fazer?» (Vitrus Ambiente) | Inteiro (texto transcrito do PDF em imagem) | — | 546 |
| E1-015 | Tarifário PAYT (Vitrus Ambiente) | Inteiro (texto transcrito do PDF em imagem) | — | 116 |
| E1-016 | Ruas abrangidas e horários de recolha do PAYT (Vitrus Ambiente) | Inteiro | — | 200 |
| E1-017 | Urgezes Circular (Laboratório da Paisagem) | pp. 2-10 | Capa e contracapa. | 3 516 |
| E1-018 | Study on textile waste generation in the undifferentiated municipal solid waste stream in Guimarães (Laboratório da Paisagem) | pp. 1-14 | Referências. | 7 522 |
| E1-019 | Estudo das perceções e dos hábitos ambientais dos habitantes de Guimarães (Laboratório da Paisagem) | pp. 19-20, a secção «Resíduos» | O resto do estudo é dos temas das outras áreas. | 410 |
| E1-020 | Pegadas: 5 anos do Laboratório da Paisagem | p. 24, projetos de economia circular | O resto é educação ambiental (E4). | 241 |
| E1-021 | Guimarães: Circular Economy Towards a Sustainable City (Laboratório da Paisagem) | pp. 1-6 | Referências. | 2 535 |
| E1-024 | Revista Guimarães 26, volume 1 (Câmara) | pp. 40-42, «Economia Circular» | O resto da revista é de outros temas. | 271 |
| E1-025 | Revista Guimarães 26, volume 2 (Câmara) | p. 70, «Mercado sem Plástico» | O resto da revista é de outros temas. | 86 |
| E1-026 | Revista Guimarães 26, volume 3 (Câmara) | p. 103, «Re-Erguer» | O resto é de outros temas; as boas práticas HORECA (pp. 143-153) ficaram opcionais porque misturam energia. | 124 |
| E1-029 | Statistical Analysis of Urban Waste Management via PAYT in Guimarães (Universidade do Minho) | pp. 1-4 | Referências. | 871 |
| E1-101 | Relatório Anual de Resíduos Urbanos 2025 (APA) | pp. 9-58 (nota introdutória, sumário e análise nacional de 2025) e pp. 149-152 (ficha da RESINORTE, com Guimarães) | Capa e índice; anexos de metodologia e de resultados por sistema; fichas dos outros sistemas. | 12 770 |
| E1-102 | PERSU 2030, RCM n.º 30/2023 (Governo) | Secções 1 a 4 (enquadramento, situação de referência, metas e cenários) e 8 e 9 (eixos, objetivos, medidas e ações) | Secções 5 e 6 (fração residual e capacidade das instalações, para operadores); 7, 10 e 11 (financiamento, monitorização e governança) ficaram opcionais; anexos (balanço do PERSU 2020, metodologias e glossário que repete o RGGR). | 23 738 |
| E1-103 | Decreto-Lei n.º 102-D/2020, Regime Geral da Gestão de Resíduos, versão de 26/03/2024 (Governo) | RGGR: disposições gerais, definições e princípios, resíduos urbanos (arts. 45.º a 47.º), tarifas (arts. 106.º a 107.º-A), TGR (art. 110.º) e anexos III a V (instrumentos económicos, conteúdo dos planos e medidas de prevenção) | Preâmbulo e artigos que alteram outros diplomas; transporte, licenciamento e fiscalização; resíduos de construção e cálculo da TGR (opcionais); regime dos aterros; republicação de 2020 do UNILEX. | 15 556 |
| E1-104 | Decreto-Lei n.º 152-D/2017, Regime Unificado dos Fluxos Específicos de Resíduos, versão de 30/12/2025 (Governo) | Disposições gerais, art. 13.º, embalagens até ao art. 25.º-C, sistema de depósito e reembolso (arts. 30.º-A a 30.º-I, 30.º-T e 30.º-U), REEE, pilhas, mobílias e colchões, autocuidados de saúde no domicílio | Preâmbulo; regras dos sistemas de gestão para as entidades gestoras; requisitos de fabrico e metas das embalagens (as metas entram pelo 119); financiamento e licenciamento do sistema de depósito; contribuição sobre sacos de plástico; óleos lubrificantes; pneus e veículos em fim de vida (opcionais); fiscalização e anexos. | 19 358 |
| E1-105 | Guia técnico de sistemas PAYT, SAYT ou RAYT nos Açores, volume 1 (Governo dos Açores) | pp. 4-20 (o que são e como funcionam), pp. 46-50 (SAYT e RAYT) e pp. 60-68 (caso de Guimarães) | Parte de implementação para municípios (pp. 21-45, opcional), casos de outros concelhos e países e o plano para os Açores. | 9 288 |
| E1-106 | Perguntas frequentes: produtos têxteis, têxteis e calçado (APA) | pp. 3-7 | Capa e índice. | 1 615 |
| E1-107 | Nota técnica da recolha seletiva de biorresíduos (APA) | Inteiro | — | 801 |
| E1-109 | Publicada a Diretiva Europeia sobre a Reparação de Bens (Município de Vila Nova de Gaia, CIAC) | Inteiro | — | 532 |
| E1-110 | Decreto-Lei n.º 84/2021, direitos do consumidor na compra e venda de bens (Governo) | Garantias, reparação e peças (secção II do capítulo II e secção I do capítulo IV) | O resto do diploma (imóveis, conteúdos digitais, mercados em linha e disposições finais); os requisitos de conformidade (secção I do capítulo II) ficaram opcionais. | 3 045 |
| E1-111 | Estratégia Nacional de Combate ao Desperdício Alimentar, RCM n.º 46/2018 (Governo) | A resolução inteira | Os atos vizinhos da mesma publicação. | 9 958 |
| E1-112 | PNGR 2030, RCM n.º 31/2023 (Governo) | pp. 26-40 (estratégia, objetivos e metas) | Diagnóstico e medidas (pp. 2-17 e 41-72, opcionais); balanço do PNGR anterior; anexos (dados de fluxos de 2015 a 2019, fichas de indicadores, glossário). | 7 744 |
| E1-114 | Circular n.º 01/2026/DFEMR, período de transição do sistema de depósito (APA) | Inteiro | — | 901 |
| E1-119 | Embalagens e resíduos de embalagens: dados de 2022 (APA) | Inteiro | — | 1 163 |
| E1-123 | Guia de boas práticas de redução e reutilização (LIPOR) | p. 2 e pp. 4-17 | Capa e índice. | 1 257 |
| E1-126 | Objetivos intercalares por município e SGRU para as metas do PERSU 2030 (APA) | pp. 3-12 (enquadramento) e pp. 41-44 (RESINORTE, com Guimarães) | As secções dos outros sistemas. | 4 529 |

As páginas exatas e os marcadores de cada parte estão no `scripts/partes_E1.json`, no campo `"parts"` do catálogo e no `sources_E1.md`.

## 9. Ficheiros

| Ficheiro | O que é |
|---|---|
| `scripts/pdf_para_txt.py` | Converte os PDF em `.txt` limpos, escreve o catálogo e o relatório e copia os PDF usados. |
| `scripts/partes_E1.json` | Metadados de cada PDF e partes que entram (núcleo) ou ficam opcionais. |
| `scripts/rever_embeddings.py` e `scripts/temas_E1.txt` | Revisão da seleção com embeddings e as frases que descrevem o tema. |
| `scripts/perguntas_E1.py` | Procura na base, calcula as posições e o `sha1` dos trechos e valida o ficheiro das perguntas. |
| `kb/E1/raw/` | Os 55 PDF originais (fora do git). |
| `kb/E1/pdf/` | Os 36 PDF que entram na base, com o nome do `.txt` (fora do git). |
| `kb/E1/text/` | Os 36 `.txt` da base de conhecimento. |
| `kb/E1/ocr/` | O texto transcrito dos PDF em imagem (014 e 015). |
| `kb/E1/catalog_E1.jsonl` | Catálogo: `doc_id`, título, entidade, URL, data de acesso, área, ficheiro e partes. |
| `kb/E1/relatorio_palavras.csv` | Palavras por documento: no PDF, no núcleo, nas partes opcionais e no `.txt`. |
| `kb/E1/sources_E1.md` | Registo da pesquisa (fontes, critérios, pesquisas e limitações). |
| `kb/E1/revisao/` | Resultados da revisão de 30/10 (`resumo.md`, `documentos.csv`, `paragrafos.csv`, `desacordos.csv`) e as decisões (`decisoes_30-10.csv`). |
| `tests/questions_E1.jsonl` | As 15 perguntas de teste (proposta de 30/10, corrigida a 31/10, por rever). |

## 10. Uso de ferramentas de IA

O trabalho foi feito com o apoio do Claude (Anthropic). O registo linha a linha fica fora do repositório e entra no anexo «Declaração de Utilização de Ferramentas de IA» do relatório individual. Em resumo, o Claude:

- fez as pesquisas por palavras-chave, leu as páginas das entidades e montou a lista de links;
- escreveu os scripts de descarga, o `pdf_para_txt.py` e o `rever_embeddings.py`;
- analisou os 55 PDF e propôs as partes;
- sugeriu a decisão de cada um dos 80 casos da revisão;
- escreveu o `perguntas_E1.py`, propôs as 15 perguntas de teste e procurou na base do E1 as perguntas sem resposta das outras áreas;
- transcreveu os dois PDF em imagem e redigiu o `sources_E1.md` e este registo.

O responsável:

- descarregou os PDF e correu os scripts no seu computador, confirmando que os resultados batiam certo;
- escolheu a abordagem da revisão (embeddings em vez de afinar um modelo de linguagem) e aceitou as decisões;
- descarregou do Diário da República a versão em vigor do 104.

## 11. Limitações

- **Legislação:** o 103 e o 110 são cópias fiéis alojadas noutros sites públicos (Governo Regional da Madeira e AICCOPN). O 103 é a versão consolidada de 26/03/2024; alterações posteriores, se as houver, não estão incluídas.
- **Legislação europeia:** os regulamentos de aplicação direta (embalagens, Regulamento (UE) 2025/40; baterias, Regulamento (UE) 2023/1542) não estão na base.
- **Revisão:** só os 80 maiores desacordos foram revistos um a um. Ficaram por rever os outros 703 com 60 palavras ou mais e 327 mais pequenos (9 509 palavras).
- **014 e 015:** são PDF em imagem; o texto foi transcrito a partir das imagens.
- **016:** a tabela das ruas e horários do PAYT extrai com o texto partido.
- **Tabelas e gráficos:** as tabelas ficam uma linha por fila, com as células separadas por tabulações; o texto dos gráficos perde-se em parte.

## 12. Perguntas de teste (proposta de 30/10, corrigida a 31/10)

O grupo fixou a 30/10 um formato comum para as 60 perguntas: um ficheiro por área, com uma pergunta por linha. No E1 é `tests/questions_E1.jsonl`, e cada pergunta tem estes campos:

- `id` (`E1-01` a `E1-15`), `type` (`factual`, `multi_doc` ou `unanswerable`) e `subtopic`;
- `question`, `reference_answer` e `notes` (opcional);
- `evidence`, com os trechos que fundamentam a resposta. Cada trecho tem `doc_id`, `start` e `end` (posições no `.txt`, com o fim exclusivo), `text` (o trecho literal) e `sha1` (dos bytes do `.txt`, para se saber se o documento mudou). O campo opcional `group` marca trechos alternativos: basta um deles.

A proposta tem 8 perguntas factuais, 4 que juntam documentos e 3 sem resposta, sobre a separação, o encaminhamento, o tarifário, a reutilização, a reparação, a limpeza urbana, o sistema de depósito e as metas. Os trechos foram tirados dos `.txt` finais e o `perguntas_E1.py` confirmou as regras do grupo, sem erros: `texto[start:end]` igual ao trecho, o `sha1` de cada documento, a divisão 8/4/3, as perguntas de vários documentos com pelo menos 2 `doc_id` e todos os `doc_id` no catálogo. O único aviso é um trecho com 607 caracteres (o art. 30.º-F do UNILEX), abaixo do tamanho de um excerto da configuração B.

As 3 perguntas sem resposta são «quase-respostas»: o tema está na base, mas o dado pedido não. Cada uma foi procurada na base do E1 por palavras-chave, com as ocorrências lidas, e o resultado está nas `notes`. Também se procuraram na base do E1 as perguntas sem resposta do E2 (trotinetes, bicicleta em 2030, último comboio) e as três do E3 (horário do Espaço Energia, fator de emissão da eletricidade e dureza da água da torneira): nenhuma tem resposta no E1.

Ao reler a proposta a 31/10, o Claude corrigiu três pontos. Os dois trechos da E1-02 passaram a incluir o nome do contentor («Vidro» e «Resíduos Indeferenciados»), para se perceberem sozinhos. A pergunta da E1-10 deixou de pressupor que o sistema de depósito já tinha arrancado, porque a base só tem a data prevista. A E1-12 ganhou uma nota a explicar que os 494 kg são de 2025, ano que o trecho não repete. A validação continuou com 0 erros e o mesmo aviso.

## 13. Próximos passos

- Dar uma vista de olhos aos `.txt` em `kb/E1/text`, ao lado dos PDF em `kb/E1/pdf`, começando pelos que mudaram a 30/10 (101, 103, 104, 029, 114 e 119).
- Fazer commit e avisar o grupo de que o texto do E1 mudou a 30/10 (36 documentos e 216 272 palavras). A partir daqui o texto fica congelado.
- Rever as 15 perguntas propostas e acertá-las até 1/11, antes de correr o pipeline sobre elas.
- Partilhar no grupo as 3 perguntas sem resposta, para as outras áreas confirmarem que também não têm resposta nas suas bases, e confirmar dois pontos do formato: os `doc_id` do E1 (`E1-001`, como combinado a 20/10) e o cálculo do `sha1` sobre os bytes do `.txt`.
- Revisão cruzada das perguntas com o E2 a 2 e 3/11.

## Anexo A. As 80 pesquisas por palavras-chave

Feitas com o Claude num motor de pesquisa, pela ordem em que foram feitas, e agrupadas por fase.

**23/10/2026: fontes de Guimarães, nacionais e europeias**

```text
Guimarães resíduos urbanos recolha seletiva Vitrus Ambiente ecopontos
Regulamento de gestão de resíduos urbanos Município de Guimarães Diário da República
Guimarães Capital Verde Europeia 2026 candidatura resíduos economia circular documento
European Green Capital 2026 Guimarães application waste circular economy pdf
vitrus.pt recolha resíduos Guimarães monos biorresíduos porta-a-porta
"Guimarães" regulamento municipal resíduos urbanos limpeza pública cm-guimaraes.pt
Vitrus Ambiente EM Guimarães relatório e contas plano de atividades resíduos
"Guimarães" "regulamento" "serviço de gestão de resíduos urbanos" OR "resíduos urbanos e limpeza" município Guimarães
Município de Guimarães regulamento resíduos urbanos higiene limpeza Vitrus publicado Diário da República 2.ª série
Guimarães PAYT "pay as you throw" tarifário resíduos Vitrus sacos
RRRCICLO Guimarães Laboratório da Paisagem reutilização reparação
"Urgezes Circular" reparação Guimarães
Guimarães quiosques economia circular trocas reparação Capital Verde 2026 programa
Guimarães recolha seletiva têxteis porta-a-porta biorresíduos alargamento PAYT 2025 2026 cm-guimaraes.pt notícia
Resinorte Guimarães ecocentros ecopontos relatório de sustentabilidade 2024 pdf
APA PERSU 2030 documento pdf Plano Estratégico para os Resíduos Urbanos
APA Relatório Anual de Resíduos Urbanos RARU 2024 pdf
ERSAR RASARP 2025 volume resíduos urbanos qualidade do serviço pdf
Resolução do Conselho de Ministros 30/2023 PNGR 2030 PERSU 2030 PERNU 2030 Diário da República
Decreto-Lei 102-D/2020 regime geral de gestão de resíduos versão consolidada diariodarepublica.pt
Diretiva (UE) 2024/1799 direito à reparação EUR-Lex PT transposição Portugal decreto-lei 2026
ERSAR RASARP 2025 relatório anual serviços de águas e resíduos volume 1 caracterização ersar.pt
Sociedade Ponto Verde guia separação ecoponto amarelo azul verde o que colocar pdf
APA recolha seletiva têxteis obrigatória 2025 biorresíduos fluxos específicos resíduos apambiente.pt
Portugal Plano de Ação para a Economia Circular novo PAEC Resolução Conselho de Ministros 2024 2025
APA RARU 2025 relatório anual resíduos urbanos 2025 publicado outubro 2026
Guimarães Capital Verde Europeia 2026 site oficial programa iniciativas resíduos reciclagem desafios cidadãos
"guimaraes2026" OR "capital verde europeia 2026" Guimarães site programação oficial
G4CE Guimarães estratégia economia circular RRRCICLO documento
Laboratório da Paisagem Guimarães PEGADAS programa educação ambiental resíduos compostagem recursos
Diretiva (UE) 2025/1892 revisão diretiva-quadro resíduos têxteis desperdício alimentar EUR-Lex
Direção-Geral do Consumidor direito à reparação de bens informação consumidor.gov.pt diretiva 2024/1799
ERSAR guia do utilizador serviços de resíduos urbanos consumidor direitos tarifário PAYT ersar.pt
Electrão onde reciclar pilhas equipamentos elétricos lâmpadas Valormed medicamentos farmácias como funciona
ersar.pt RASARP 2025 relatório anual resíduos urbanos publicação (só no domínio ersar.pt)
Novo Verde entidade gestora resíduos de embalagens novoverde.pt
Valorcar veículos em fim de vida entidade gestora valorcar.pt Valorpneu pneus usados
```

**23/10/2026: links diretos para os PDF**

```text
PNGR 2030 Plano Nacional de Gestão de Resíduos pdf apambiente.pt
Decreto-Lei n.º 102-D/2020 pdf files.dre.pt 10 de dezembro 2020 regime geral gestão de resíduos
Decreto-Lei 152-D/2017 UNILEX pdf fluxos específicos de resíduos
Estratégia Nacional de Combate ao Desperdício Alimentar pdf Resolução Conselho de Ministros 46/2018
ERSAR guia técnico resíduos urbanos recolha seletiva biorresíduos pdf ersar.pt/docs
RECOLHABIO relatório final CIM do Ave biorresíduos Guimarães fundoambiental
Resolução do Conselho de Ministros n.º 30/2023 PERSU 2030 pdf
Resolução do Conselho de Ministros 58/2026 Plano de Ação para a Economia Circular 2025-2030 pdf
repositorium uminho dissertação Guimarães resíduos urbanos PAYT biorresíduos Vitrus pdf
cm-guimaraes.pt cmguimaraes uploads document file resíduos relatório qualidade serviço 2024 pdf
Environmental Implementation Review 2025 Portugal country report pdf resíduos economia circular
EEA early warning assessment Portugal municipal waste recycling targets 2025 pdf
guia compostagem doméstica pdf município entidade pública Portugal biorresíduos compostor
Electrão pdf guia reciclagem equipamentos elétricos pilhas lâmpadas cidadão
Valormed folheto pdf medicamentos fora de uso como entregar farmácia
Resinorte relatório e contas 2024 pdf OR relatório de sustentabilidade 2024 Resinorte pdf
vitrusambiente.pt pdf
cm-guimaraes.pt uploads pdf compostagem doméstica OR economia circular OR biorresíduos Guimarães
ersar.pt docs relatorios RASARP 2025 volume 1 pdf caracterização
eco.nomia.pt Plano de Ação para a Economia Circular PAEC pdf Liderar a transição
Decreto-Lei 84/2021 direitos do consumidor compra e venda bens garantia peças sobresselentes 10 anos pdf DGC
LIPOR guia prevenção resíduos reutilização reparação pdf cidadão
LIPOR guia reparação reutilização compostagem caseira pdf fotos bibliotecas guia
Plano Municipal de Ação Climática Guimarães pdf resíduos setor
```

**24/10/2026: fontes nacionais**

```text
Portugal transposição diretiva direito à reparação decreto-lei aprovado Conselho de Ministros 2026
sistema de depósito e reembolso embalagens de bebidas Portugal 2026 arranque SDR portaria APA
ERSAR Regulamento de Relações Comerciais serviços de águas e resíduos pdf regulamento 594/2018
Decreto-Lei 152-D/2017 pdf versão consolidada unilex embalagens REEE pilhas óleos
SDR Portugal depósito 10 cêntimos onde devolver garrafas latas máquinas consumidor guia oficial
```

**24/10/2026: alternativas aos links que deixaram de funcionar**

```text
PERSU 2030 Resolução do Conselho de Ministros 30/2023 pdf files.diariodarepublica.pt OR apambiente.pt
Estratégia Nacional e Plano de Ação de Combate ao Desperdício Alimentar pdf CNCDA
"PAYT" "Implementação de Sistemas de Pagamento em Função da Produção" ERSAR pdf guia
"Reexame da aplicação da política ambiental" 2025 Portugal relatório pdf Comissão Europeia
"files.diariodarepublica.pt/1s/2023/03/06000"
PERSU 2030 Plano Estratégico para os Resíduos Urbanos documento pdf download 2023 versão final
"files.dre.pt/1s/2023/03/06000/00140"
Resolução do Conselho de Ministros n.º 46/2018 27 de abril pdf files.dre.pt 1s 2018 04 Estratégia Nacional Combate Desperdício Alimentar
Environmental Implementation Review 2025 country report Portugal PDF SWD(2025) 321 environment.ec.europa.eu document download
```

**30/10/2026: versão em vigor do UNILEX (104)**

```text
Decreto-Lei 152-D/2017 alterações 2023 2024 2025 versão consolidada UNILEX
"152-D/2017" "24/2024" fluxos específicos de resíduos alteração
diariodarepublica.pt legislação consolidada Decreto-Lei n.º 152-D/2017 regime unificado dos fluxos específicos de resíduos
"legislacao-consolidada/decreto-lei/2017" 152-D
diariodarepublica.pt legislacao-consolidada decreto-lei 2017 "152-D/2017" "fluxos específicos"
```
