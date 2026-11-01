# Registo da pesquisa: E1, resíduos e economia circular

**Área:** resíduos e economia circular, incluindo a separação e o encaminhamento de resíduos, a reutilização e a reparação.  
**Responsável:** Guilherme Lobo Pinto.  
**Período:** 23 a 30 de outubro de 2026.

## 1. Como foi feita a pesquisa

A pesquisa foi feita com o apoio do Claude (Anthropic), que fez as pesquisas na web e leu as páginas das entidades (o registo de uso de IA entra no anexo «Declaração de Utilização de Ferramentas de IA» do relatório individual). O ponto de partida foram as entidades que o enunciado indica: o Município de Guimarães, a Capital Verde Europeia 2026, a Agência Portuguesa do Ambiente e outras entidades públicas.

- **23/10:** pesquisa de fontes de Guimarães e de fontes nacionais e europeias (75 pesquisas até 24/10, na secção 7). Daí saiu uma lista de 81 PDF com link direto, 32 deles de Guimarães.
- **23/10:** descarga dos 32 PDF de Guimarães com um script de PowerShell. Os 4 de repositórios universitários falharam e foram descarregados à mão. A dissertação da Universidade do Minho de 2019 (n.º 29 da lista de links) não foi descarregada, por isso o ficheiro 029 é o link 30, o 030 é o link 32 e o 031 é o link 31.
- **24/10:** alargamento às fontes nacionais, com 25 links (ficheiros 101 a 125). O script descarregou 19; os outros 6 links já não funcionavam. Três foram substituídos pelos PDF oficiais do Diário da República (102, 111 e 112), o guia PAYT da ERSAR deu lugar ao guia técnico do Governo dos Açores (105) e dois ficaram de fora por não haver alternativa em PDF (113 e 122). Juntou-se o Documento Orientador da APA (126), com as metas por município.
- **24/10:** leitura dos 55 PDF, escolha das partes úteis para o E1 (definidas em `scripts/partes_E1.json`) e extração e limpeza do texto com `scripts/pdf_para_txt.py`. Os dois PDF em imagem (014 e 015) foram transcritos para `kb/E1/ocr/`.
- **30/10:** revisão da seleção com embeddings e troca do 104 pela versão consolidada em vigor, descarregada do Diário da República (secção 4; mais 5 pesquisas na secção 7).

Sites consultados diretamente: Câmara Municipal de Guimarães (secção «Economia circular e gestão de resíduos», planos e estratégias, ecocentros, regulamentos), Vitrus Ambiente, Laboratório da Paisagem (publicações), Guimarães 26 (revista), RRRCICLO, Resinorte, APA, ERSAR, Diário da República, Comissão Europeia (página de Guimarães 2026 e CIRCABC), OCDE e repositórios académicos (RepositóriUM, Universidade Fernando Pessoa, Universidade de Coimbra).

## 2. Critérios de seleção

- **Tema do E1:** separação, recolha e encaminhamento de resíduos, reutilização, reparação e economia circular. O que é das outras áreas (água, energia, clima, mobilidade, espaços verdes e eventos) fica de fora, para não haver duplicados na base integrada.
- **Fontes públicas e oficiais primeiro:** Câmara, Vitrus, APA, Governo e Diário da República. Os trabalhos académicos entram só como complemento.
- **Atualidade:** entre versões do mesmo documento fica a mais recente (o tarifário de 2026 em vez do de 2025, o RARU 2025 em vez do de 2024) e, na legislação, a versão consolidada em vigor.
- **Português primeiro.** Entram três textos em inglês sobre Guimarães (018, 021 e 029).
- **Nacional também conta:** o que é de âmbito nacional entra quando se aplica hoje a Guimarães e não repete nem contradiz o que já está na base.
- **Só as partes relevantes** nos documentos longos (planos, relatórios e legislação). No catálogo, o campo `"parts"` tem as páginas usadas e o porquê do corte; quando o documento entra inteiro, é `null`.

## 3. Resultado

| | Documentos | Palavras |
|---|---|---|
| PDF descarregados (2 932 páginas) | 55 | 845 482 |
| **Na base de conhecimento** (`kb/E1/text` e `catalog_E1.jsonl`) | **36** | **216 272** |
| De Guimarães / nacionais | 21 / 15 | 104 017 / 112 255 |
| Partes opcionais (não usadas) | 19 (11 só com partes opcionais) | 74 588 |
| Excluídos | 8 | — |

As palavras contam-se com `len(texto.split())` no texto já limpo. O `doc_id` é `E1-` seguido do número do ficheiro.

**Excluídos:**

