# Banco de repertório sociocultural

Repertório **legítimo e produtivo** (C2): referência externa real, citável e
**articulada ao argumento** — não citação decorativa. Organizado pelas 8
categorias de tema (ver `temas/lista_temas.md`).

**Uso pelo corretor:**
1. **Verificar autenticidade** — repertório que o aluno citou é real? Conferir no
   corpus: `python3 scripts/amostra.py --busca "<termo>" --faixa 800-1000 --n 1`.
   Se nem no corpus nem no conhecimento geral existe → provável invenção → não
   conta como produtivo (e, na prática 2025, penaliza 2 competências — ver
   `regras_por_ano.md`).
2. **Classificar produtividade** — a referência é diretamente pertinente,
   explica uma etapa causal e continua necessária depois que o nome do autor é
   retirado? Se for verdadeira, mas transferível ou ligada só por analogia,
   marcar `fronteira_repertorio_bolso`.
3. **Sugerir** — oferecer repertório pertinente ao tema do aluno.

`(corpus: N≥900)` = nº de redações nota ≥900 no `corpus.db` que citam o termo.
É sinal de ocorrência em textos fortes pré-2025, **não prova de produtividade no
texto atual**. Termos sem marca são curados.

## Regra 2025 — repertório de bolso

Aplicar quatro testes separados:

| Teste | Pergunta |
| --- | --- |
| Legitimidade | A fonte e o conceito existem? |
| Pertinência | A referência trata diretamente do recorte? |
| Produtividade | Ela explica uma etapa do argumento? |
| Especificidade | O parágrafo sobreviveria com três outros temas trocando poucas palavras? |

Classificação operacional:

- **produtivo:** específico, pertinente e usado para explicar mecanismo;
- **limítrofe/de bolso:** verdadeiro e contextualizado, mas transferível,
  analógico ou dispensável para o raciocínio;
- **genérico:** fonte vaga ou sem conteúdo verificável;
- **inventado/distorcido:** fonte inexistente ou conceito atribuído sem respaldo.

Microdados 2025 mostraram C2 e C3 variando de 120 a 200 para o mesmo texto entre
avaliadores oficiais. Documento adicional reportado pelo g1 ligou a avaliação
negativa do repertório na C2 à C3. Por isso, referência limítrofe exige faixa e
justificativa; não deve receber 200 automaticamente nem ser tratada como
invenção. C3 só cai quando a fragilidade também compromete desenvolvimento e
progressão — não por contágio mecânico.

O caso citado pela matéria mostra limite de qualquer checklist: Mbembe foi
contextualizado com composição etária do Congresso, políticas públicas e
geriatria nas UBS, mas ainda recebeu C2=120 de um avaliador e 200 de outros. Um
mecanismo específico reduz risco; não elimina subjetividade oficial.

---

## Transversais (servem em quase qualquer tema)
- **Constituição Federal de 1988** `(corpus: 48)` — direitos fundamentais, art. 5º, 6º, 196 (saúde), 205 (educação), 225 (meio ambiente).
- **Declaração Universal dos Direitos Humanos (1948)** `(corpus: 12)` — dignidade, igualdade.
- **Zygmunt Bauman** — "modernidade líquida" `(corpus: 13)` — fragilidade dos laços/instituições.
- **Democracia / cidadania** `(corpus: 46/25)` — participação, esfera pública.
- **Objetivos de Desenvolvimento Sustentável (ODS/ONU)** — agenda 2030.

## Saúde
- Lei 8.080/1990 — SUS, saúde como direito universal.
- OMS — dados epidemiológicos, definição de saúde (bem-estar físico/mental/social).
- Michel Foucault — "biopoder" / "O Nascimento da Clínica" `(corpus: 7)`.
- Drauzio Varella — divulgação científica (automedicação, saúde pública).

## Envelhecimento

- **Estatuto da Pessoa Idosa (Lei 10.741/2003)** — direitos, autonomia,
  proteção contra discriminação e dever institucional.
