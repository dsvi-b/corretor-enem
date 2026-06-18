# Metodologia de Correção — Prompt-Driven LLM

Destilado do TG UFPE *"Automated ENEM Essay Scoring and Feedbacks: A
Prompt-Driven LLM Approach"* (Silva & Araujo, 2024) — texto completo em
`tg_ufpe_metodologia.txt`. Eles atingiram **100% de concordância adjacente**
com corretores humanos nas 5 competências usando GPT-4o-mini.

## Princípio central

Não corrigir a redação "de uma vez". **Decompor** em sub-análises granulares,
uma competência por vez, com raciocínio passo a passo (chain-of-thought), e
**só então** atribuir o nível. Eles usaram 24 prompts em 6 componentes
(C1–C5 + agregador). Aqui replicamos isso como um roteiro mental por
competência.

## Cadeia por competência (o que checar antes de pontuar)

**C1 — Norma padrão** (3 passos)
1. Identificar desvios (ortografia, pontuação, concordância, regência, crase…).
2. Análise aprofundada: reincidência? diversidade dos desvios? estrutura sintática (períodos truncados/justapostos)?
3. Avaliação geral → nível 0–200.

**C2 — Tema + tipo textual** (4 passos)
1. Áreas de conhecimento acionadas / repertório (legitimado? produtivo?).
2. Aderência ao tipo dissertativo-argumentativo (tem traços de narração/descrição?).
3. Compreensão do tema (desenvolve? tangencia? foge?).
4. Avaliação geral → nível.

**C3 — Projeto de texto** (4 passos)
1. Fluxo estrutural (intro→desenvolvimento→conclusão presentes e funcionais?).
2. Avaliação do plano de texto (há progressão planejada ou amontoado?).
3. Escrutínio dos argumentos (consistentes? defendem um ponto de vista? há autoria?).
4. Avaliação geral → nível.

**C4 — Coesão** (5 passos)
1. Coesão **entre** parágrafos (cada um retoma o anterior?).
2. Repetição de palavras / eco indesejado.
3. Extração das ideias-chave (a referenciação mantém o fio?).
4. Avaliação dos conectivos/transições (diversidade vs. repetição).
5. Avaliação geral → nível.

**C5 — Proposta de intervenção** (7 passos)
1–5. Detectar **cada** um dos 5 elementos separadamente:
   **ação, agente, modo/meio, efeito, detalhamento** (ver cartilha p/ agente nulo).
6. Identificar a proposta mais completa (pode haver várias no texto).
7. Avaliação geral → nível = nº de elementos válidos (mapeado na cartilha).

## Estrutura de um bom prompt de análise (10 partes do TG)

Ao construir cada sub-análise, seguir esse esqueleto:

1. **Papel e tarefa** — "Você é especialista em correção de redação ENEM…".
2. **Controle de fluxo** — "Você receberá a redação a seguir."
3. **Contexto** — critério oficial específico daquela checagem.
4. **Instrução explícita** — focar no elemento exato sob avaliação.
5. **Exemplificação (in-context)** — exemplos de resposta válida e inválida.
6. **Casos de borda** — ex.: agente nulo, proposta ausente.
7. **Reforço** — repetir a diretriz crítica no fim (contra recency bias).
8. **Chain-of-thought** — "Pense passo a passo e explique antes de responder."
9. **Casos múltiplos** — ex.: mais de uma proposta de intervenção.
10. **Saída estruturada** — formato fixo (aqui: ver SKILL.md).

## Calibração obrigatória

Antes de fechar as notas, puxar exemplos reais já corrigidos por humanos na
faixa estimada, pra ancorar o julgamento:

```
python3 scripts/amostra.py --faixa 800-900 --n 2
python3 scripts/amostra.py --faixa 1000-1000 --n 1
```

Comparar a redação sob correção com esses exemplos da mesma faixa. Se a sua
nota destoar do padrão dos exemplos, revisar.

## Notas de fidelidade

- O sistema do TG roda em inglês internamente mas foi escrito/testado em PT.
  Aqui mantemos tudo em PT — é a língua da prova.
- Concordância adjacente (não exata) é a métrica que importa: acertar a
  **faixa** (±80/competência, ±100 total), não o ponto exato.
- A rubrica oficial usa termos subjetivos ("muito bem", "detalhado"). Os
  manuais de correção por competência dão os critérios concretos — por isso a
  cartilha lista os elementos contáveis (sobretudo C5).
