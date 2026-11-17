# Análise de erros (E1)

Por pergunta e experiência: os 5 excertos recuperados (✔ = acerta num trecho, pela regra do E1), os quase-acertos (trecho certo entre o 6.º e o 10.º), a resposta, os problemas detetados em código e as notas do juiz, se houver.

## E1-01 (factual): Em Guimarães, como devo deitar fora o óleo alimentar usado em casa?

**Referência:** Deve pô-lo numa garrafa de plástico fechada e colocá-la nos contentores próprios para óleos alimentares usados, que ficam junto aos ecopontos.

- Trecho E1-004 [31636, 31774): «Os OAU provenientes do sector doméstico devem ser acondicionados em garrafa de plástico, fechada, e colocada nos equipamentos específicos;»
- Trecho E1-004 [43527, 43725): «1 — A recolha seletiva de OAU provenientes do sector doméstico (habitações) processa-se por contentores, localizados junto aos ecopontos, em circuitos predefinidos em toda área de intervenção da EG.»

### A (dense, excertos A): Recall@5 0.5, RR 0.33

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_A0011 | 0.6006 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 2 | E1-003_A0010 | 0.5952 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |
| 3 | E1-004_A0023 | 0.5897 | ✔ | 3 — A Vitrus efetua a recolha de RU através de contentores e de sistemas Payt. 4 — À exceção do Município e de outras entidades, públicas ou… |
| 4 | E1-002_A0040 | 0.5805 |  | Na figura seguinte apresenta-se os alojamentos/hotéis com cozinha em Guimarães, verificandose que estes encontram-se maioritariamente na zon… |
| 5 | E1-004_A0015 | 0.5791 |  | Artigo 14.º Atendimento ao público 1 — O Município de Guimarães dispõe, de Balcão Único de Atendimento, de um serviço de atendimento telefón… |

**Resposta** (gemma4:12b, 1.85 s): A recolha seletiva de óleos alimentares usados provenientes do setor doméstico (habitações) processa-se por contentores, localizados junto aos ecopontos, em circuitos predefinidos em toda a área de intervenção da entidade gestora [E1-004]. A entidade responsável pela recolha, transporte e destino final dos óleos alimentares usados é a Resinorte [E1-004]. Além disso, os habitantes do Município de Guimarães podem efetuar a entrega de óleos alimentares usados nos dois Ecocentros localizados nas freguesias de Aldão e Ponte [E1-001] [E1-003].

**Problemas em código:** pesquisa_parcial, correcao_1
**Juiz** (gpt-oss-120b): correção 1 (A resposta menciona os contentores junto aos ecopontos, mas omite a necessidade de colocar o óleo numa garrafa de plástico fechada, informação essencial da referência.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas e as citações suportam-nas.)

### B (dense, excertos B): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-004_B0061 | 0.6547 | ✔ | Artigo 31.º Transporte O transporte de resíduos é da responsabilidade da EG, tendo por destino final a Estação de Tratamento de Resíduos Urb… |
| 2 | E1-001_B0086 | 0.5903 |  | MEDIDA 7 – Combate ao Desperdício Alimentar (Ação OB.I.5.6) Conscientes que o desperdício alimentar é uma das principais fontes de produção … |
| 3 | E1-001_B0026 | 0.5893 |  | Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) Papel e embalagens de cartão 2 vezes por semana (ci… |
| 4 | E1-004_B0045 | 0.5884 | ✔ | d) Não é permitido o despejo de OAU nos contentores destinados a RU, nas vias ou outros espaços públicos, bem como o despejo nos sistemas de… |
| 5 | E1-003_B0027 | 0.5876 |  | Resíduos recolhidos em Ecocentros Os habitantes do Município de Guimarães usam 2 Ecocentros (Aldão e Ponte) para entregas de resíduos não re… |

**Resposta** (gemma4:12b, 2.15 s): Os óleos alimentares usados (OAU) provenientes do setor doméstico devem ser acondicionados em garrafas de plástico fechadas e colocados nos equipamentos específicos [E1-004]. A recolha seletiva destes resíduos processa-se por contentores localizados junto aos ecopontos, em circuitos predefinidos em toda a área de intervenção da EG [E1-004]. Não é permitido o despejo de OAU nos contentores destinados a resíduos urbanos, nas vias ou outros espaços públicos, nem nos sistemas de drenagem, individuais ou coletivos, incluindo sarjetas e sumidouros [E1-004]. Adicionalmente, os habitantes do Município de Guimarães podem entregar óleos alimentares usados nos Ecocentros localizados nas freguesias de Aldão e Ponte [E1-001] [E1-003].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (Inclui toda a informação essencial da referência e não contém erros.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas de citações que correspondem aos excertos e suportam as informações.)

### C (hybrid, excertos A): Recall@5 0.5, RR 0.33

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-003_A0010 | 0.031514 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |
| 2 | E1-001_A0011 | 0.030679 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 3 | E1-004_A0023 | 0.029958 | ✔ | 3 — A Vitrus efetua a recolha de RU através de contentores e de sistemas Payt. 4 — À exceção do Município e de outras entidades, públicas ou… |
| 4 | E1-004_A0007 | 0.02904 |  | p) Estação de Transferência — instalação onde o resíduo é descarregado com o objetivo de o preparar para ser transportado para outro local d… |
| 5 | E1-001_A0040 | 0.028778 |  | O Município de Guimarães, pretende ainda, implementar um sistema de bonificação para os cidadãos que promovam a compostagem doméstica e comu… |

**Resposta** (gemma4:12b, 2.76 s): A recolha seletiva de óleos alimentares usados (OAU) provenientes do setor doméstico processa-se por contentores, localizados junto aos ecopontos, em circuitos predefinidos em toda a área de intervenção da entidade gestora [E1-004]. A entidade responsável pela recolha, transporte e destino final dos OAU é a Resinorte [E1-004]. Além disso, o Município de Guimarães pretende reforçar a aquisição e implementação de novos equipamentos de contentores por proximidade para os OAU, bem como manter e reforçar a recolha porta-a-porta (PaP) deste fluxo, em conjunto com a implementação do sistema PAYT a todo o Município [E1-001].

**Problemas em código:** pesquisa_parcial, correcao_1
**Juiz** (gpt-oss-120b): correção 1 (A resposta menciona os contentores junto aos ecopontos, mas omite a necessidade de colocar o óleo numa garrafa de plástico fechada, informação essencial da referência.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas por citações que correspondem a excertos que as suportam.)

## E1-02 (factual): Posso pôr copos e pratos partidos no ecoponto do vidro? Se não, onde os devo pôr?

**Referência:** Não. Copos, pratos, chávenas, cristal e espelhos não vão para o ecoponto do vidro; a loiça partida vai para os resíduos indiferenciados.

- Trecho E1-014 [1181, 1431): «Vidro
Deve colocar: Garrafas de bebidas e azeite, boiões de conserva e doces, frascos de perfume e cosmética.
Não deve colocar: Lâmpadas, chávenas, copos, pratos, cristal, espelhos, vidraças, material de construção civil…»
- Trecho E1-014 [2335, 2573): «Resíduos Indeferenciados
Deve colocar: Papel higiénico, guardanapos e lenços de papel, cartão com gordura, loiça partida, sacos de cimento vazios, restos de comida, fraldas, espelhos, etc e outros materiais cuja reciclag…»

### A (dense, excertos A): Recall@5 0.5, RR 0.33

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-101_A0016 | 0.6121 |  | Salientar que no caso do vidro, os contaminantes integram-se, em grande parte (47%), na categoria “finos”, pelo que podem corresponder també… |
| 2 | E1-001_A0012 | 0.5744 |  | Porta-a-porta vidro	VITRUS	PAYT Porta-a-porta papel/cartão	VITRUS	PAYT RESINORTE-Urgezes Porta-a-porta embalagens plásticas e metálicas VITR… |
| 3 | E1-014_A0001 | 0.5735 | ✔ | Nunca fiz a Separação. Como devo fazer? Se a separação de resíduos ainda não for um hábito para si, então poderá estranhar um pouco no iníci… |
| 4 | E1-001_A0011 | 0.5716 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 5 | E1-123_A0005 | 0.5604 |  | Pode doar a familiares, amigos, instituições Pode modificar e transformar numa nova peça diy, oficina de restauro Entregue no ecocentro em b… |

Quase-acertos: E1-014_A0002 em 6.º

**Resposta** (gemma4:12b, 2.93 s): Não deve colocar copos, pratos ou chávenas no ecoponto do vidro [E1-014]. No entanto, os excertos não indicam especificamente onde deve colocar estes itens, mencionando apenas que os resíduos não recolhidos por ecopontos ou pelo sistema de recolha porta-a-porta podem ser entregues em ecocentros [E1-001].

**Problemas em código:** pesquisa_parcial, correcao_1, afirmacoes_nao_suportadas, citacoes_1
**Juiz** (gpt-oss-120b): correção 1 (A resposta indica corretamente que não se deve colocar copos e pratos no ecoponto do vidro, mas não indica que a loiça partida deve ir para os resíduos indiferenciados, omitindo informação essencial.); fidelidade 0.667; citações 1 (Uma das afirmações tem citação que não suporta o conteúdo, por isso a nota de citações é 1.)
- não suportada: Os excertos não indicam especificamente onde deve colocar estes itens.

