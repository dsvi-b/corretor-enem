# Corretor de Redação ENEM

Corretor de redação dissertativo-argumentativa do ENEM nas **5 competências
oficiais** (0–200 cada, 0–1000 total), ancorado em **11.147 redações reais**
já corrigidas por banca. Roda dentro de qualquer coding agent (Claude Code,
Codex, Cursor, Gemini, Aider…). **Sem API externa, sem ML.**

A correção segue a metodologia *prompt-driven* de Silva & Araujo (UFPE, 2024) —
decomposição em sub-análises por competência + chain-of-thought + adesão estrita
à rubrica INEP — ancorada em um corpus SQLite local.

> ⚠️ **Aviso.** Estimativa pedagógica, não nota oficial. O ENEM começa com dois
> avaliadores e pode convocar terceiro avaliador ou banca extraordinária. Os
> microdados 2025 documentam divergências amplas, sobretudo na C2. Este projeto
> modela a incerteza; não oferece previsão contratual nem substitui o resultado
> oficial.

## Por que usar

- **Calibrado em dados reais.** Antes de fechar a nota, consulta redações reais
  da mesma faixa/nível no `corpus.db` (Essay-BR). Reduz viés de "agente bonzinho".
- **Rubrica oficial, por ano.** Aplica a cartilha INEP do ano vigente (2025) e
  sinaliza *drift* onde a prática mudou em relação ao corpus (pré-2025).
- **Saida estruturada e acionável.** Nota central + faixa provável + confiança +
  diagnóstico + redação anotada + trecho reescrito + plano de treino.
- **Modo treino x modo banca.** Padrão corrige pedagogicamente mesmo com risco de
  anulação; modo banca zera como a banca zeraria.
- **Agnóstico de ferramenta.** Metodologia em markdown puro; shims finos por
  agent. Funciona no seu agente favorito.

## Quickstart

### 1. Setup (uma vez)

```bash
git clone https://github.com/dsvi-b/corretor-enem.git
cd corretor-enem
python3 scripts/build_db.py     # gera dataset/corpus.db (44 MB)
```

Requer **Python 3.10+** (apenas stdlib: `sqlite3`). Sem `pip install`.

### 2. Soltar a redação

Coloque sua redação em `redacoes/` (`.txt` ou `.md`) **ou** cole o texto na
conversa. Informe o **tema** junto (sem tema, é inferido e confirmado).

### 3. Pedir a correção (no seu agent)

Abra a pasta do projeto no agente e peça:

> *corrija a redação em redacoes/ sobre o tema X* — ou — *que nota essa redação
> tira?* (cole o texto)

| Agent | O que acontece |
|---|---|
| **Claude Code** | skill `corretor-enem` auto-dispara pela descrição (`.claude/skills/`) |
| **OpenAI Codex** | lê `AGENTS.md` → carrega `CORRETOR.md` e segue o fluxo |
| **Cursor** | regra `.cursor/rules/corretor.mdc` aciona ao editar `redacoes/` |
| **Gemini CLI** | lê `AGENTS.md` → carrega `CORRETOR.md` |
| **Aider** | `aider --read CORRETOR.md` e peça a correção |
| **Qualquer outro** | diga ao agent: *"leia `CORRETOR.md` e corrija esta redação"* |

Saída esperada: nota central estimada, faixa provável, confiança
(baixa/média/alta), tabela por competência, diagnóstico, redação anotada e plano
de treino. Veja o formato completo em [`CORRETOR.md`](CORRETOR.md).

## Como funciona

1. **Regra do ano** (`referencia/regras_por_ano.md`) é carregada — o ano vigente
   manda sobre o corpus.
2. **Gate de anulação** (fuga ao tema, tipo textual errado, texto insuficiente,
   etc.). Em modo treino, vira *Alerta de risco*; em modo banca, zera.
3. **C1→C5**, competência por competência, com chain-of-thought, citando trechos
   literais como evidência e respeitando a regra anti-halo (cada competência com
   prova própria).
4. **Sanity-check** do total contra inflação/punição em cascata.
5. **Calibração da central** com regras empíricas
   (`referencia/calibrador_total.md`, `auditoria_extremos.md`,
   `calibracao_observada.md`).
6. **Faixa provável + confiança** com travas anti-inflação
   (`referencia/calibracao_humildade.md`).
7. **Calibração com exemplos reais** via `scripts/amostra.py` sobre o `corpus.db`.
8. **Confronto com nota oficial**, quando fornecida, sem apagar diferença entre
   resultado administrativo e estimativa pedagógica.

## Estrutura

