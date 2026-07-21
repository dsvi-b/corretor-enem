# Calibração observada — erros sistemáticos conhecidos do corretor

Registro empírico de onde a correção tende a errar sistematicamente, ancorado em
redações reais com nota humana conhecida. **Consultar antes de fechar a nota** —
se o texto cair num destes padrões, revisar a tendência contrária.

> Achados derivados de validação contra redações reais corrigidas por banca.
> Conteúdo vivo: adicionar aqui novos vieses confirmados, com a redação-fonte.

## C1 — tendência a sobre-penalizar estilo

**Tendência:** classificar como "erro recorrente de norma" o que é construção
estilística/criativa.

**Exemplo real:** construções como *"Nem ética, para Nietzsche…"* (frase
fragmentada estilística) ou possíveis neologismos (*"agros transversais"*) foram
penalizados como desvio de norma. A banca viu "poucos desvios" (160) onde o
corretor viu "alguns" (120).

**Regra:** só conta desvio de norma-padrão claro e recorrente (concordância,
regência, ortografia, acentuação, pontuação inequívoca). Ambiguidade sintática
estilística é tolerada.

**Como aplicar:** antes de dar C1=120, confirmar que os desvios são
inequivocamente erros de norma (não estilo), e que há pelo menos 3+ ocorrências
distintas de tipos diferentes. Em dúvida → 160.

## C4 — aplicar F6 forte demais

**Tendência:** derrubar para 120 textos que têm, na verdade, diversidade coesiva
real.

**Exemplo real:** texto com sequência, adição, conclusivos, referenciais e
causais em estrutura organizada foi punido para 120 por causa de conectivos
protocolares. A banca deu 160.

**Regra:** a trava F6 ("conectivo presente não garante C4") é para texto com
poucos recursos coesivos ou todos repetidos. **Não se aplica** quando há
variedade de funções coesivas.

**Como aplicar:** contar tipos funcionais distintos (sequência / adição /
referenciação / conclusão / causal). **4+ tipos em texto organizado → 160.** Só
120 se predomina 1 tipo ou os encadeamentos são vazios.

## Caso oficial ENEM 2025 — filosofia abstrata + proposta dupla

**Resultado final da banca:** C1=160, C2=120, C3=120, C4=160, C5=200; total 760.

**Trajetória oficial recuperada nos microdados:**

| Instância | C1 | C2 | C3 | C4 | C5 | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AV1 | 160 | 200 | 160 | 160 | 160 | 840 |
| AV2 | 120 | 160 | 160 | 120 | 120 | 680 |
| AV3 | 160 | 120 | 120 | 160 | 200 | 760 |
| AV4 — banca de 3 | 160 | 120 | 120 | 160 | 200 | 760 |

O registro anonimizado foi identificado por combinação única das notas entre
4.810.772 linhas. A diferença inicial de 160 acionou AV3. Sua nota ficou 80
pontos distante de AV1 e AV2; a equidistância levou a AV4. A banca confirmou
integralmente AV3. Portanto, houve três correções individuais e uma adjudicação
colegiada, não quatro leituras individuais independentes.

**Perfil do texto:** introdução com *Bhagavad Gita*, D1 com Nietzsche, D2 com
Foucault, vocabulário formal, muitos conectivos e duas propostas de intervenção
(União + Secretaria de Comunicação Social). O texto tem arquitetura visível,
mas explica pouco os mecanismos materiais do idadismo.

### Lições por competência

- **C1 final 160; faixa individual 120–160:** linguagem sofisticada não elimina
  impropriedades lexicais e construções como "requer promover"; também não se
  deve sobre-penalizar estilo.
- **C2 final 120; faixa individual 120–200:** esta é a principal fronteira. Gita,
  moral do ressentimento e regime de verdade foram aceitos como produtivos por
  AV1 e rebaixados por AV3 e banca. Fonte legítima não garante produtividade;
  ligação por analogia ampla continua arriscada.
- **C3 final 120; faixa individual 120–160:** AV1 e AV2 reconheceram 160, mas AV3
  e banca deram 120. Quatro parágrafos e tese bifurcada não garantem progressão;
  termos abstratos não substituem agente → prática → consequência concreta.
- **C4 final 160; faixa individual 120–160:** diversidade e constância sustentam
  160 na maioria das instâncias, mas retomadas vagas e relações artificiais ainda
  permitem leitura em 120.
- **C5 final 200; faixa individual 120–200:** AV1 deu 160 e AV2, 120; AV3 e banca
  reconheceram 200. A proposta deve ser preservada porque recebeu o teto no
  veredito final, não porque tenha sido unanimemente considerada completa.

**Regra de calibração:** texto com repertório prestigioso, estrutura pronta e
proposta completa, mas sem exemplos ou cadeia causal concreta, deve começar com
C2/C3 em 120–160, não em 200. C4 começa em 160 quando há diversidade funcional;
só sobe a 200 se as relações também forem precisas. C5 pode ser mantida em 200
quando os cinco elementos estão demonstráveis, mas a justificativa deve apontar
cada elemento: a trajetória 120–200 proíbe tratá-la como força automática.

### Limite dessa âncora

A nota final de 760 é dado administrativo soberano, não leitura individual
unânime: o mesmo texto recebeu 680, 760 e 840 de corretores oficiais. AV1 mostra
que 840 era uma leitura possível; AV3 e banca mostram que não era boa previsão do
veredito. Usar 760 para corrigir inflação conhecida, preservar 680–840 como faixa
empírica deste texto e não transformar nenhum ponto dessa faixa em teto universal
para toda redação filosófica.

## Repertório-teto — "individualismo" trava em C3=160

**Achado de corpus (`dataset/corpus.db`, Essay-BR):** `individualismo` + C3=200 =
**0 redações**. Todas travam em C3=160. É estrutural: o termo é usado como
*rótulo diagnóstico* ("brasileiros são individualistas → problema persiste"), não
como *mecanismo causal*.

**Perfil estatístico que separa C3=200 de C3=160** (mesmo ~350 palavras):
- degraus de raciocínio: **8,2 (200) vs 6,9 (160)** — a 200 raciocina em mais passos.
- conectivos ornamentais (ademais/outrossim/destarte): **1,17 (200) vs 2,53 (160)**
  — a 160 enfeita mais para compensar falta de encadeamento lógico.

**Como furar o teto:** mecanismo causal de 4 degraus, repertório que **explica a
origem** (Tocqueville cunhou o termo; Jung+Edinger, eixo ego-Self) em vez de
**renomear** (Bauman, "tempos líquidos"). Detalhado em
`referencia/formula_individualismo.md`.

**Generalização:** repertórios usados como rótulo/diagnóstico (não como
mecanismo) tendem a travar a C3. Avaliar se o repertório *explica* ou só *nomeia*.