### B (dense, excertos B): Recall@5 0.5, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-014_B0003 | 0.6131 | ✔ | Não deve colocar: Lâmpadas, chávenas, copos, pratos, cristal, espelhos, vidraças, material de construção civil e embalagens de medicamentos.… |
| 2 | E1-101_B0043 | 0.6095 |  | Salientar que no caso do vidro, os contaminantes integram-se, em grande parte (47%), na categoria “finos”, pelo que podem corresponder també… |
| 3 | E1-001_B0026 | 0.6062 |  | Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) Papel e embalagens de cartão 2 vezes por semana (ci… |
| 4 | E1-003_B0026 | 0.6011 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 5 | E1-001_B0028 | 0.5684 |  | Porta-a-porta com contentores e sacos VITRUS	PAYT Porta-a-porta com sacos	Município e VITRUS De proximidade com contentores de superfície Mu… |

**Resposta** (gemma4:12b, 2.61 s): Não deve colocar copos, pratos ou chávenas no ecoponto do vidro [E1-014]. Os excertos não indicam onde deve colocar especificamente estes itens, mas mencionam que os habitantes do Município de Guimarães podem entregar resíduos não recolhidos por ecopontos nos Ecocentros localizados nas freguesias de Aldão e Ponte [E1-001].

**Problemas em código:** pesquisa_parcial, correcao_1, afirmacoes_nao_suportadas, citacoes_1
**Juiz** (gpt-oss-120b): correção 1 (Falta indicar que a loiça partida deve ir para resíduos indiferenciados, apesar de acertar que não vai ao ecoponto do vidro.); fidelidade 0.667; citações 1 (Falta citação para a afirmação de que os excertos não indicam onde colocar os itens.)
- não suportada: Os excertos não indicam onde deve colocar especificamente estes itens.

### C (hybrid, excertos A): Recall@5 0.5, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-014_A0001 | 0.032266 | ✔ | Nunca fiz a Separação. Como devo fazer? Se a separação de resíduos ainda não for um hábito para si, então poderá estranhar um pouco no iníci… |
| 2 | E1-101_A0016 | 0.031545 |  | Salientar que no caso do vidro, os contaminantes integram-se, em grande parte (47%), na categoria “finos”, pelo que podem corresponder també… |
| 3 | E1-001_A0012 | 0.030214 |  | Porta-a-porta vidro	VITRUS	PAYT Porta-a-porta papel/cartão	VITRUS	PAYT RESINORTE-Urgezes Porta-a-porta embalagens plásticas e metálicas VITR… |
| 4 | E1-001_A0011 | 0.030118 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 5 | E1-003_A0010 | 0.029631 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |

Quase-acertos: E1-014_A0002 em 6.º

**Resposta** (gemma4:12b, 3.68 s): Não deve colocar copos, pratos e chávenas no ecoponto do vidro [E1-014]. Os habitantes do Município de Guimarães podem entregar estes resíduos, que não são recolhidos indiferenciadamente ou por ecopontos, nos 2 Ecocentros localizados nas freguesias de Aldão e Ponte [E1-001] [E1-003].

**Problemas em código:** pesquisa_parcial, correcao_0
**Juiz** (gpt-oss-120b): correção 0 (A resposta indica que a loiça partida deve ser entregue nos Ecocentros, contradizendo a referência que afirma que deve ir para os resíduos indiferenciados.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas e os excertos suportam‑nas.)

## E1-03 (factual): Tenho um sofá velho em casa, em Guimarães. Como me desfaço dele e quanto custa?

**Referência:** Os sofás, tal como os móveis, os colchões e os eletrodomésticos, são «monstros» e não podem ser deixados na rua. Há duas formas, e qualquer uma basta: contactar a Vitrus Ambiente para agendar a recolha, que é gratuita, ou levá-lo a um ecocentro.

**Nota sobre a referência:** A referência foi completada a 15/11. O regulamento municipal (E1-004, art. 38.º) também manda levar os volumosos aos ecocentros, e antes as respostas que iam por aí levavam 0 por «contradizerem» a referência (como na E2-02). Ficou «Há duas formas, e qualquer uma basta: contactar a Vitrus Ambiente para agendar a recolha, que é gratuita, ou levá-lo a um ecocentro», sem dizer de que entidade, para valer tanto para os ecocentros de Aldão e Ponte (E1-001) como para os da Resinorte (E1-004). Os trechos continuam os do E1-014. Mesmo assim, os dois juízes leem as duas formas como obrigatórias: com o 120b, a resposta só com a Vitrus e a recolha gratuita (B) desce de 2 para 1, por omitir a alternativa do ecocentro. As notas antes e depois estão no docs/pipeline_E1_15-11.md.

- Trecho E1-014 [3220, 3348): «Consideramos monstros tudo o que sejam móveis, sofás, colchões, eletrodomésticos, roupa ou outros têxteis, resíduos verdes, etc.»
- Trecho E1-014 [3448, 3587): «Por isso, se tiver algum monstro em sua casa/estabelecimento, nunca o abandone na rua. Contacte a VITRUS para agendar uma recolha gratuita.»

### A (dense, excertos A): Recall@5 0.0, RR 0.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_A0032 | 0.5479 |  | Na estratégia e hierarquização da gestão de resíduos, a reutilização, surge como uma das mais favoráveis ações de valorização. Desta forma, … |
| 2 | E1-003_A0010 | 0.5351 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |
| 3 | E1-006_A0026 | 0.5309 |  | A seguir à indústria têxtil, a quarta indústria mais prevalente em Guimarães é a metalomecânica, ligada à construção e à produção de cutelar… |
| 4 | E1-004_A0015 | 0.5296 |  | Artigo 14.º Atendimento ao público 1 — O Município de Guimarães dispõe, de Balcão Único de Atendimento, de um serviço de atendimento telefón… |
| 5 | E1-001_A0011 | 0.5282 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |

Quase-acertos: E1-014_A0003 em 6.º

**Resposta** (gemma4:12b, 3.36 s): O Município de Guimarães classifica objetos domésticos volumosos fora de uso, como um sofá, como "monstros" ou "monos" [E1-004]. Estes resíduos podem ser entregues em dois Ecocentros localizados nas freguesias de Aldão e Ponte, onde os habitantes podem depositar resíduos não recolhidos indiferenciadamente, por ecopontos ou pelo sistema de recolha porta-a-porta [E1-001] [E1-003].

Não encontrei informação suficiente nas fontes disponíveis para responder a quanto custa o descarte do sofá.

**Problemas em código:** pesquisa_sem_acerto, correcao_1, juiz_abstencao_com_resposta_nos_excertos
**Juiz** (gpt-oss-120b): correção 1 (A resposta inclui a informação dos ecocentros mas omite a opção de recolha gratuita pela Vitrus Ambiente, que é essencial na referência.); fidelidade 1.0; citações 2 (Todas as afirmações factuais são acompanhadas de citações que as suportam nos excertos.)

### B (dense, excertos B): Recall@5 1.0, RR 0.2

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_B0080 | 0.5599 |  | Na estratégia e hierarquização da gestão de resíduos, a reutilização, surge como uma das mais favoráveis ações de valorização. Desta forma, … |
| 2 | E1-003_B0035 | 0.5424 |  | O Município promove o mercado de segunda-mão, disponibilizando um local para a venda de produtos e artigos usados nos primeiros e terceiros … |
| 3 | E1-001_B0027 | 0.5423 |  | Embalagens	Plásticos duros	Têxteis Madeira	Sucata As tabelas 4-9 a seguir apresentadas resumem a distribuição de recolha de resíduos pelas d… |
| 4 | E1-123_B0011 | 0.5339 |  | Anexo de atividades Móveis usados Sim	Não em mau estado pode ter reparação? Sim	Não carpinteiro, oficina de restauro pode modificar e transf… |
| 5 | E1-014_B0006 | 0.5293 | ✔ | Por exemplo: Monstros! Nós recolhemos. Consideramos monstros tudo o que sejam móveis, sofás, colchões, eletrodomésticos, roupa ou outros têx… |

**Resposta** (gemma4:12b, 2.0 s): O sofá é considerado um "monstro" devido às suas dimensões e não pode ser recolhido nos circuitos normais de recolha [E1-014]. Não deve abandonar o sofá na rua [E1-014]. Para se desfazer dele, deve contactar a VITRUS para agendar uma recolha gratuita [E1-014].

**Problemas em código:** correcao_1
**Juiz** (gpt-oss-120b): correção 1 (A resposta inclui a informação essencial de contactar a Vitrus para recolha gratuita, mas omite a alternativa de levar o sofá a um ecocentro.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas e suportadas pelo excerto E1-014.)

### C (hybrid, excertos A): Recall@5 0.0, RR 0.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-006_A0024 | 0.03055 |  | A nível local, em Guimarães, as condições demográficas e socioculturais amplificam estas lacunas regulamentares. O padrão de ocupação disper… |
| 2 | E1-003_A0014 | 0.027109 |  | “Urgezes Circular” 1 é o mote do projeto aprovado pelo Fundo Ambiental que é liderado pela Junta de Freguesia de Urgezes, em consórcio com o… |
| 3 | E1-004_A0015 | 0.026263 |  | Artigo 14.º Atendimento ao público 1 — O Município de Guimarães dispõe, de Balcão Único de Atendimento, de um serviço de atendimento telefón… |
| 4 | E1-001_A0052 | 0.024198 |  | Contudo, estes apoios não serão suficientes face à escala dos desafios e investimentos necessários ou face ao potencial acréscimo na tarifa … |
| 5 | E1-004_A0003 | 0.023615 |  | CAPÍTULO I Disposições gerais Artigo 1.º Lei habilitante O presente Regulamento é aprovado ao abrigo do disposto no artigo 62.º do Decreto-L… |

**Resposta** (gemma4:12b, 4.22 s): O Município de Guimarães classifica objetos domésticos volumosos fora de uso, como sofás, como "monstros" ou "monos" [E1-004]. O regulamento define as regras para a gestão destes resíduos sob a responsabilidade do município [E1-004].

Relativamente ao custo, o documento indica que o custo médio cobrado atualmente pela recolha de resíduos urbanos é de 79,12 €/alojamento/ano [E1-001]. No entanto, o tarifário indicativo para 2030, considerando os investimentos e a implementação de novos sistemas, será de 100 €/alojamento/ano [E1-001]. Não foram fornecidos detalhes sobre custos específicos para a recolha individual de um único objeto volumoso.

**Problemas em código:** pesquisa_sem_acerto, correcao_0
**Juiz** (gpt-oss-120b): correção 0 (A resposta não indica as duas formas corretas de descarte (contactar a Vitrus Ambiente ou levar a um ecocentro) e fornece informação de custos que não constam na referência.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas de citações que correspondem aos excertos que as suportam.)

## E1-04 (factual): Para onde vão os resíduos indiferenciados recolhidos em Guimarães?

**Referência:** Vão todos para a estação de tratamento mecânico e biológico da RESINORTE, a entidade gestora em alta; uma percentagem elevada do refugo dessa estação acaba depois em aterro.

- Trecho E1-001 [18413, 18722), grupo 1: «100% dos resíduos urbanos (Resíduos indiferenciados), recolhidos no Município de Guimarães são enviados para a estação de tratamento mecânico e biológico, da entidade gestora em alta RESINORTE, no entanto, existe ainda u…»
- Trecho E1-003 [19556, 19865), grupo 1: «100% dos resíduos urbanos (Resíduos indiferenciados), recolhidos no Município de Guimarães são enviados para a estação de tratamento mecânico e biológico, da entidade gestora em Alta RESINORTE, no entanto, existe ainda u…»

### A (dense, excertos A): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_A0011 | 0.8139 | ✔ | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 2 | E1-003_A0010 | 0.8093 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |
| 3 | E1-003_A0011 | 0.8047 | ✔ | 2.2 RECUPERAÇÃO DE RESÍDUOS RECOLHIDOS SEPARADOS a) Por favor, especifique quem recolhe os resíduos indiferenciados. Porta-a-porta com conte… |
| 4 | E1-003_A0009 | 0.7847 |  | 2. ENQUADRAMENTO DA GESTÃO DE RESÍDUOS NO MUNICÍPIO Tipo de resíduos	Frequência de recolha de resíduos Resíduos indiferenciados	Diariamente … |
| 5 | E1-001_A0008 | 0.7795 |  | São Tiago e Mascotelos, Polvoreira, Pinheiro, e parcelas residuais de Atães e Rendufe, Aldão e Ponte fazem parte desse grupo. A cidade esten… |

**Resposta** (gemma4:12b, 3.94 s): 100% dos resíduos urbanos (Resíduos indiferenciados) recolhidos no Município de Guimarães são enviados para a estação de tratamento mecânico e biológico da entidade gestora em alta, a RESINORTE [E1-001] [E1-003]. No entanto, existe uma elevada percentagem de refugo da Estação que é posteriormente encaminhada para aterro [E1-001]. No ano de 2022, 79% dos resíduos do município tiveram como destino final a deposição em aterro [E1-001].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (Inclui toda a informação essencial da referência e não contém erros.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas de citações que correspondem a excertos que as suportam.)

### B (dense, excertos B): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_B0027 | 0.8409 | ✔ | Embalagens	Plásticos duros	Têxteis Madeira	Sucata As tabelas 4-9 a seguir apresentadas resumem a distribuição de recolha de resíduos pelas d… |
| 2 | E1-003_B0027 | 0.8178 |  | Resíduos recolhidos em Ecocentros Os habitantes do Município de Guimarães usam 2 Ecocentros (Aldão e Ponte) para entregas de resíduos não re… |
| 3 | E1-002_B0056 | 0.8012 |  | O Município de Guimarães é a Entidade Gestora responsável pela recolha indiferenciada em toda a área do Município, exceto nas zonas onde a r… |
| 4 | E1-003_B0029 | 0.7887 | ✔ | 100% dos resíduos urbanos (Resíduos indiferenciados), recolhidos no Município de Guimarães são enviados para a estação de tratamento mecânic… |
| 5 | E1-003_B0021 | 0.7878 |  | Não incluem: • Resíduos de redes de esgotos e tratamento de esgoto, incluindo as lamas de depuração; • Resíduos de construção e demolição e … |

**Resposta** (gemma4:12b, 2.74 s): 100% dos resíduos urbanos (resíduos indiferenciados) recolhidos no Município de Guimarães são enviados para a estação de tratamento mecânico e biológico da entidade gestora em alta, a RESINORTE [E1-001] [E1-003]. No entanto, existe uma elevada percentagem de refugo desta estação que é posteriormente encaminhada para aterro [E1-001] [E1-003]. No ano de 2022, 79% dos resíduos do município tiveram como destino final a deposição em aterro [E1-001].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (Inclui toda a informação essencial da referência e não contém erros.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas e as citações suportam-nas.)