| N.º | Documento | Motivo |
|---|---|---|
| 008 | Edital do tarifário de resíduos urbanos para 2026 | Só anuncia a aprovação do tarifário de 2026 (PDF em imagem). |
| 009 | Tarifário de gestão de resíduos para o ano de 2025 | Foi substituído pelo tarifário de 2026. |
| 010 | Edital do tarifário de resíduos urbanos para 2025 | Só anuncia a aprovação do tarifário de 2025 (PDF em imagem). |
| 023 | Spatial accumulation of flood-driven riverside litter in two Northern Atlantic Rivers | Artigo científico sobre rios, mais perto do E3. |
| 027 | The Circular Economy in Cities and Regions of the European Union | Guimarães só aparece em tabelas e listas. |
| 030 | Estudo de caso: gestão dos circuitos de recolha de RSU no concelho de Guimarães (monografia) | Dados de 2004. |
| 115 | Relatório Anual de Resíduos Urbanos 2024 (RARU 2024) | Repete o RARU 2025 com dados de outro ano. |
| 124 | Projeto de compostagem doméstica: guia | Repete o guia de compostagem do 125, e o texto extraído parte as palavras com letra capitular. |

**Encontrados mas não recolhidos:** as páginas web de Guimarães (ecocentros, monos, orgânicos, PAYT, RRRCICLO), a candidatura de Guimarães a Capital Verde 2026 (só descarrega no browser, no CIRCABC), a legislação europeia no EUR-Lex e os sites das entidades gestoras (Sociedade Ponto Verde, Electrão, Valormed).

## 4. Revisão da seleção (30/10)

A seleção de 24/10 foi revista com embeddings, com o `scripts/rever_embeddings.py` (escrito com o Claude). O modelo `Qwen/Qwen3-Embedding-0.6B`, a correr no GPU do responsável, deu a cada parágrafo do texto limpo uma nota: a semelhança às frases que descrevem o E1 menos a semelhança às frases dos outros temas (`scripts/temas_E1.txt`), suavizada com os parágrafos vizinhos. O limiar (0,1076) é o que melhor separa o núcleo do texto que tinha ficado fora. Os embeddings não decidem: só apontam os sítios onde a nota e a seleção discordam, para rever caso a caso.

| | Valor |
|---|---|
| Parágrafos analisados (47 documentos; os 8 excluídos não entram) | 20 079 |
| Palavras do núcleo acima do limiar / de fora do núcleo acima do limiar | 72% / 39% |
| **Palavras relevantes segundo os embeddings** | **357 131** |
| ... dentro do núcleo / nas partes opcionais / fora da seleção | 147 283 / 49 410 / 160 438 |
| Casos de desacordo com 60 palavras ou mais | 783 (221 «tirar?» e 562 «juntar?») |
| Casos revistos um a um (os 80 maiores) | 80 |
| **Palavras na base depois da revisão** | **216 272** |

Critério da revisão: juntar o que se aplica hoje a Guimarães, responde a uma dúvida do cidadão ou explica uma regra, e não repete nem contradiz a base; não juntar dados antigos já superados, casos de outras regiões, texto só para operadores nem repetições; tirar só o que não é do E1. O Claude analisou os 80 casos (os títulos, o início e o fim de cada um e, nos duvidosos, o texto todo) e sugeriu uma decisão e o motivo; o responsável aceitou todas as sugestões. O registo caso a caso está em `kb/E1/revisao/decisoes_30-10.csv`.

- **Juntados (6 casos):** a nota introdutória (pp. 9-11) e a secção 5 (pp. 43-50) do RARU 2025 (101); o art. 110.º do RGGR, sobre a TGR (103); e, inteiros, o 029 (números do primeiro ano do PAYT em Guimarães), o 114 (arranque do sistema de depósito em 2026) e o 119 (metas de reciclagem de embalagens).
- **Mantidos no núcleo (7 casos):** tabelas, listas de ações e texto jurídico de Guimarães e do PERSU 2030 com nota baixa por causa do formato. Nenhum caso foi tirado.
- **Deixados de fora (67 casos):** a republicação de 2020 do UNILEX dentro do 103, as dissertações 028 e 031 (dados de 2013 e 2014), casos de outros concelhos e países, balanços de planos já terminados, glossários e princípios que repetem o RGGR e texto só para operadores.
- **104 trocado:** a revisão mostrou que a versão de 10/08/2021 do UNILEX estava desatualizada. O Decreto-Lei n.º 24/2024 fez-lhe a décima alteração, e o art. 23.º-C dessa versão dizia que o depósito de embalagens de bebidas era obrigatório desde 2022 e incluía o vidro, ao contrário da circular de 2026 da APA (114). Entrou a versão consolidada de 30/12/2025 (com os Decretos-Leis n.os 24/2024, 34/2024 e 139-A/2025), descarregada do Diário da República a 30/10/2026, com as mesmas secções de antes (disposições gerais, art. 13.º, embalagens, REEE e pilhas) e, de novo, o sistema de depósito e reembolso (arts. 30.º-A a 30.º-I, 30.º-T e 30.º-U) e as secções de mobílias e colchões e de autocuidados de saúde no domicílio (arts. 87.º-A a 87.º-C).