```
CORRETOR.md               metodologia canônica (fluxo, formato, regras)
AGENTS.md                 entrada cross-agent (lida por Codex/Cursor/Gemini)
CLAUDE.md                 shim Claude Code
referencia/               rubrica INEP, regras por ano, calibração, repertório
scripts/
  build_db.py             gera dataset/corpus.db a partir dos CSVs (idempotente)
  amostra.py              consulta o corpus (faixa, nível, tema, busca FTS, --escala)
  validar.py              harness de auto-validação (adjacent agreement vs humano)
  sync_shims.py           regenera .claude/skills e .cursor/rules a partir de CORRETOR.md
dataset/
  corpus.db               11.147 redações reais + FTS (gerado, gitignored)
  essay-br/               corpus base (MIT) — github.com/rafaelanchieta/essay
  extended/               corpus estendido (MIT) — github.com/lplnufpi/essay-br
redacoes/                 suas redações (gitignored)
.claude/skills/corretor-enem/SKILL.md   shim Claude (GERADO)
.cursor/rules/corretor.mdc              shim Cursor (GERADO)
```

## Calibração — o diferencial

A correção é ancorada nas 11.147 redações reais do `corpus.db`. Antes de fechar
nota, o agent compara com exemplos da mesma faixa/nível:

```bash
python3 scripts/amostra.py --faixa 800-900 --n 2     # exemplos da faixa estimada
python3 scripts/amostra.py --faixa 1000-1000 --n 1   # padrão-ouro
python3 scripts/amostra.py --escala --comp 4         # régua 0→200 da C4
python3 scripts/amostra.py --busca "Krenak" --n 1    # checar repertório
python3 scripts/amostra.py --tema armas --faixa 500-600 --n 2
```

`--help` em cada script lista todas as opções.

## Auto-validação

Meça se as notas do agent reproduzem a humana (*adjacent agreement*):

```bash
python3 scripts/validar.py prepare --n 10 --seed 1   # redações cegas + gabarito oculto
# corrija cada validacao/cegas/*.txt seguindo CORRETOR.md; preencha respostas.json
python3 scripts/validar.py score                     # → validacao/relatorio.md
```

## Limitações conhecidas

- **Drift do corpus.** O `corpus.db` é pré-2025. A prática de C2/C4/C5 mudou; o
  corretor segue o ano vigente e anota a divergência, mas espere ruído nessas
  competências.
- **Estimativa, não veredito.** Faixa provável ±100/160/240 conforme confiança.
- **Variância interavaliador.** Microdados 2025 registraram C2 e C3 variando de
  120 a 200 para o mesmo texto; um caso passou por 600, 760 e 960 antes de
  receber 1000 da banca extraordinária, que teve acesso às notas anteriores.
  Isso exige faixa e humildade, mas não torna toda correção aleatória.
- **Erros correlacionados.** Várias IAs ou correções de cursinho podem premiar os
  mesmos sinais superficiais e repetir a mesma inflação.
- **Repertório.** O agent pode ser enganado por repertório inventado; o fluxo manda
  conferir em `repertorio.md` ou com `amostra.py --busca`. Fonte verdadeira e
  frequente no corpus ainda pode ser repertório de bolso.

## Adicionar suporte a outro agent

1. A metodologia já é agnóstica em `CORRETOR.md`.
2. Crie um shim com o frontmatter da ferramenta apontando para `CORRETOR.md`
   (ou embutindo o corpo). Use `scripts/sync_shims.py` como modelo.
3. Se o agente lê um arquivo raiz, adicione uma linha em `AGENTS.md` ou crie o
   equivalente (ex.: `GEMINI.md`, `.windsurfrules`, `.clinerules`).

## Metodologia e fontes

- Silva, G. F.; Araujo, R. *"Automated ENEM Essay Scoring and Feedbacks: A
  Prompt-Driven LLM Approach"*. UFPE, 2024. Roteiro destilado em
  `referencia/metodologia_correcao.md`; paper-fonte em
  `referencia/tg_ufpe_metodologia.txt`.
- Cartilha do Participante INEP (2025) em `referencia/manuais_inep/`.
- [Microdados do Enem — Inep](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)
  e [levantamento do g1 sobre divergências de 2025](https://g1.globo.com/educacao/noticia/2026/06/26/divergencia-notas-redacao-enem-2025.ghtml).
- Corpus Essay-BR (MIT): [rafaelanchieta/essay](https://github.com/rafaelanchieta/essay)
  e [lplnufpi/essay-br](https://github.com/lplnufpi/essay-br).

## Licença

MIT — veja [LICENSE](LICENSE). Os corpora em `dataset/essay-br/` e
`dataset/extended/` mantêm suas próprias licenças MIT (atribuição preservada).