### C (hybrid, excertos A): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_A0011 | 0.031545 | ✔ | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 2 | E1-003_A0008 | 0.031025 |  | Estes resíduos são recolhidos pelos municípios ou por outras entidades a quem pode ser adjudicado/ concessionado o serviço. • Os resíduos ur… |
| 3 | E1-001_A0006 | 0.03055 |  | Este ponto não é aplicável ao Município de Guimarães, uma vez que não foi elaborado o PAPERSU no âmbito do PERSU 2020 e 2020+. 3 Descrição d… |
| 4 | E1-002_A0020 | 0.030478 |  | As características detalhadas de cada território de Guimarães, devem ser consideradas na definição da solução mais adequada para a implement… |
| 5 | E1-004_A0005 | 0.029211 |  | Artigo 5.º Entidade Titular e Entidade Gestora do sistema 1 — O Município de Guimarães é a ET que, nos termos da lei, tem por atribuição ass… |

**Resposta** (gemma4:12b, 3.0 s): Os resíduos urbanos (resíduos indiferenciados) recolhidos no Município de Guimarães são enviados para a estação de tratamento mecânico e biológico da entidade gestora em alta, a RESINORTE [E1-001]. No ano de 2022, 79% destes resíduos tiveram como destino final a deposição em aterro [E1-001].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (Inclui toda a informação essencial da referência e não contém erros.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas com [E1-001] e o excerto suporta-as.)

## E1-05 (factual): No tarifário de resíduos de Guimarães para 2026, que desconto tem quem comprova que separa os orgânicos?

**Referência:** Tem uma redução de 50% na tarifa variável.

**Nota sobre a referência:** Decisão de 8/11: o PAPERSU (E1-001) descreve um reembolso de 50% da tarifa variável, mas em dezembro de 2024 e com outras condições. Não entra como trecho alternativo: é informação parecida noutro documento.

- Trecho E1-007 [1020, 1112): «Redução de 50% da tarifa variável, para utilizadores que comprovem a separação dos orgânicos»

### A (dense, excertos A): Recall@5 0.0, RR 0.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_A0028 | 0.7625 |  | PAYT para 0,026€/L, como forma de desincentivar a sua deposição. Relativamente à aplicação do sistema SAYR, o novo sistema tarifário será re… |
| 2 | E1-001_A0052 | 0.7175 |  | Contudo, estes apoios não serão suficientes face à escala dos desafios e investimentos necessários ou face ao potencial acréscimo na tarifa … |
| 3 | E1-001_A0040 | 0.7128 |  | O Município de Guimarães, pretende ainda, implementar um sistema de bonificação para os cidadãos que promovam a compostagem doméstica e comu… |
| 4 | E1-001_A0049 | 0.6838 |  | RU	ton 71175 70665 71175 71175 71175 71089 69049 64378 60426 Capitação Produção de RU Kg/hab 454	451	454	454	454	453	440	410	385 6.1.2. Reco… |
| 5 | E1-001_A0027 | 0.6797 |  | 72/2010, de 4 de fevereiro. Nos locais com implementação do sistema PAYT, é realizada a distinção entre métodos de quantificação, nomeadamen… |

**Resposta** (gemma4:12b, 2.13 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** pesquisa_sem_acerto, abstencao_sem_trecho_nos_excertos, correcao_0, afirmacoes_nao_suportadas, citacoes_0, juiz_abstencao_com_resposta_nos_excertos
**Juiz** (gpt-oss-120b): correção 0 (A resposta do sistema não fornece a informação da redução de 50% e afirma falta de dados, contradizendo a referência.); fidelidade 0.0; citações 0 (Não foram incluídas citações e a afirmação não é suportada pelos excertos.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

### B (dense, excertos B): Recall@5 0.0, RR 0.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_B0100 | 0.7228 |  | Relativamente à aplicação do sistema SAYR, o novo sistema tarifário será realizado através do reembolso de 50% da tarifa variável, em dezemb… |
| 2 | E1-001_B0069 | 0.7036 |  | A visão estratégica do município de Guimarães, de acordo com o PAPERSU 2030, visa alargar o sistema PAYT a todo município até ao ano 2030 e … |
| 3 | E1-001_B0070 | 0.7003 |  | PAYT para 0,026€/L, como forma de desincentivar a sua deposição. Relativamente à aplicação do sistema SAYR, o novo sistema tarifário será re… |
| 4 | E1-105_B0083 | 0.6995 |  | 12 De referir ainda neste enquadramento, e tendo em consideração o novo plano de recolha seletiva de biorresíduos que teve início em 2022 no… |
| 5 | E1-003_B0056 | 0.6858 |  | 4. COMISSÃO DE ACOMPANHAMENTO DA EXECUÇÃO DO COMPROMISSO O Município de Guimarães compromete-se, até ao ano 2030, a criar condições que lhe … |

**Resposta** (gemma4:12b, 1.43 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** pesquisa_sem_acerto, abstencao_sem_trecho_nos_excertos, correcao_0, afirmacoes_nao_suportadas, citacoes_0, juiz_abstencao_com_resposta_nos_excertos
**Juiz** (gpt-oss-120b): correção 0 (A resposta do sistema não fornece a informação da redução de 50% e afirma falta de dados, contradizendo a referência.); fidelidade 0.0; citações 0 (Nenhuma citação foi incluída e, portanto, não há suporte às afirmações.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

### C (hybrid, excertos A): Recall@5 0.0, RR 0.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_A0028 | 0.032522 |  | PAYT para 0,026€/L, como forma de desincentivar a sua deposição. Relativamente à aplicação do sistema SAYR, o novo sistema tarifário será re… |
| 2 | E1-001_A0052 | 0.032522 |  | Contudo, estes apoios não serão suficientes face à escala dos desafios e investimentos necessários ou face ao potencial acréscimo na tarifa … |
| 3 | E1-001_A0040 | 0.031498 |  | O Município de Guimarães, pretende ainda, implementar um sistema de bonificação para os cidadãos que promovam a compostagem doméstica e comu… |
| 4 | E1-001_A0027 | 0.03031 |  | 72/2010, de 4 de fevereiro. Nos locais com implementação do sistema PAYT, é realizada a distinção entre métodos de quantificação, nomeadamen… |
| 5 | E1-015_A0001 | 0.028039 |  | PAYT: Pague pelo resíduo que produz. Reciclar para poupar! Centro da cidade. Tarifário Payt Método B Assim no método B (pré-definido), o cál… |

Quase-acertos: E1-007_A0001 em 7.º

**Resposta** (gemma4:12b, 2.09 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** pesquisa_sem_acerto, abstencao_sem_trecho_nos_excertos, correcao_0, juiz_abstencao_com_resposta_nos_excertos
**Juiz** (gpt-oss-120b): correção 0 (A resposta do sistema não fornece a informação da redução de 50% e afirma falta de dados, contradizendo a referência.); fidelidade None; citações None (Não foram apresentadas citações, apesar de os excertos conterem informação relevante.)

## E1-06 (factual): Que objetos se podiam trocar ou vender no Mercado das Trocas de equipamentos elétricos e eletrónicos de Guimarães, e em que estado tinham de estar?

**Referência:** Só equipamentos elétricos e eletrónicos usados e em bom estado: pequenos eletrodomésticos, equipamentos informáticos e de telecomunicações, equipamentos de consumo (rádios, câmaras, leitores), iluminação, ferramentas elétricas e eletrónicas, e brinquedos e equipamentos de lazer eletrónicos. Tinham de estar limpos, funcionais e em condições de utilização segura.

- Trecho E1-013 [2205, 2675): «1. São admitidos a troca/ venda apenas objetos usados em bom estado de conservação, nomeadamente:
a) Pequenos eletrodomésticos;
b) Equipamentos informáticos e de telecomunicações;
c) Equipamentos de consumo (rádios, câma…»

### A (dense, excertos A): Recall@5 1.0, RR 0.33

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-013_A0001 | 0.8116 |  | Normas de Participação no Mercado das Trocas – Edição Equipamentos Elétricos e Eletrónicos No âmbito da Semana Europeia da Prevenção de Resí… |
| 2 | E1-013_A0003 | 0.7267 |  | 2. Os resíduos gerados devem ser depositados nos contentores adequados à separação seletiva. 3. O Município disponibilizará recipientes próp… |
| 3 | E1-013_A0002 | 0.6861 | ✔ | 3. O pedido de inscrição deve incluir: a) Nome e contacto do participante; b) Breve descrição dos objetos a trocar ou vender; c) 1 a 2 fotog… |
| 4 | E1-025_A0001 | 0.6183 |  | 4 Mercado Municipal O Mercado Municipal de Guimarães destaca-se pela oferta de produtos frescos e pelo incentivo ao consumo local, fortalece… |
| 5 | E1-123_A0005 | 0.6182 |  | Pode doar a familiares, amigos, instituições Pode modificar e transformar numa nova peça diy, oficina de restauro Entregue no ecocentro em b… |

**Resposta** (gemma4:12b, 2.98 s): São admitidos para troca ou venda apenas objetos usados em bom estado de conservação [E1-013]. Estes objetos devem estar limpos, funcionais e em condições de utilização segura [E1-013]. Estão especificamente admitidos: pequenos eletrodomésticos; equipamentos informáticos e de telecomunicações; equipamentos de consumo (rádios, câmaras, leitores, etc.); iluminação (candeeiros, lâmpadas, projetores); ferramentas elétricas e eletrónicas; e brinquedos e equipamentos de lazer eletrónicos [E1-013]. É interdita a exposição de produtos contrafeitos, danificados, perigosos ou não funcionais [E1-013].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (Contém toda a informação essencial da referência e não apresenta erros.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas por citação [E1-013] que as suporta.)

### B (dense, excertos B): Recall@5 1.0, RR 0.33

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-013_B0002 | 0.8377 |  | Artigo 1.º Objetivo O Mercado das Trocas tem como objetivo promover a reutilização e valorização de equipamentos elétricos e eletrónicos (EE… |
| 2 | E1-013_B0001 | 0.7804 |  | Normas de Participação no Mercado das Trocas – Edição Equipamentos Elétricos e Eletrónicos No âmbito da Semana Europeia da Prevenção de Resí… |
| 3 | E1-013_B0004 | 0.7574 | ✔ | Artigo 5.º Condições de Participação 1. São admitidos a troca/ venda apenas objetos usados em bom estado de conservação, nomeadamente: a) Pe… |
| 4 | E1-013_B0007 | 0.6681 |  | Artigo 9.º Disposições Finais 1. A participação no Mercado das Trocas – Edição Equipamentos Elétricos e Eletrónicos implica a aceitação inte… |
| 5 | E1-003_B0035 | 0.6518 |  | O Município promove o mercado de segunda-mão, disponibilizando um local para a venda de produtos e artigos usados nos primeiros e terceiros … |

**Resposta** (gemma4:12b, 2.8 s): São admitidos para troca ou venda apenas objetos usados em bom estado de conservação [E1-013]. Estes objetos devem estar limpos, funcionais e em condições de utilização segura [E1-013]. Os artigos permitidos incluem pequenos eletrodomésticos, equipamentos informáticos e de telecomunicações, equipamentos de consumo (como rádios, câmaras e leitores), iluminação (candeeiros, lâmpadas e projetores), ferramentas elétricas e eletrónicas, bem como brinquedos e equipamentos de lazer eletrónicos [E1-013]. É expressamente interdita a exposição de produtos contrafeitos, danificados, perigosos ou não funcionais [E1-013].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (A resposta contém todas as categorias e condições indicadas na referência, sem erros.); fidelidade 1.0; citações 2 (Todas as afirmações têm citação [E1-013] e o excerto citado suporta-as.)

### C (hybrid, excertos A): Recall@5 1.0, RR 0.33

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-013_A0001 | 0.032787 |  | Normas de Participação no Mercado das Trocas – Edição Equipamentos Elétricos e Eletrónicos No âmbito da Semana Europeia da Prevenção de Resí… |
| 2 | E1-013_A0003 | 0.032258 |  | 2. Os resíduos gerados devem ser depositados nos contentores adequados à separação seletiva. 3. O Município disponibilizará recipientes próp… |
| 3 | E1-013_A0002 | 0.031746 | ✔ | 3. O pedido de inscrição deve incluir: a) Nome e contacto do participante; b) Breve descrição dos objetos a trocar ou vender; c) 1 a 2 fotog… |
| 4 | E1-123_A0004 | 0.030777 |  | Antes de comprar, reutilize bens que já existem. E lembre-se sempre de dar uma nova vida aqueles de que já não precisa. Bancos de Bens Adira… |
| 5 | E1-102_A0060 | 0.029274 |  | Associações empresariais Setor comercial Divulgação de dois guias de boas práticas direcionados para dois setores 2023 Medida OB.I.5 Capacit… |