## 5. Limitações

- **Legislação:** o 103 e o 110 são cópias fiéis alojadas noutros sites públicos (Governo Regional da Madeira e AICCOPN), e o 103 é a versão consolidada de 26/03/2024. O `url` do catálogo é o da cópia usada.
- **Revisão:** só os 80 maiores desacordos foram revistos um a um; ficaram por rever os outros 703 com 60 palavras ou mais e 327 mais pequenos (9 509 palavras).
- **014 e 015:** PDF em imagem, com o texto transcrito a partir das imagens.
- **016:** a tabela das ruas e horários do PAYT extrai com o texto partido.
- **Tabelas e gráficos:** as tabelas ficam uma linha por fila, com as células separadas por tabulações; o texto dos gráficos perde-se em parte.

## 6. Documentos na base de conhecimento

| doc_id | Documento | Entidade | Partes usadas | Palavras |
|---|---|---|---|---|
| E1-001 | PAPERSU Guimarães 2030 | Câmara Municipal de Guimarães | pp. 6-46 (até antes de «9. Referencias») | 14 545 |
| E1-002 | Plano de Gestão de Biorresíduos Guimarães 2030 | Câmara Municipal de Guimarães | pp. 4-5; pp. 10-23; pp. 27-35; pp. 41-68; pp. 72-78 | 15 410 |
| E1-003 | Compromisso Zero Resíduos do Município de Guimarães | Câmara Municipal de Guimarães | documento inteiro | 6 463 |
| E1-004 | Regulamento do Serviço de Gestão de Resíduos Urbanos do Município de Guimarães | Câmara Municipal de Guimarães | pp. 1-14 (de «Edital n.º 248/2016» até antes de «ANEXO 2») | 14 815 |
| E1-005 | Regulamento Municipal de Limpeza Pública e Higiene Urbana de Guimarães | Câmara Municipal de Guimarães | pp. 1-9 (de «Edital n.º 589/2021» até antes de «CAPÍTULO IV») | 4 248 |
| E1-006 | Plano de Ação Integrado para a Circularidade Têxtil de Guimarães | Câmara Municipal de Guimarães | pp. 8-123 | 30 154 |
| E1-007 | Tarifário de gestão de resíduos para o ano de 2026 | Câmara Municipal de Guimarães | documento inteiro | 380 |
| E1-011 | Relatório da qualidade do serviço de resíduos urbanos 2025 | Câmara Municipal de Guimarães | documento inteiro | 805 |
| E1-013 | Normas de participação no Mercado das Trocas – Edição Equipamentos Elétricos e Eletrónicos | Câmara Municipal de Guimarães | documento inteiro | 759 |
| E1-014 | Nunca fiz a separação. Como devo fazer? | Vitrus Ambiente, EM | documento inteiro (texto transcrito) | 546 |
| E1-015 | Tarifário PAYT | Vitrus Ambiente, EM | documento inteiro (texto transcrito) | 116 |
| E1-016 | Ruas abrangidas e horários de recolha do sistema PAYT | Vitrus Ambiente, EM | documento inteiro | 200 |
| E1-017 | Urgezes Circular | Laboratório da Paisagem | pp. 2-10 | 3 516 |
| E1-018 | Study on textile waste generation in the undifferentiated municipal solid waste stream in Guimarães, Portugal | Laboratório da Paisagem | pp. 1-14 (até antes de «References») | 7 522 |
| E1-019 | Estudo das perceções e dos hábitos ambientais dos habitantes de Guimarães | Laboratório da Paisagem | pp. 19-20 | 410 |
| E1-020 | Pegadas: 5 anos do Laboratório da Paisagem | Laboratório da Paisagem | p. 24 | 241 |
| E1-021 | Guimarães: Circular Economy Towards a Sustainable City | Laboratório da Paisagem | pp. 1-6 (até antes de «References») | 2 535 |
| E1-024 | Revista Guimarães 26, volume 1 (jan.–abr. 2026) | Câmara Municipal de Guimarães | pp. 40-42 | 271 |
| E1-025 | Revista Guimarães 26, volume 2 (mai.–ago. 2026) | Câmara Municipal de Guimarães | p. 70 | 86 |
| E1-026 | Revista Guimarães 26, volume 3 (set.–dez. 2026) | Câmara Municipal de Guimarães | p. 103 | 124 |
| E1-029 | Statistical Analysis of Urban Waste Management via Pay-As-You-Throw (PAYT) System in the Portuguese City of Guimarães | Universidade do Minho | pp. 1-4 (até antes de «References») | 871 |
| E1-101 | Relatório Anual de Resíduos Urbanos 2025 (RARU 2025) | Agência Portuguesa do Ambiente | pp. 9-58 (a partir de «1. Nota Introdutória»); pp. 149-152 | 12 770 |
| E1-102 | Plano Estratégico para os Resíduos Urbanos 2030 (PERSU 2030), Resolução do Conselho de Ministros n.º 30/2023 | Governo de Portugal | pp. 1-29 (até antes de «5 — Gestão da fração residual»); pp. 49-105 (a partir de «8 — PERSU 2030») | 23 738 |
| E1-103 | Decreto-Lei n.º 102-D/2020, que aprova o Regime Geral da Gestão de Resíduos (versão consolidada de 26/03/2024) | Governo de Portugal | pp. 57-81 (de «Anexo I» até antes de «Capítulo IV»); pp. 84-86 (de «Capítulo V» até antes de «Artigo 48.º»); pp. 115-116 (de «Título IV» até antes de «Capítulo II»); p. 117 (de «Capítulo III» até antes de «Artigo 111.º»); pp. 132-135 (de «Anexo III» até antes de «Anexo VI») | 15 556 |
| E1-104 | Decreto-Lei n.º 152-D/2017, Regime Unificado dos Fluxos Específicos de Resíduos (versão consolidada de 30/12/2025) | Governo de Portugal | pp. 8-17 (de «Capítulo I» até antes de «Capítulo II»); pp. 23-25 (de «Artigo 13.º» até antes de «Artigo 14.º»); pp. 33-39 (de «Secção I» até antes de «Artigo 26.º»); pp. 43-47 (de «Subsecção I» até antes de «Artigo 30.º-J»); pp. 54-55 (de «Artigo 30.º-T» até antes de «Artigo 30.º-V»); pp. 64-72 (de «Secção IV» até antes de «Artigo 69.º»); pp. 72-76 (de «Secção V» até antes de «Secção VI»); pp. 81-82 (de «Secção VII» até antes de «Capítulo IV») | 19 358 |
| E1-105 | Guia técnico de implementação de sistemas PAYT, SAYT ou RAYT nos Açores, volume 1 | Secretaria Regional do Ambiente e Alterações Climáticas dos Açores | pp. 4-20; pp. 46-50 (a partir de «4. SISTEMAS SAYT E RAYT»); pp. 60-68 (de «2.2. GUIMARÃES» até antes de «2.1. LOUSADA») | 9 288 |
| E1-106 | Perguntas frequentes: produtos têxteis, têxteis e calçado (dezembro de 2025) | Agência Portuguesa do Ambiente | pp. 3-7 | 1 615 |
| E1-107 | Nota técnica relativa à recolha seletiva de biorresíduos (janeiro de 2025) | Agência Portuguesa do Ambiente | documento inteiro | 801 |
| E1-109 | Publicada a Diretiva Europeia sobre a Reparação de Bens | Município de Vila Nova de Gaia (CIAC) | documento inteiro | 532 |
| E1-110 | Decreto-Lei n.º 84/2021, direitos do consumidor na compra e venda de bens, conteúdos e serviços digitais | Governo de Portugal | pp. 9-13 (de «SECÇÃO II» até antes de «SECÇÃO III»); pp. 21-23 (de «CAPÍTULO IV» até antes de «SECÇÃO II») | 3 045 |
| E1-111 | Estratégia Nacional e Plano de Ação de Combate ao Desperdício Alimentar, Resolução do Conselho de Ministros n.º 46/2018 | Governo de Portugal | pp. 1-13 (de «Resolução do Conselho de Ministros n.º 46/2018» até antes de «NEGÓCIOS ESTRANGEIROS») | 9 958 |
| E1-112 | Plano Nacional de Gestão de Resíduos 2030 (PNGR 2030), Resolução do Conselho de Ministros n.º 31/2023 | Governo de Portugal | pp. 26-40 | 7 744 |
| E1-114 | Circular n.º 01/2026/DFEMR: período de transição do Sistema de Depósito e Reembolso | Agência Portuguesa do Ambiente | documento inteiro | 901 |
| E1-119 | Embalagens e resíduos de embalagens: dados de 2022 | Agência Portuguesa do Ambiente | documento inteiro | 1 163 |
| E1-123 | Guia de boas práticas de redução e reutilização | LIPOR (Comunidades Reuse) | p. 2; pp. 4-17 | 1 257 |
| E1-126 | Objetivos intercalares alocados aos municípios e SGRU para o cumprimento das metas do PERSU 2030 (abril de 2024) | Agência Portuguesa do Ambiente | pp. 3-12; pp. 41-44 (até antes de «16. RSTJ») | 4 529 |

## 7. Pesquisas feitas (com o Claude)

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
