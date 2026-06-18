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
2. **Sugerir** — oferecer repertório pertinente ao tema do aluno.

`(corpus: N≥900)` = nº de redações nota ≥900 no `corpus.db` que citam o termo —
sinal de que é repertório "que funciona". Termos sem marca são curados.

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