**Resposta** (gemma4:12b, 4.03 s): No Mercado das Trocas de Guimarães, são admitidos para troca ou venda apenas objetos usados em bom estado de conservação [E1-013]. Estes objetos devem estar limpos, funcionais e em condições de utilização segura [E1-013]. Estão especificamente admitidos: pequenos eletrodomésticos; equipamentos informáticos e de telecomunicações; equipamentos de consumo (como rádios, câmaras e leitores); iluminação (candeeiros, lâmpadas e projetores); ferramentas elétricas e eletrónicas; e brinquedos e equipamentos de lazer eletrónicos [E1-013]. É expressamente proibida a exposição de produtos que estejam danificados, perigosos ou não funcionais, bem como produtos contrafeitos [E1-013].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (A resposta inclui todas as categorias e requisitos de estado indicados na referência, sem erros.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas por citação [E1-013] que as suporta.)

## E1-07 (factual): Durante quanto tempo é o produtor obrigado a ter peças para reparar um bem que comprei?

**Referência:** Durante 10 anos depois de colocar no mercado a última unidade desse bem.

- Trecho E1-110 [11308, 11648): «1 — Sem prejuízo do cumprimento dos deveres inerentes à responsabilidade do profissional ou do produtor pela falta de conformidade dos bens, o produtor é obrigado a disponibilizar as peças necessárias à reparação dos ben…»

### A (dense, excertos A): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-110_A0007 | 0.7596 | ✔ | 8 — O profissional deve proceder à remoção dos bens sempre que a resolução do contrato de compra e venda assim o exija, a título gratuito. A… |
| 2 | E1-110_A0005 | 0.6992 |  | c) Sem grave inconveniente para o consumidor, tendo em conta a natureza dos bens e a finalidade a que o consumidor os destina. 3 — O prazo p… |
| 3 | E1-110_A0001 | 0.6819 |  | SECÇÃO II Responsabilidade do profissional, prazos de conformidade, ónus da prova e direitos do consumidor Artigo 12.º Responsabilidade do p… |
| 4 | E1-109_A0001 | 0.6772 |  | Publicada a Diretiva Europeia sobre a Reparação de Bens Foi hoje publicada no Jornal Oficial da União Europeia a Diretiva (UE) 2024/1799 do … |
| 5 | E1-110_A0004 | 0.6448 |  | 9 — O direito à resolução do contrato ou à redução proporcional do preço pode ser exercido quando a falta de conformidade tenha levado ao pe… |

**Resposta** (gemma4:12b, 3.2 s): O produtor é obrigado a disponibilizar as peças necessárias à reparação dos bens adquiridos pelo consumidor durante o prazo de 10 anos após a colocação em mercado da última unidade do respetivo bem [E1-110]. Esta obrigação não se aplica a bens perecíveis, bens cuja natureza seja incompatível com o prazo referido ou bens cuja obrigatoriedade de disponibilização de peças esteja prevista em regulamentação específica da União Europeia em matéria de conceção ecológica, a qual prevalece [E1-110].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (Inclui a informação essencial (10 anos) e não contém erros.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas de citação [E1-110] que as suporta.)

### B (dense, excertos B): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-110_B0015 | 0.7284 | ✔ | 7 — Sem prejuízo do disposto no número anterior, e salvo situações em que incumba ao profissional a recolha do bem, o profissional pode proc… |
| 2 | E1-110_B0011 | 0.7206 |  | 3 — O prazo para a reparação ou substituição não deve exceder os 30 dias, salvo nas situações em que a natureza e complexidade dos bens, a g… |
| 3 | E1-110_B0016 | 0.6814 |  | 2 — A obrigação prevista no número anterior não é aplicável a bens cuja obrigatoriedade de disponibilização de peças esteja prevista em regu… |
| 4 | E1-110_B0018 | 0.6806 |  | b) Não tenha colocado o bem, conteúdo ou serviço digital em circulação; c) Possa considerar-se, tendo em conta as circunstâncias, que a não … |
| 5 | E1-110_B0022 | 0.6754 |  | 4 — Nos casos em que o produtor oferece ao consumidor uma garantia comercial de durabilidade do bem durante um determinado período tempo, o … |

**Resposta** (gemma4:12b, 2.74 s): O produtor é obrigado a disponibilizar as peças necessárias à reparação dos bens adquiridos pelo consumidor durante o prazo de 10 anos após a colocação em mercado da última unidade do respetivo bem [E1-110]. Esta obrigação não se aplica a bens perecíveis, bens cuja natureza seja incompatível com o prazo referido ou bens cuja obrigatoriedade de disponibilização de peças esteja prevista em regulamentação específica da União Europeia em matéria de conceção ecológica, a qual prevalece [E1-110]. No momento da celebração do contrato, o profissional deve informar o consumidor sobre a existência e duração desta obrigação de disponibilização de peças [E1-110].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (Contém a informação essencial (10 anos após a última unidade) e não contradiz a referência.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas por citações [E1-110] que suportam diretamente o conteúdo.)

### C (hybrid, excertos A): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-110_A0007 | 0.032787 | ✔ | 8 — O profissional deve proceder à remoção dos bens sempre que a resolução do contrato de compra e venda assim o exija, a título gratuito. A… |
| 2 | E1-110_A0005 | 0.031754 |  | c) Sem grave inconveniente para o consumidor, tendo em conta a natureza dos bens e a finalidade a que o consumidor os destina. 3 — O prazo p… |
| 3 | E1-109_A0001 | 0.031498 |  | Publicada a Diretiva Europeia sobre a Reparação de Bens Foi hoje publicada no Jornal Oficial da União Europeia a Diretiva (UE) 2024/1799 do … |
| 4 | E1-110_A0009 | 0.030536 |  | 1 — O profissional pode exercer o direito de regresso na ação judicial intentada pelo consumidor, aplicando-se, com as necessárias adaptaçõe… |
| 5 | E1-110_A0004 | 0.03031 |  | 9 — O direito à resolução do contrato ou à redução proporcional do preço pode ser exercido quando a falta de conformidade tenha levado ao pe… |

**Resposta** (gemma4:12b, 3.28 s): O produtor é obrigado a disponibilizar as peças necessárias à reparação dos bens adquiridos pelo consumidor durante o prazo de 10 anos após a colocação em mercado da última unidade do respetivo bem [E1-110]. Esta obrigação não se aplica a bens perecíveis, bens cuja natureza seja incompatível com o referido prazo ou bens cuja obrigatoriedade de disponibilização de peças esteja prevista em regulamentação específica da União Europeia em matéria de conceção ecológica [E1-110].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (Inclui a informação essencial (10 anos após a última unidade) e não contém erros.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas e as citações correspondem ao conteúdo do excerto.)

## E1-08 (factual): Em Guimarães, que coima pode ter quem deita uma ponta de cigarro para o chão na rua?

**Referência:** É proibido deitar pontas de cigarro no espaço público, e a infração é punível com uma coima de 25 € a 250 €.

- Trecho E1-005 [21411, 21530): «É proibido o descarte em espaço público de pontas de cigarros, charutos ou outros cigarros contendo produtos de tabaco.»
- Trecho E1-005 [22810, 22926): «1 — Constitui contraordenação punível com coima mínima de 25,00 € e máxima de 250,00 €, o incumprimento do disposto:»
- Trecho E1-005 [23447, 23507): «e) O incumprimento da proibição estabelecida no artigo 15.º;»

### A (dense, excertos A): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-005_A0012 | 0.7297 | ✔ | 2 — Exceciona-se do disposto no número anterior, as pessoas com deficiência visual quando acompanhados exclusivamente por cães-guia. 3 — A d… |
| 2 | E1-005_A0013 | 0.6934 | ✔ | a) A adoção de modelo de cinzeiro sem aprovação prévia ou em desrespeito pelo modelo aprovado pela Divisão responsável pelo Centro Histórico… |
| 3 | E1-005_A0001 | 0.6433 |  | Edital n.º 589/2021 Sumário: Regulamento Municipal da Limpeza Pública e Higiene Urbana de Guimarães Domingos Bragança Salgado, Presidente da… |
| 4 | E1-005_A0014 | 0.6406 |  | f) Manter nos terrenos ou logradouros dos prédios arbustos, silvados, sebes ou resíduos de qualquer espécie, que possam constituir insalubri… |
| 5 | E1-005_A0004 | 0.6258 |  | d) Despejo e manutenção de recipientes para dejetos de animais; e) Despejo e manutenção de cinzeiros públicos, «ecopontas» e «papachicletes»… |

**Resposta** (gemma4:12b, 2.87 s): O descarte de pontas de cigarros, charutos ou outros cigarros contendo produtos de tabaco em espaço público é proibido [E1-005]. O incumprimento desta proibição constitui uma contraordenação punível com uma coima mínima de 25,00 € e máxima de 250,00 € [E1-005].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (A resposta contém toda a informação essencial da referência e está correta.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas e suportadas pelo excerto E1-005.)

### B (dense, excertos B): Recall@5 0.33, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-005_B0031 | 0.7248 | ✔ | Artigo 15.º Descarte de pontas de cigarros É proibido o descarte em espaço público de pontas de cigarros, charutos ou outros cigarros conten… |
| 2 | E1-005_B0034 | 0.7105 |  | g) A deslocação de quaisquer equipamentos de recolha colocados na via pública; h) Retirar ou remexer nos resíduos contidos nos contentores c… |
| 3 | E1-005_B0011 | 0.6862 |  | d) Lei n.º 88/2019, de 3 de setembro, que aprova as medidas para a redução do impacto das pontas de cigarros, charutos ou outros cigarros no… |
| 4 | E1-005_B0016 | 0.6794 |  | Artigo 10.º Espaços públicos, terrenos do domínio municipal e equipamentos de uso coletivo 1 — Em todos os espaços públicos, nomeadamente ru… |
| 5 | E1-005_B0013 | 0.6416 |  | c) As pontas de cigarros, charutos ou outros cigarros contendo produtos de tabaco. Artigo 7.º Recipientes para deposição indiferenciada dos … |

Quase-acertos: E1-005_B0032 em 9.º, E1-005_B0033 em 10.º

**Resposta** (gemma4:12b, 3.87 s): É proibido o descarte em espaço público de pontas de cigarros, charutos ou outros cigarros contendo produtos de tabaco [E1-005]. É também proibido lançar para o chão qualquer resíduo, nomeadamente beatas de cigarros, em espaços públicos [E1-005]. O regulamento estabelece que a violação das obrigações de limpeza constitui uma contraordenação punível com uma coima mínima de 250 € e máxima de 1500,00 € [E1-005]. No entanto, os excertos não especificam se esta coima se aplica especificamente ao descarte de pontas de cigarro, uma vez que a referida coima está associada ao incumprimento das obrigações de limpeza consagradas nos números 1, 5 e 6 do artigo 13.º, cujo conteúdo não consta nos documentos fornecidos.

**Problemas em código:** pesquisa_parcial, correcao_0, afirmacoes_nao_suportadas, citacoes_1
**Juiz** (gpt-oss-120b): correção 0 (A resposta indica coima mínima 250 € e máxima 1500 €, divergindo da referência que indica 25 € a 250 €.); fidelidade 0.75; citações 1 (A última afirmação tem citação que não a suporta, reduzindo a nota para 1.)
- não suportada: Os excertos não especificam se esta coima se aplica especificamente ao descarte de pontas de cigarro, pois está associada ao incumprimento das obrigações de limpeza dos números 1,5 e 6 do artigo 13.º, cujo conteúdo não consta nos documentos fornecidos.

