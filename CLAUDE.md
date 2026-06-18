# Corretor de Redação ENEM

Base de conhecimento + skill pra corrigir redação dissertativo-argumentativa do
ENEM nas 5 competências, rodando no Claude Code (sem API externa, sem ML).

## Como usar

1. Soltar a redação em `redacoes/` (`.txt`/`.md`) ou colar na conversa.
2. Disparar a skill `corretor-enem` (ex: "corrige essa redação", "que nota tira
   nisso", "vê minha redação sobre <tema>").
3. Receber **nota central estimada**, **faixa provável**, confiança
   (baixa/média/alta), notas por competência, justificativa com trechos citados e
   plano de treino.

Modo padrão = **treino**: mesmo com risco de anulação, o corretor alerta e
corrige pedagogicamente. **Modo banca** só quando pedido explicitamente.

Informar o **tema** junto. Sem tema, é inferido e confirmado.

## Estrutura

```
dataset/
  essay-br/         corpus base (4570 redações, github.com/rafaelanchieta/essay)
  extended/         corpus estendido (6577 redações, github.com/lplnufpi/essay-br)
  corpus.db         SQLite: 11.147 redações reais + FTS (gerado por build_db.py)
referencia/
  regras_por_ano.md           regra vigente (2025) + mudanças por ano + drift
  cartilha_competencias.md    rubrica oficial INEP, 6 níveis/competência
  manuais_inep/cartilha_2025.txt  fonte primária INEP (cartilha 2025)
  metodologia_correcao.md     roteiro de correção (destilado do TG UFPE)
  tg_ufpe_metodologia.txt     paper-fonte (prompt-driven, 100% adjacent agreement)
  repertorio.md               banco de repertório legítimo por categoria
  calibracao_humildade.md     travas anti-inflação + confiança alta rara
  calibrador_total.md         regras empíricas para calibrar a nota central
  temas/lista_temas.md        151 temas + categorias
  redacoes_nota_1000/         exemplos comentados (2021–2025)
scripts/
  build_db.py       gera dataset/corpus.db a partir dos CSVs (idempotente)
  amostra.py        consulta corpus.db (faixa, nível, tema, busca, --escala)
  validar.py        auto-validação: adjacent agreement vs nota humana
redacoes/           suas redações pra corrigir
validacao/          gerado pelo validar.py (gitignored)
.claude/skills/corretor-enem/   a skill
```

## Regras mudam por ano

ENEM altera a prática de correção por edição. **Ano vigente: 2025.** Antes de
corrigir, o corretor lê `referencia/regras_por_ano.md` e declara no laudo qual
ano aplica. O `corpus.db` é pré-2025 → calibração com drift (esperar divergência
em C2/C4/C5). Manutenção: a cada nova edição, baixar a cartilha em
`manuais_inep/` e registrar o diff em `regras_por_ano.md`.

## Calibração (o diferencial)

A correção é ancorada nas 11.147 redações reais do `corpus.db` (já corrigidas por
humanos). Antes de fechar nota, comparar com exemplos da mesma faixa/nível:

```
python3 scripts/amostra.py --faixa 800-900 --n 2
python3 scripts/amostra.py --faixa 1000-1000 --n 1
python3 scripts/amostra.py --comp 5 --nivel 200 --n 1
python3 scripts/amostra.py --busca "Krenak" --n 1
python3 scripts/amostra.py --escala --comp 4
python3 scripts/amostra.py --tema armas --faixa 500-600 --n 2
```

## Auto-validação

Medir se o corretor acerta a nota humana (adjacent agreement):

```
python3 scripts/validar.py prepare --n 10 --seed 1   # redações cegas + gabarito
# corrigir cada validacao/cegas/*.txt e preencher validacao/respostas.json
python3 scripts/validar.py score                     # → validacao/relatorio.md
```

## Fonte da metodologia

Silva & Araujo (UFPE, 2024), *"Automated ENEM Essay Scoring and Feedbacks: A
Prompt-Driven LLM Approach"*. Decomposição em sub-análises por competência +
chain-of-thought + adesão estrita à rubrica INEP. Detalhes em
`referencia/metodologia_correcao.md`.