- **Simone de Beauvoir, “A Velhice”** — construção social da marginalização na
  velhice; exige ligação a prática concreta, não só menção.
- **IBGE** — transição demográfica, expectativa de vida e composição etária;
  citar dado apenas quando houver valor e recorte confiáveis.
- **OMS — envelhecimento saudável** — capacidade funcional, participação e
  ambientes favoráveis.
- **Lei do Sexagenário (1885)** — permite contraste histórico sobre quem teve
  possibilidade material de envelhecer; explicar contexto escravista.
- **Obra ou personagem com protagonismo idoso** — usar para analisar
  representação, autonomia ou estereótipo específico.

## Segurança
- Constituição Federal art. 144 — segurança como dever do Estado.
- Estatuto do Desarmamento (Lei 10.826/2003) — porte de armas.
- Cesare Beccaria — "Dos Delitos e das Penas" (proporcionalidade da pena).
- "justiça com as próprias mãos" → **fere DH** (ver `regras_por_ano.md`).

## Educação
- Lei de Diretrizes e Bases (LDB 9.394/1996).
- Paulo Freire — "Pedagogia do Oprimido", educação como prática de liberdade `(corpus: 2)`.
- PNE (Plano Nacional de Educação); dados INEP/IDEB.
- Lei 10.639/2003 — ensino de história e cultura afro-brasileira.

## Sociedade e cultura (categoria mais frequente do corpus)
- Antonio Candido — "O Direito à Literatura" (cultura como direito).
- Milton Santos — "O Espaço do Cidadão" `(corpus: 3)` — cidadania mutilada.
- Darcy Ribeiro — "O Povo Brasileiro" — formação e diversidade.
- Hannah Arendt — banalidade do mal; esfera pública `(corpus: 5)`.
- Marilena Chauí — cultura como essência humana `(corpus: 1)`.
- Lei Maria da Penha (11.340/2006); Lei do Feminicídio (gênero).

## Ciência e tecnologia
- Lei Geral de Proteção de Dados (LGPD 13.709/2018).
- Marco Civil da Internet (12.965/2014).
- Bauman / Byung-Chul Han ("Sociedade do Cansaço") — redes e subjetividade.
- "aldeia global" (McLuhan); fake news e manipulação política.

## Meio ambiente
- Constituição art. 225 — meio ambiente ecologicamente equilibrado.
- Acordo de Paris; ODS 13 (ação climática).
- Ailton Krenak — "Ideias para Adiar o Fim do Mundo" `(corpus: 0, mas 2 no total)`.
- Política Nacional de Resíduos Sólidos (12.305/2010).

## Economia
- Constituição art. 170 — ordem econômica e valorização do trabalho.
- IBGE/IPEA — dados de desigualdade, Gini, desemprego `(corpus: IBGE 4)`.
- Amartya Sen — "Desenvolvimento como Liberdade".
- Celso Furtado — "Formação Econômica do Brasil".

## Política
- Contrato social — Rousseau/Hobbes/Locke `(corpus: contrato social 8)`.
- Montesquieu — separação dos poderes.
- DataFolha/IBOPE — pesquisas de opinião `(corpus: 2)`.
- Iluminismo — razão, esfera pública, cidadania `(corpus: 5)`.

---

## Sinal de repertório fraco (derruba C2)
- Citação **solta** sem ligar ao argumento ("como diz Bauman, ...") e segue sem usar.
- Repertório **genérico**: "estudos mostram", "segundo especialistas", "uma pesquisa".
- Dado **inventado** ou fonte inexistente.
- Repertório **só dos textos motivadores** → no máximo nível mediano (120).
- Referência verdadeira, mas intercambiável entre temas e ligada apenas por
  “sob esse viés”, “por analogia” ou fórmula ideal × realidade.
- Autor prestigioso usado para renomear a causa sem agente, prática e
  consequência observáveis.