### C (hybrid, excertos A): Recall@5 0.67, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-005_A0012 | 0.032787 | ✔ | 2 — Exceciona-se do disposto no número anterior, as pessoas com deficiência visual quando acompanhados exclusivamente por cães-guia. 3 — A d… |
| 2 | E1-005_A0001 | 0.031025 |  | Edital n.º 589/2021 Sumário: Regulamento Municipal da Limpeza Pública e Higiene Urbana de Guimarães Domingos Bragança Salgado, Presidente da… |
| 3 | E1-005_A0006 | 0.030415 |  | Artigo 9.º Dever de prevenção e limpeza 1 — Todas as entidades (pessoas coletivas ou singulares) cujas atividades sejam passíveis de sujar a… |
| 4 | E1-005_A0014 | 0.030118 |  | f) Manter nos terrenos ou logradouros dos prédios arbustos, silvados, sebes ou resíduos de qualquer espécie, que possam constituir insalubri… |
| 5 | E1-005_A0004 | 0.029083 |  | d) Despejo e manutenção de recipientes para dejetos de animais; e) Despejo e manutenção de cinzeiros públicos, «ecopontas» e «papachicletes»… |

**Resposta** (gemma4:12b, 3.89 s): É proibido o descarte em espaço público de pontas de cigarros, charutos ou outros cigarros contendo produtos de tabaco [E1-005]. Qualquer violação ao disposto no regulamento constitui contraordenação punível com coima [E1-005]. No entanto, os excertos não especificam o valor exato da coima para o descarte de pontas de cigarro no chão, mencionando apenas uma coima de 25,00 € a 250,00 € para a adoção de modelo de cinzeiro sem aprovação prévia ou em desrespeito pelo modelo aprovado pela Divisão responsável pelo Centro Histórico [E1-005].

**Problemas em código:** pesquisa_parcial, correcao_0, afirmacoes_nao_suportadas, citacoes_1
**Juiz** (gpt-oss-120b): correção 0 (A resposta não indica a coima de 25 € a 250 € para a infração, afirmando que o valor não está especificado, contradizendo a referência.); fidelidade 0.75; citações 1 (Uma das afirmações tem citação que não suporta o conteúdo, por isso a nota é 1.)
- não suportada: Os excertos não especificam o valor exato da coima para o descarte de pontas de cigarro no chão.

## E1-09 (multi_doc): Quando e onde começou o sistema PAYT em Guimarães, e que resultados teve no primeiro ano?

**Referência:** O PAYT entrou em vigor em abril de 2016, no centro histórico da cidade. No primeiro ano, a quantidade de resíduos orgânicos desceu 34% e a de resíduos recicláveis subiu 126%.

- Trecho E1-105 [48973, 49301): «O sistema PAYT de Guimarães entrou em vigor em abril de 2016 no centro histórico da cidade, como resultado do esforço da Câmara Municipal, da empresa Vitrus Ambiente e da RESINORTE, sendo o município responsável pelo pro…»
- Trecho E1-029 [3496, 3659): «As we can see in Figure 2, in the first year of PAYT there was a 34% decrease in the amount of organic waste and a 126% increase in the amount of recyclable waste.»

### A (dense, excertos A): Recall@5 0.5, RR 0.25

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-006_A0007 | 0.8129 |  | 1.3. Enquadramento das Políticas Municipais de Guimarães e Percurso para a Circularidade A jornada intencional do município de Guimarães rum… |
| 2 | E1-001_A0045 | 0.7828 |  | 6.3 EIXOIII – OPERACIONALIZÃO MEDIDA 19 – Reforço do sistema PAYT a todo o território (Ação OB.IV.2.2) Os sistemas PAYT fundamentam-se na ap… |
| 3 | E1-001_A0046 | 0.7647 |  | Em 2023, o sistema PAYT sofreu a sua 4º fase de implementação, aumentando para 55 000, o número de utilizadores. Relativamente aos resultado… |
| 4 | E1-105_A0025 | 0.755 | ✔ | Por outro lado, sendo expectável a redução dos quantitativos de resíduos indiferenciados, não é justificável a manutenção das atuais frequên… |
| 5 | E1-029_A0003 | 0.7451 |  | The PAYT system was implemented in the Historic Center of Guimarães in 2016 and, due to its success, it was expanded to the peripheries in e… |

**Resposta** (gemma4:12b, 3.97 s): O sistema PAYT foi implementado em Guimarães em 2016 [E1-006] [E1-001] [E1-105] [E1-029]. A sua implementação inicial ocorreu no centro histórico da cidade [E1-001] [E1-105] [E1-029]. No primeiro ano de implementação, os resultados mostraram uma produção de resíduos urbanos de 538,48 toneladas de resíduos orgânicos, 68,54 toneladas de papel, 54,30 toneladas de vidro e 147,72 toneladas de plástico/metal [E1-029].

**Problemas em código:** pesquisa_parcial, correcao_0
**Juiz** (gpt-oss-120b): correção 0 (A resposta não indica a data exata (abril de 2016) nem os percentuais de variação (‑34% e +126%), apresentando dados diferentes, logo está incorreta.); fidelidade 1.0; citações 2 (Todas as afirmações têm citações e cada citação suporta a afirmação nos excertos fornecidos.)

### B (dense, excertos B): Recall@5 0.0, RR 0.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_B0115 | 0.848 |  | Importa salientar que o Município de Guimarães foi o primeiro a nível nacional a introduzir o sistema PAYT, e desde a sua implementação foi … |
| 2 | E1-006_B0017 | 0.848 |  | No mesmo ano, foi também publicado o primeiro roteiro para a economia circular, o “G4CE - Guimarães para a Economia Circular”. Em 2016, para… |
| 3 | E1-029_B0006 | 0.7899 |  | The PAYT system was implemented in the Historic Center of Guimarães in 2016 and, due to its success, it was expanded to the peripheries in e… |
| 4 | E1-017_B0017 | 0.788 |  | Desde a implementação, pioneira em Portugal, do sistema Pay-As-You-Throw (PAYT), em 2016, um modelo que beneficia quem mais recicla. Ainda n… |
| 5 | E1-001_B0114 | 0.7866 |  | Os custos suportados pelos utilizadores estão diretamente relacionados à sua efetiva produção de resíduos, promovendo a redução e reciclagem… |

Quase-acertos: E1-105_B0065 em 8.º

**Resposta** (gemma4:12b, 3.14 s): O sistema PAYT foi implementado em Guimarães em 2016 [E1-001] [E1-006] [E1-017]. A implementação inicial ocorreu no Centro Histórico da cidade [E1-006] [E1-001], abrangendo inicialmente 800 utilizadores [E1-006] ou 682 utilizadores [E1-001]. No primeiro ano de implementação, os resultados para o peso total de resíduos urbanos (orgânicos e seletivos) foram de 538,48 toneladas de papel, 68,54 toneladas de plástico/metal, 54,30 toneladas de vidro e 147,72 toneladas de resíduos indiferenciados [E1-029].

**Problemas em código:** pesquisa_sem_acerto, correcao_0, afirmacoes_nao_suportadas, citacoes_1
**Juiz** (gpt-oss-120b): correção 0 (A resposta não menciona a queda de 34% nos orgânicos nem o aumento de 126% nos recicláveis e fornece dados diferentes dos da referência, faltando informação essencial.); fidelidade 0.8; citações 1 (A maioria das afirmações está corretamente citada, mas a última afirmação tem citações que não suportam totalmente a descrição dos tipos de resíduos, resultando numa nota 1.)
- não suportada: No primeiro ano de implementação, os resultados para o peso total de resíduos urbanos (orgânicos e seletivos) foram de 538,48 toneladas de papel, 68,54 toneladas de plástico/metal, 54,30 toneladas de vidro e 147,72 toneladas de resíduos indiferenciados.

### C (hybrid, excertos A): Recall@5 0.0, RR 0.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-006_A0007 | 0.032787 |  | 1.3. Enquadramento das Políticas Municipais de Guimarães e Percurso para a Circularidade A jornada intencional do município de Guimarães rum… |
| 2 | E1-001_A0045 | 0.031754 |  | 6.3 EIXOIII – OPERACIONALIZÃO MEDIDA 19 – Reforço do sistema PAYT a todo o território (Ação OB.IV.2.2) Os sistemas PAYT fundamentam-se na ap… |
| 3 | E1-002_A0030 | 0.030622 |  | Os resultados da Operação, beneficiam de forma direta os resultados da RESINORTE, com impacto em todo o Sistema Multimunicipal e assumindo a… |
| 4 | E1-017_A0006 | 0.029236 |  | Desde 2014, que Guimarães assumiu como propósito o desenvolvimento	sustentável, através da implementação de um ecossistema de governança par… |
| 5 | E1-001_A0046 | 0.02886 |  | Em 2023, o sistema PAYT sofreu a sua 4º fase de implementação, aumentando para 55 000, o número de utilizadores. Relativamente aos resultado… |

Quase-acertos: E1-105_A0025 em 10.º

**Resposta** (gemma4:12b, 4.45 s): O sistema PAYT foi implementado em Guimarães em 2016 [E1-006] [E1-001]. A implementação inicial ocorreu no centro da cidade, abrangendo inicialmente 800 utilizadores [E1-006], sendo que, especificamente na área do Centro histórico de elevada densidade de construção, o sistema serviu 682 utilizadores [E1-001].

Os excertos não fornecem informações sobre os resultados específicos obtidos apenas no primeiro ano de implementação. No entanto, indicam que o sistema teve como objetivo aumentar a recolha seletiva e reduzir a produção de resíduos indiferenciados [E1-006]. Em 2022, o programa reduziu com sucesso os resíduos indiferenciados para 172 kg per capita/ano e aumentou a recolha trifluxo em 115 kg per capita/ano [E1-001].

**Problemas em código:** pesquisa_sem_acerto, correcao_0, afirmacoes_nao_suportadas, citacoes_1
**Juiz** (gpt-oss-120b): correção 0 (A resposta não menciona os resultados do primeiro ano (‑34% orgânicos, +126% recicláveis) e indica que não há informação, divergindo da referência.); fidelidade 0.833; citações 1 (Uma das afirmações não tem citação, por isso a nota é 1.)
- não suportada: Os excertos não fornecem informações sobre os resultados específicos obtidos apenas no primeiro ano de implementação.

## E1-10 (multi_doc): Quando estava previsto começar a funcionar o sistema de depósito e reembolso de embalagens de bebidas, e como é que o consumidor recebe o depósito de volta?

**Referência:** O início do funcionamento estava previsto para 10 de abril de 2026, com um período de transição de 120 dias. O depósito é devolvido quando se entrega a embalagem num ponto de recolha: nos manuais, em dinheiro ou noutras formas, como troca ou vale de compras; nos automáticos, por pagamento eletrónico, donativo ou vale. O reembolso em dinheiro não pode ser recusado nem condicionado.

**Nota sobre a referência:** A referência fica como está (decisão de 15/11), mas inclui os 120 dias de transição, que a pergunta não pede. Isso tira 1 ponto, por igual, a quase todas as respostas que não se abstêm. Com o juiz 120b, nenhuma das respostas à E1-10 tem 2, e só uma em 10 refere os 120 dias (o AMALIA no teste na A).

- Trecho E1-114 [1034, 1403): «A gestão do fluxo de resíduos de embalagens de bebidas é complementada pelo SDR, existindo um período de transição total de 120 dias, a contar da data de entrada em funcionamento operacional do sistema, com início previs…»
- Trecho E1-104 [72775, 73382): «1 - O reembolso do valor de depósito ao consumidor final pode ser realizado por uma das seguintes formas:
a) No caso dos pontos de recolha manuais, em numerário ou através de outras modalidades, designadamente, troca por…»
- Trecho E1-104 [73383, 73461): «2 - A opção pelo reembolso em numerário não pode ser retirada ou condicionada.»

### A (dense, excertos A): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-104_A0040 | 0.754 | ✔ | 3 - O valor de depósito a fixar nos termos do número anterior não está sujeito a tributação, devendo estimular a devolução da embalagem usad… |
| 2 | E1-104_A0031 | 0.7289 |  | 8 - Os resíduos de embalagens retomados através destes equipamentos são contabilizados na recolha seletiva do SGRU. 9 - O disposto no presen… |
| 3 | E1-114_A0001 | 0.7227 | ✔ | Circular n.º 01/2026/DFEMR V1.1 Período de transição – Sistema de Depósito e Reembolso (SDR) Data: 20 de fevereiro de 2026, alterada a 24 de… |
| 4 | E1-104_A0028 | 0.7149 |  | 2 - O sistema de reutilização de embalagens de produtos destinados ao consumidor envolve necessariamente a cobrança, no ato da compra, de um… |
| 5 | E1-104_A0030 | 0.7038 |  | 16 - Em linha com as melhores práticas a nível internacional e no sentido de melhorar o desempenho ambiental dos sistemas de reutilização de… |

**Resposta** (gemma4:12b, 6.06 s): O início previsto para a entrada em funcionamento operacional do Sistema de Depósito e Reembolso (SDR) é 10 de abril de 2026 [E1-114]. O reembolso do valor de depósito ao consumidor final pode ser realizado de diferentes formas, dependendo do tipo de ponto de recolha [E1-104]:

Nos pontos de recolha manuais, o reembolso pode ser feito em numerário ou através de outras modalidades, como troca por troca ou vale de compras no exato valor do depósito [E1-104]. Nos pontos de recolha automática, o reembolso ocorre através de formas de pagamento desmaterializadas, donativos ou mediante a emissão de um vale comprovativo do retorno, que pode ser redimido em numerário, vale de compras ou atividades e serviços que correspondam ao exato valor do depósito [E1-104]. A opção pelo reembolso em numerário não pode ser retirada ou condicionada [E1-104].

**Problemas em código:** correcao_1
**Juiz** (gpt-oss-120b): correção 1 (A resposta inclui a data de início e as formas de reembolso corretas, mas omite o período de transição de 120 dias mencionado na referência.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas de citações que correspondem aos excertos que as suportam.)

### B (dense, excertos B): Recall@5 0.0, RR 0.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-104_B0104 | 0.7401 |  | Artigo 30.º-A Sistema de depósito e reembolso 1 - A gestão do fluxo de resíduos de embalagens de bebidas é complementada pelo sistema de dep… |
| 2 | E1-104_B0076 | 0.7326 |  | Artigo 23.º Sistemas de gestão de embalagens reutilizáveis 1 - Os embaladores que utilizam embalagens reutilizáveis devem estabelecer sistem… |
| 3 | E1-104_B0109 | 0.7298 |  | 5 - Os resultados da reciclagem das embalagens recolhidas nos termos do presente artigo concorrem para o cumprimento dos objetivos de valori… |
| 4 | E1-104_B0110 | 0.7266 |  | 3 - O valor de depósito a fixar nos termos do número anterior não está sujeito a tributação, devendo estimular a devolução da embalagem usad… |
| 5 | E1-114_B0001 | 0.7253 |  | Circular n.º 01/2026/DFEMR V1.1 Período de transição – Sistema de Depósito e Reembolso (SDR) Data: 20 de fevereiro de 2026, alterada a 24 de… |

**Resposta** (gemma4:12b, 1.45 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** pesquisa_sem_acerto, abstencao_sem_trecho_nos_excertos, correcao_0, afirmacoes_nao_suportadas, citacoes_0, juiz_abstencao_com_resposta_nos_excertos
**Juiz** (gpt-oss-120b): correção 0 (A resposta do sistema não fornece nenhuma das informações da referência, falhando totalmente em responder à pergunta.); fidelidade 0.0; citações 0 (A resposta não apresenta citações e a afirmação não é suportada pelos excertos.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

### C (hybrid, excertos A): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-104_A0040 | 0.032787 | ✔ | 3 - O valor de depósito a fixar nos termos do número anterior não está sujeito a tributação, devendo estimular a devolução da embalagem usad… |
| 2 | E1-114_A0001 | 0.031746 | ✔ | Circular n.º 01/2026/DFEMR V1.1 Período de transição – Sistema de Depósito e Reembolso (SDR) Data: 20 de fevereiro de 2026, alterada a 24 de… |
| 3 | E1-104_A0031 | 0.031514 |  | 8 - Os resíduos de embalagens retomados através destes equipamentos são contabilizados na recolha seletiva do SGRU. 9 - O disposto no presen… |
| 4 | E1-104_A0028 | 0.03125 |  | 2 - O sistema de reutilização de embalagens de produtos destinados ao consumidor envolve necessariamente a cobrança, no ato da compra, de um… |
| 5 | E1-104_A0038 | 0.030622 |  | 3 - O SDR é gerido autonomamente do sistema integrado de gestão de resíduos de embalagens (SIGRE), bem como de sistemas individuais de embal… |

**Resposta** (gemma4:12b, 4.28 s): O início previsto para a entrada em funcionamento operacional do sistema de depósito e reembolso (SDR) é 10 de abril de 2026 [E1-114]. O reembolso do valor de depósito ao consumidor final pode ser realizado de diferentes formas, dependendo do tipo de ponto de recolha [E1-104]:

*   **Pontos de recolha manuais:** o reembolso pode ser feito em numerário ou através de outras modalidades, como troca por troca ou vale de compras no exato valor do depósito [E1-104].
*   **Pontos de recolha automática:** o reembolso ocorre através de formas de pagamento desmaterializadas, donativos ou mediante a emissão de um vale comprovativo do retorno, que pode ser redimido em numerário, vale de compras, ou atividades e serviços que correspondam ao exato valor do depósito [E1-104].

A opção pelo reembolso em numerário não pode ser retirada ou condicionada [E1-104].

**Problemas em código:** correcao_1
**Juiz** (gpt-oss-120b): correção 1 (Falta mencionar o período de transição de 120 dias, embora o resto esteja correto.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas e as citações suportam as informações.)

## E1-11 (multi_doc): O que é a TGR que aparece no tarifário de resíduos de Guimarães, e quanto paga por dia um utilizador doméstico em 2026?

**Referência:** É a taxa de gestão de resíduos, criada para compensar os custos administrativos de acompanhamento da gestão de resíduos, incentivar a redução dos resíduos e o cumprimento das metas nacionais. É repercutida nas tarifas até ao produtor dos resíduos. Em 2026, um utilizador doméstico de Guimarães paga 0,0633 € por dia de TGR.

- Trecho E1-007 [272, 328): «(€/m3)ii
TGR (€/dia)
Doméstico (UD)	0,1600	0,2600	0,0633»
- Trecho E1-103 [84949, 85238): «1 - É estabelecida uma TGR, que visa compensar os custos administrativos de acompanhamento das atividades de gestão de resíduos, incentivar a redução da produção de resíduos, estimular o cumprimento dos objetivos naciona…»
- Trecho E1-103 [85542, 85778): «3 - A TGR deve ser repercutida nas tarifas e prestações financeiras cobradas pelos sujeitos passivos e ao longo da cadeia de valor da gestão de resíduos até ao produtor dos resíduos, sem prejuízo do estabelecido no n.º 5…»

### A (dense, excertos A): Recall@5 1.0, RR 0.5

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-001_A0052 | 0.7771 |  | Contudo, estes apoios não serão suficientes face à escala dos desafios e investimentos necessários ou face ao potencial acréscimo na tarifa … |
| 2 | E1-007_A0001 | 0.7478 | ✔ | Departamento de Ambiente e Sustentabilidade \| Divisão de Ambiente e Espaço Público	Mod. 238-B/SQ 1 TARIFÁRIO GESTÃO DE RESÍDUOS PARA O ANO D… |
| 3 | E1-103_A0046 | 0.7458 | ✔ | Capítulo III Tarifas de gestão de resíduos Artigo 110.º Taxa de gestão de resíduos 1 - É estabelecida uma TGR, que visa compensar os custos … |
| 4 | E1-001_A0028 | 0.7372 |  | PAYT para 0,026€/L, como forma de desincentivar a sua deposição. Relativamente à aplicação do sistema SAYR, o novo sistema tarifário será re… |
| 5 | E1-001_A0027 | 0.6999 |  | 72/2010, de 4 de fevereiro. Nos locais com implementação do sistema PAYT, é realizada a distinção entre métodos de quantificação, nomeadamen… |

**Resposta** (gemma4:12b, 4.24 s): A Taxa de Gestão de Resíduos (TGR) é um valor que visa compensar os custos administrativos de acompanhamento das atividades de gestão de resíduos, incentivar a redução da produção de resíduos, estimular o cumprimento dos objetivos nacionais em matéria de gestão de resíduos e melhorar o desempenho do setor [E1-103]. A TGR deve ser repercutida nas tarifas e prestações financeiras cobradas pelos sujeitos passivos ao longo da cadeia de valor da gestão de resíduos [E1-103].

No tarifário de 2026, o valor da TGR para um utilizador doméstico (UD) é de 0,0633 €/dia [E1-007]. Este valor aplica-se tanto a utilizadores com abastecimento de água como a utilizadores sem abastecimento de água, incluindo as categorias de UD – Social e UD – Emigrante [E1-007].

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (A resposta contém toda a informação essencial da referência e não apresenta erros.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas de citações que correspondem aos excertos que as suportam.)

### B (dense, excertos B): Recall@5 1.0, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-007_B0001 | 0.7605 | ✔ | Departamento de Ambiente e Sustentabilidade \| Divisão de Ambiente e Espaço Público	Mod. 238-B/SQ 1 TARIFÁRIO GESTÃO DE RESÍDUOS PARA O ANO D… |
| 2 | E1-001_B0133 | 0.7556 |  | Foi considerado o valor da TGR de 35 €/t para a fração indiferenciada. Considerando os valores comunicados pelo município de Guimarães à ERS… |
| 3 | E1-103_B0124 | 0.7426 | ✔ | 3 - A TGR deve ser repercutida nas tarifas e prestações financeiras cobradas pelos sujeitos passivos e ao longo da cadeia de valor da gestão… |
| 4 | E1-103_B0123 | 0.7254 | ✔ | Capítulo III Tarifas de gestão de resíduos Artigo 110.º Taxa de gestão de resíduos 1 - É estabelecida uma TGR, que visa compensar os custos … |
| 5 | E1-001_B0131 | 0.7205 |  | Contudo, estes apoios não serão suficientes face à escala dos desafios e investimentos necessários ou face ao potencial acréscimo na tarifa … |

**Resposta** (gemma4:12b, 2.93 s): A Taxa de Gestão de Resíduos (TGR) é estabelecida para compensar os custos administrativos de acompanhamento das atividades de gestão de resíduos, incentivar a redução da produção de resíduos, estimular o cumprimento dos objetivos nacionais em matéria de gestão de resíduos e melhorar o desempenho do setor [E1-103]. No tarifário de gestão de resíduos para o ano de 2026, um utilizador doméstico (UD) com abastecimento de água paga uma tarifa de disponibilidade de 0,1600 €/dia e uma TGR de 0,0633 €/dia [E1-007]. Para utilizadores domésticos sem abastecimento de água, o documento não indica o valor da tarifa de disponibilidade nem da TGR [E1-007].

**Problemas em código:** afirmacoes_nao_suportadas, citacoes_1
**Juiz** (gpt-oss-120b): correção 2 (A resposta contém a definição correta da TGR e indica o valor de 0,0633 €/dia para o utilizador doméstico, sem erros.); fidelidade 0.667; citações 1 (Uma das citações não suporta a afirmação correspondente.)
- não suportada: Para utilizadores domésticos sem abastecimento de água, o documento não indica o valor da tarifa de disponibilidade nem da TGR.

### C (hybrid, excertos A): Recall@5 0.33, RR 1.0

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-007_A0001 | 0.032522 | ✔ | Departamento de Ambiente e Sustentabilidade \| Divisão de Ambiente e Espaço Público	Mod. 238-B/SQ 1 TARIFÁRIO GESTÃO DE RESÍDUOS PARA O ANO D… |
| 2 | E1-001_A0052 | 0.032018 |  | Contudo, estes apoios não serão suficientes face à escala dos desafios e investimentos necessários ou face ao potencial acréscimo na tarifa … |
| 3 | E1-001_A0027 | 0.031514 |  | 72/2010, de 4 de fevereiro. Nos locais com implementação do sistema PAYT, é realizada a distinção entre métodos de quantificação, nomeadamen… |
| 4 | E1-015_A0001 | 0.030077 |  | PAYT: Pague pelo resíduo que produz. Reciclar para poupar! Centro da cidade. Tarifário Payt Método B Assim no método B (pré-definido), o cál… |
| 5 | E1-001_A0026 | 0.02967 |  | ▪ Projeto “Aqualastic: Educar, Reduzir e Valorizar” - surgiu de uma candidatura aprovada ao Fundo Ambiental do Ministério do Ambiente e da A… |

**Resposta** (gemma4:12b, 3.99 s): A TGR corresponde à Taxa de Gestão de Resíduos, representando o encargo suportado pelo Município relativo a este valor [E1-001]. No tarifário para o ano de 2026, em locais sem sistema PAYT, um utilizador doméstico (UD) com abastecimento de água paga 0,0633 €/dia de TGR [E1-007]. Para um utilizador doméstico (UD) em locais sem abastecimento de água, o valor da TGR é igualmente de 0,0633 €/dia [E1-007]. Nos locais com sistema PAYT (Método A), o valor da TGR para um utilizador doméstico (UD) é de 0,0633 €/dia [E1-007].

**Problemas em código:** pesquisa_parcial, correcao_1
**Juiz** (gpt-oss-120b): correção 1 (Define TGR corretamente e indica o valor correto, mas omite a explicação sobre os objetivos da taxa.); fidelidade 1.0; citações 2 (Todas as afirmações têm citações e cada citação corresponde a um excerto que as suporta.)

## E1-12 (multi_doc): Que meta tem Guimarães para a quantidade total de resíduos produzidos por habitante até 2030, e quanto foi essa produção em Portugal continental em 2025?

**Referência:** Guimarães compromete-se a reduzir a produção total de resíduos para 362 kg por habitante e por ano até 2030, menos 15% do que em 2019. Em 2025, Portugal continental produziu 494 kg por habitante, abaixo da média europeia de 517 kg.

- Trecho E1-003 [39227, 39319): «O Município de Guimarães compromete-se, até ao ano 2030, a criar condições que lhe permitam:»
- Trecho E1-003 [39689, 39860): «5. Reduzir a quantidade total de resíduos produzidos para 362 kg per capita por ano, (reduzir em 15% a quantidade de RU produzidos por habitante face aos valores de 2019).»
- Trecho E1-101 [22042, 22310): «Relativamente à produção por habitante, em Portugal Continental, o valor foi de 494 kg/hab.ano5, abaixo da média Europeia de 517 kg/hab.ano6, correspondente a uma produção de 1,35 kg/hab.dia, valor esse que sofreu uma pe…»

### A (dense, excertos A): Recall@5 0.67, RR 0.25

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-006_A0026 | 0.7919 |  | A seguir à indústria têxtil, a quarta indústria mais prevalente em Guimarães é a metalomecânica, ligada à construção e à produção de cutelar… |
| 2 | E1-101_A0038 | 0.7514 |  | 19 Onde se inclui a produção e encaminhamento de CDR. 20 Inclui as escórias inertes e inqueimados, resultantes de VE, não valorizadas. 21 Pa… |
| 3 | E1-001_A0049 | 0.7503 |  | RU	ton 71175 70665 71175 71175 71175 71089 69049 64378 60426 Capitação Produção de RU Kg/hab 454	451	454	454	454	453	440	410	385 6.1.2. Reco… |
| 4 | E1-003_A0022 | 0.7446 | ✔ | • Um representante da Associação Laboratório da Paisagem; • Um representante da empresa Municipal Vitrus Ambiente; • Um representante da ZER… |
| 5 | E1-001_A0048 | 0.7381 |  | Direcionar campanhas de sensibilização para pequenos e grandes produtores de modo a conseguir uma correta gestão de resíduos. Os impactes ex… |

Quase-acertos: E1-101_A0012 em 7.º

**Resposta** (gemma4:12b, 3.35 s): O município de Guimarães tem como meta reduzir a quantidade total de resíduos produzidos para 362 kg por habitante por ano até ao ano 2030 [E1-003]. Esta meta representa uma redução de 15% na quantidade de resíduos urbanos produzidos por habitante face aos valores de 2019 [E1-003]. Em Portugal Continental, o resultado obtido para a produção de resíduos per capita em 2025 foi de 494 kg/hab.ano [E1-101].

**Problemas em código:** pesquisa_parcial
**Juiz** (gpt-oss-120b): correção 2 (A resposta contém toda a informação essencial da referência e não tem erros.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas de citações que correspondem aos excertos que as suportam.)

### B (dense, excertos B): Recall@5 0.67, RR 0.2

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-006_B0066 | 0.7988 |  | Em termos de geração total de resíduos sólidos urbanos, a gestão de resíduos do município de Guimarães está abaixo da média nacional e europ… |
| 2 | E1-001_B0123 | 0.7922 |  | A redução da produção de RU no município de Guimarães em 2030 será de 15% do total RU produzidos no ano de referência (2022). Importa salien… |
| 3 | E1-101_B0102 | 0.7854 |  | Na Tabela 8 apresenta-se o resultado obtido para Portugal Continental em 2025. Tabela 8 – Posicionamento de Portugal Continental face à prev… |
| 4 | E1-006_B0074 | 0.7796 |  | Em 2023, foram produzidos 449 kg de resíduos urbanos (RU) por ano per capita, de um total de 70 655 toneladas de RU. Desses 449 kg per capit… |
| 5 | E1-003_B0056 | 0.7762 | ✔ | 4. COMISSÃO DE ACOMPANHAMENTO DA EXECUÇÃO DO COMPROMISSO O Município de Guimarães compromete-se, até ao ano 2030, a criar condições que lhe … |

**Resposta** (gemma4:12b, 2.21 s): O município de Guimarães compromete-se a reduzir a quantidade total de resíduos produzidos para 362 kg por capita por ano até ao ano 2030 [E1-003]. Em 2025, a produção de resíduos per capita em Portugal Continental foi de 494 kg/hab.ano [E1-101].

**Problemas em código:** pesquisa_parcial
**Juiz** (gpt-oss-120b): correção 2 (A resposta contém exatamente a meta de 362 kg/hab/ano até 2030 e o valor de 494 kg/hab em 2025, sem erros.); fidelidade 1.0; citações 2 (Todas as afirmações têm citação e os excertos citados suportam-nas.)

### C (hybrid, excertos A): Recall@5 0.33, RR 0.25

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-101_A0038 | 0.032002 |  | 19 Onde se inclui a produção e encaminhamento de CDR. 20 Inclui as escórias inertes e inqueimados, resultantes de VE, não valorizadas. 21 Pa… |
| 2 | E1-101_A0042 | 0.030415 |  | RU depositados em aterro (%) RU depositados em aterro (t) Resultado obtido 2025	52	2 963 006 Meta 2035	10	528 13826 Relembrar que, no presen… |
| 3 | E1-102_A0038 | 0.03009 |  | De referir que, para o cálculo das metas, e pese embora se encontrem disponíveis dados referentes a 2020 (ano de fecho do PERSU 2020 e de cu… |
| 4 | E1-101_A0012 | 0.029851 | ✔ | Variação face ao ano anterior	↑1%	↑0,24%	↑0,28%	↑3,97%	↑2,07%	↑1,54% * Valor médio tendo por base as capitações por SGRU de PT Continental e… |
| 5 | E1-101_A0006 | 0.029214 |  | Do desempenho do setor de resíduos urbanos, a nível nacional, resultou, em 2025, uma taxa de preparação para reutilização e reciclagem de 39… |

Quase-acertos: E1-003_A0022 em 6.º

**Resposta** (gemma4:12b, 2.3 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** pesquisa_parcial, abstencao_com_trecho_nos_excertos, correcao_0, juiz_abstencao_com_resposta_nos_excertos
**Juiz** (gpt-oss-120b): correção 0 (A resposta não fornece a meta de 362 kg/habitante/ano nem o valor de 494 kg/habitante para 2025, contradizendo a referência.); fidelidade None; citações None (Não há afirmações a citar; portanto a pontuação de citações é 2 por vacuidade.)

## E1-13 (unanswerable): A que horas abre o ecocentro de Aldão ao sábado?

**Referência:** A base de conhecimento não contém informação sobre o horário dos ecocentros de Guimarães.


### A (dense, excertos A): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-016_A0001 | 0.4607 |  | Largo Dr. João Mota Prego Largo João Franco Rua Dr. António Mota Prego Largo do Serralho Rua Rainha D. Maria II Viela São Crispim Rua Dr. Av… |
| 2 | E1-004_A0015 | 0.4605 |  | Artigo 14.º Atendimento ao público 1 — O Município de Guimarães dispõe, de Balcão Único de Atendimento, de um serviço de atendimento telefón… |
| 3 | E1-001_A0011 | 0.4585 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 4 | E1-003_A0010 | 0.4557 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |
| 5 | E1-105_A0019 | 0.4266 |  | 3.8.3. Utilização de ecocentros Apesar de a utilização de ecocentros ser consentânea com a existência de um sistema PAYT, estas infraestrutu… |

**Resposta** (gemma4:12b, 2.08 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** afirmacoes_nao_suportadas, citacoes_0
**Juiz** (gpt-oss-120b): correção 2 (A resposta indica claramente que a informação não está nas fontes.); fidelidade 0.0; citações 0 (A única afirmação não tem citações e não é suportada por nenhum excerto.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

### B (dense, excertos B): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-003_B0027 | 0.5239 |  | Resíduos recolhidos em Ecocentros Os habitantes do Município de Guimarães usam 2 Ecocentros (Aldão e Ponte) para entregas de resíduos não re… |
| 2 | E1-001_B0026 | 0.5219 |  | Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) Papel e embalagens de cartão 2 vezes por semana (ci… |
| 3 | E1-016_B0002 | 0.4956 |  | Rua Alfredo Guimarães Rua Arrochela Rua Val de Donas Ruas Horários de Recolha Recolha PAYT Centro Histórico Número Verde 800 209 565 9h30 9h… |
| 4 | E1-002_B0111 | 0.4742 |  | Assim, está prevista a criação desta minicentral junto ao ecocentro de Aldão, com um investimento inicial de 200.000,00€ e com um custo de o… |
| 5 | E1-004_B0037 | 0.4714 |  | j) Contactos e horários de atendimento. Artigo 14.º Atendimento ao público 1 — O Município de Guimarães dispõe, de Balcão Único de Atendimen… |

**Resposta** (gemma4:12b, 1.55 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** afirmacoes_nao_suportadas, citacoes_0
**Juiz** (gpt-oss-120b): correção 2 (A resposta indica claramente que a informação não está nas fontes.); fidelidade 0.0; citações 0 (A resposta não inclui quaisquer citações, pelo que a nota de citações é 0.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

### C (hybrid, excertos A): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-016_A0001 | 0.032787 |  | Largo Dr. João Mota Prego Largo João Franco Rua Dr. António Mota Prego Largo do Serralho Rua Rainha D. Maria II Viela São Crispim Rua Dr. Av… |
| 2 | E1-001_A0011 | 0.031025 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 3 | E1-003_A0010 | 0.03101 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |
| 4 | E1-004_A0022 | 0.029857 |  | 2 — A recolha processa-se nos seguintes horários: a) No período da noite entre as 23.00 horas e as 04.45h; b) No período da manhã entre as 0… |
| 5 | E1-004_A0015 | 0.029116 |  | Artigo 14.º Atendimento ao público 1 — O Município de Guimarães dispõe, de Balcão Único de Atendimento, de um serviço de atendimento telefón… |

**Resposta** (gemma4:12b, 2.3 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** nenhum
**Juiz** (gpt-oss-120b): correção 2 (A resposta indica claramente que a informação não está nas fontes.); fidelidade None; citações None (Não há afirmações factuais a citar; portanto as citações são irrelevantes e a nota é 2.)

## E1-14 (unanswerable): Quanto é o depósito cobrado por cada garrafa ou lata no sistema de depósito e reembolso?

**Referência:** A base de conhecimento não contém informação sobre o valor do depósito do sistema de depósito e reembolso.


### A (dense, excertos A): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-104_A0040 | 0.7592 |  | 3 - O valor de depósito a fixar nos termos do número anterior não está sujeito a tributação, devendo estimular a devolução da embalagem usad… |
| 2 | E1-104_A0028 | 0.6932 |  | 2 - O sistema de reutilização de embalagens de produtos destinados ao consumidor envolve necessariamente a cobrança, no ato da compra, de um… |
| 3 | E1-104_A0044 | 0.6822 |  | 1 - Os estabelecimentos do setor HORECA devem assegurar a armazenagem preliminar das embalagens de bebidas adquiridas e consumidas no seu es… |
| 4 | E1-104_A0039 | 0.6811 |  | Artigo 30.º-D Metas de gestão 1 - Os embaladores responsáveis pela colocação no mercado de embalagens abrangidas pelo SDR devem assegurar, a… |
| 5 | E1-104_A0031 | 0.6686 |  | 8 - Os resíduos de embalagens retomados através destes equipamentos são contabilizados na recolha seletiva do SGRU. 9 - O disposto no presen… |

**Resposta** (gemma4:12b, 3.49 s): O valor de depósito é determinado por despacho dos membros do Governo responsáveis pelas áreas da economia e do ambiente [E1-104] [E1-104]. Este valor não está sujeito a tributação e deve estimular a devolução da embalagem usada [E1-104] [E1-104]. O montante é cobrado ao consumidor final no ato da venda de bebidas, independentemente da técnica de venda utilizada, incluindo por via eletrónica ou à distância, com exceção dos casos previstos para os estabelecimentos do setor HORECA [E1-104].

**Problemas em código:** respondeu_sem_resposta_na_base, correcao_0
**Juiz** (gpt-oss-120b): correção 0 (A resposta não indica que a informação falta, apenas dá uma descrição genérica, portanto não cumpre o critério de dizer claramente que não está nas fontes.); fidelidade 1.0; citações 2 (Todas as afirmações são acompanhadas de citações que as suportam.)

### B (dense, excertos B): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-104_B0109 | 0.7531 |  | 5 - Os resultados da reciclagem das embalagens recolhidas nos termos do presente artigo concorrem para o cumprimento dos objetivos de valori… |
| 2 | E1-104_B0110 | 0.7485 |  | 3 - O valor de depósito a fixar nos termos do número anterior não está sujeito a tributação, devendo estimular a devolução da embalagem usad… |
| 3 | E1-104_B0104 | 0.7188 |  | Artigo 30.º-A Sistema de depósito e reembolso 1 - A gestão do fluxo de resíduos de embalagens de bebidas é complementada pelo sistema de dep… |
| 4 | E1-104_B0076 | 0.7001 |  | Artigo 23.º Sistemas de gestão de embalagens reutilizáveis 1 - Os embaladores que utilizam embalagens reutilizáveis devem estabelecer sistem… |
| 5 | E1-104_B0105 | 0.6994 |  | Artigo 30.º-B Âmbito objetivo 1 - Estão abrangidas pelo âmbito de aplicação do SDR as embalagens primárias não reutilizáveis de bebidas em p… |

**Resposta** (gemma4:12b, 2.83 s): O valor de depósito é determinado por despacho dos membros do Governo responsáveis pelas áreas da economia e do ambiente [E1-104]. Este valor pode ser revisto por iniciativa do Governo ou sob proposta das entidades gestoras do SDR, especialmente quando não for assegurado o cumprimento da meta de recolha [E1-104]. O valor de depósito não está sujeito a tributação e deve estimular a devolução da embalagem usada [E1-104]. Não encontrei informação suficiente nas fontes disponíveis para indicar o valor exato cobrado por cada garrafa ou lata.

**Problemas em código:** respondeu_sem_resposta_na_base, afirmacoes_nao_suportadas, citacoes_1
**Juiz** (gpt-oss-120b): correção 2 (A resposta indica claramente que não há informação suficiente para indicar o valor exato, alinhando‑se com a referência que afirma a ausência de dados.); fidelidade 0.75; citações 1 (A última afirmação não tem citação e não é suportada pelos excertos; as demais têm citação correta.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para indicar o valor exato cobrado por cada garrafa ou lata.

### C (hybrid, excertos A): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-104_A0040 | 0.032787 |  | 3 - O valor de depósito a fixar nos termos do número anterior não está sujeito a tributação, devendo estimular a devolução da embalagem usad… |
| 2 | E1-104_A0028 | 0.032002 |  | 2 - O sistema de reutilização de embalagens de produtos destinados ao consumidor envolve necessariamente a cobrança, no ato da compra, de um… |
| 3 | E1-104_A0039 | 0.03125 |  | Artigo 30.º-D Metas de gestão 1 - Os embaladores responsáveis pela colocação no mercado de embalagens abrangidas pelo SDR devem assegurar, a… |
| 4 | E1-114_A0001 | 0.030835 |  | Circular n.º 01/2026/DFEMR V1.1 Período de transição – Sistema de Depósito e Reembolso (SDR) Data: 20 de fevereiro de 2026, alterada a 24 de… |
| 5 | E1-104_A0038 | 0.030536 |  | 3 - O SDR é gerido autonomamente do sistema integrado de gestão de resíduos de embalagens (SIGRE), bem como de sistemas individuais de embal… |

**Resposta** (gemma4:12b, 3.46 s): O valor de depósito é determinado por despacho dos membros do Governo responsáveis pelas áreas da economia e do ambiente [E1-104]. Este valor pode ser revisto por iniciativa do Governo ou sob proposta das entidades gestoras do SDR, especialmente quando não for assegurado o cumprimento da meta de recolha [E1-104]. O valor de depósito não está sujeito a tributação e deve servir para estimular a devolução da embalagem usada [E1-104].

**Problemas em código:** respondeu_sem_resposta_na_base, correcao_0
**Juiz** (gpt-oss-120b): correção 0 (A resposta não afirma que a informação não está nas fontes e tenta dar explicação, não cumprindo o critério de indicar a ausência de dados.); fidelidade 1.0; citações 2 (Todas as afirmações são citadas e as citações suportam as afirmações.)

## E1-15 (unanswerable): Quantos ecopontos existem no concelho de Guimarães?

**Referência:** A base de conhecimento não contém informação sobre o número de ecopontos em Guimarães.


### A (dense, excertos A): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-003_A0010 | 0.7202 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |
| 2 | E1-001_A0011 | 0.7188 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 3 | E1-001_A0008 | 0.6807 |  | São Tiago e Mascotelos, Polvoreira, Pinheiro, e parcelas residuais de Atães e Rendufe, Aldão e Ponte fazem parte desse grupo. A cidade esten… |
| 4 | E1-003_A0009 | 0.6715 |  | 2. ENQUADRAMENTO DA GESTÃO DE RESÍDUOS NO MUNICÍPIO Tipo de resíduos	Frequência de recolha de resíduos Resíduos indiferenciados	Diariamente … |
| 5 | E1-006_A0026 | 0.6712 |  | A seguir à indústria têxtil, a quarta indústria mais prevalente em Guimarães é a metalomecânica, ligada à construção e à produção de cutelar… |

**Resposta** (gemma4:12b, 2.03 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** afirmacoes_nao_suportadas, citacoes_0
**Juiz** (gpt-oss-120b): correção 2 (A resposta indica claramente que a informação não está disponível nas fontes.); fidelidade 0.0; citações 0 (Falta citação para a afirmação feita, por isso a nota é 1.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

### B (dense, excertos B): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-018_B0023 | 0.7359 |  | According to the 2021 Census, Guimarães has 156,849 inhabitants distributed over 241 km2 [30]. In terms of administrative organisation, the … |
| 2 | E1-003_B0027 | 0.7299 |  | Resíduos recolhidos em Ecocentros Os habitantes do Município de Guimarães usam 2 Ecocentros (Aldão e Ponte) para entregas de resíduos não re… |
| 3 | E1-001_B0026 | 0.6936 |  | Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) Papel e embalagens de cartão 2 vezes por semana (ci… |
| 4 | E1-001_B0014 | 0.6762 |  | 3 Descrição da entidade gestora do sistema municipal O Município de Guimarães é a Entidade Titular do seu sistema municipal e multimunicipal… |
| 5 | E1-003_B0024 | 0.6631 |  | Em relação a este aspeto, evidencia-se o mapa dos resíduos de Guimarães , elaborado em 2016, que procurou caraterizar os hábitos dos cidadão… |

**Resposta** (gemma4:12b, 1.37 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** afirmacoes_nao_suportadas, citacoes_0
**Juiz** (gpt-oss-120b): correção 2 (A resposta indica claramente que a informação não está disponível nas fontes.); fidelidade 0.0; citações 0 (A afirmação não tem citações e nenhuma delas suporta a declaração.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

### C (hybrid, excertos A): Recall@5 —, RR —

| # | Excerto | Pontuação | Acerta | Início do texto |
|---|---|---|---|---|
| 1 | E1-003_A0010 | 0.031545 |  | Resíduos recolhidos porta-a-porta O sistema de recolha mais representativo no Município de Guimarães, é o porta-a-porta através de saco perd… |
| 2 | E1-003_A0011 | 0.031319 |  | 2.2 RECUPERAÇÃO DE RESÍDUOS RECOLHIDOS SEPARADOS a) Por favor, especifique quem recolhe os resíduos indiferenciados. Porta-a-porta com conte… |
| 3 | E1-001_A0012 | 0.031025 |  | Porta-a-porta vidro	VITRUS	PAYT Porta-a-porta papel/cartão	VITRUS	PAYT RESINORTE-Urgezes Porta-a-porta embalagens plásticas e metálicas VITR… |
| 4 | E1-001_A0011 | 0.029287 |  | Tipo de resíduos	Frequência de recolha de resíduos Embalagens mistas	2 vezes por semana (cidade e vilas), 1 por semana (outras localidades) … |
| 5 | E1-020_A0001 | 0.028446 |  | Desde 2016, Guimarães tem em curso um plano estratégico para a Economia Circular (G4CE – Guimarães para a Economia Circular). Neste plano es… |

**Resposta** (gemma4:12b, 2.2 s): Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

**Problemas em código:** afirmacoes_nao_suportadas, citacoes_0
**Juiz** (gpt-oss-120b): correção 2 (A resposta indica claramente que a informação não está disponível nas fontes.); fidelidade 0.0; citações 0 (A resposta não apresenta citações e, portanto, não cumpre o requisito de citar os excertos.)
- não suportada: Não encontrei informação suficiente nas fontes disponíveis para responder a esta pergunta.

## Contagem dos problemas

| Experiência | Problema | Respostas |
|---|---|---|
| A | abstencao_sem_trecho_nos_excertos | 1 |
| A | afirmacoes_nao_suportadas | 4 |
| A | citacoes_0 | 3 |
| A | citacoes_1 | 1 |
| A | correcao_0 | 3 |
| A | correcao_1 | 4 |
| A | juiz_abstencao_com_resposta_nos_excertos | 2 |
| A | pesquisa_parcial | 4 |
| A | pesquisa_sem_acerto | 2 |
| A | respondeu_sem_resposta_na_base | 1 |
| B | abstencao_sem_trecho_nos_excertos | 2 |
| B | afirmacoes_nao_suportadas | 9 |
| B | citacoes_0 | 4 |
| B | citacoes_1 | 5 |
| B | correcao_0 | 4 |
| B | correcao_1 | 2 |
| B | juiz_abstencao_com_resposta_nos_excertos | 2 |
| B | pesquisa_parcial | 3 |
| B | pesquisa_sem_acerto | 3 |
| B | respondeu_sem_resposta_na_base | 1 |
| C | abstencao_com_trecho_nos_excertos | 1 |
| C | abstencao_sem_trecho_nos_excertos | 1 |
| C | afirmacoes_nao_suportadas | 3 |
| C | citacoes_0 | 1 |
| C | citacoes_1 | 2 |
| C | correcao_0 | 7 |
| C | correcao_1 | 3 |
| C | juiz_abstencao_com_resposta_nos_excertos | 2 |
| C | pesquisa_parcial | 5 |
| C | pesquisa_sem_acerto | 3 |
| C | respondeu_sem_resposta_na_base | 1 |
