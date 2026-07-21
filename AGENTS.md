# Corretor de Redação ENEM

Base de conhecimento + metodologia para corrigir redação
dissertativo-argumentativa do ENEM nas 5 competências oficiais (0–200 cada,
0–1000 total). Agnóstico de ferramenta: roda em qualquer coding agent. Sem API
externa, sem ML.

> **AGENTS.md é o ponto de entrada cross-agent** (padrão lido por Codex, Cursor,
> Gemini, etc.). A metodologia completa vive em **`CORRETOR.md`** — carregar
> sob demanda quando o usuário pedir correção.

## Quando agir

Sempre que o usuário pedir para **corrigir / avaliar / dar nota** numa redação do
ENEM, soltar um texto de redação na pasta `redacoes/`, perguntar "quanto tiraria
nisso", pedir feedback de competência, ou simular correção ENEM — mesmo sem a
palavra "corrigir" ("vê minha redação", "tá boa essa?", "qual nota disso" também
acionam).

## Como agir

1. **Carregar a metodologia:** ler `CORRETOR.md` (fluxo de correção, formato de
   saída, regras). É o arquivo canônico.
2. **Ler a regra do ano** (`referencia/regras_por_ano.md`) antes de pontuar — o
   ano vigente (2025) manda sobre o corpus.
3. **Obter a redação** de `redacoes/` (.txt/.md mais recente ou o indicado) ou da
   conversa. Pegar também o **tema** — se não informado, inferir e confirmar.
4. **Seguir o fluxo de `CORRETOR.md`** (8 passos: regra do ano → obter redação →
   modo → C1–C5 → sanity-check → calibrar central → faixa/confiança → calibrar
   com `corpus.db` → fechar laudo).
5. **Calibrar com exemplos reais** via `scripts/amostra.py` (banco de 11.147
   redações pré-2025 em `dataset/corpus.db`) e aplicar as ressalvas dos
   microdados 2025 em `referencia/regras_por_ano.md`.
6. Se o usuário fornecer **nota oficial**, preservar o resultado, comparar por
   competência e registrar onde a estimativa errou. Nota oficial é soberana no
   exame, mas microdados mostram variância interavaliador; não tratá-la como
   medida pedagógica sem ruído nem descartá-la como mero acaso. Se houver
   trajetória AV1–AV4, mostrar cada instância; AV4 é banca de três avaliadores,
   não quarto corretor individual.

Modo padrão = **treino** (corrige pedagogicamente mesmo com risco de anulação).
**Modo banca** só quando pedido explicitamente.

## Setup do ambiente (uma vez)

Se `dataset/corpus.db` não existir:

```
python3 scripts/build_db.py
```

Python 3.10+ (usa apenas stdlib: `sqlite3`). Sem dependências.

## Estrutura

```
CORRETOR.md               metodologia canônica (fluxo, formato, regras)
AGENTS.md                 este arquivo — entrada cross-agent (sempre carregado)
referencia/               rubrica INEP, regras por ano, calibração, repertório
scripts/                  build_db.py (gera corpus.db), amostra.py (consulta), validar.py
dataset/corpus.db         11.147 redações reais + FTS (gerado, gitignored)
dataset/essay-br/         corpus base (MIT) — github.com/rafaelanchieta/essay
dataset/extended/         corpus estendido (MIT) — github.com/lplnufpi/essay-br
redacoes/                 suas redações para corrigir (gitignored)
.claude/skills/corretor-enem/   shim Claude Code (auto-trigger) — GERADO
.cursor/rules/corretor.mdc     shim Cursor — GERADO
```

Shims por agent são **gerados** a partir de `CORRETOR.md` por
`scripts/sync_shims.py`. Não editar shims à mão.

## Regras mudam por ano

ENEM altera a prática de correção por edição. **Ano vigente: 2025.** O corpus é
pré-2025 → calibração com drift (esperar divergência em C2/C4/C5; seguir 2025 e
anotar). Microdados 2025 também documentam C2 e C3 variando de 120 a 200 para o
mesmo texto conforme a classificação do repertório de bolso e seu impacto no
desenvolvimento. Manutenção: a cada nova edição, baixar a cartilha em
`referencia/manuais_inep/` e registrar o diff em `referencia/regras_por_ano.md`.

## Auto-validação

Medir se as notas reproduzem a humana (adjacent agreement, à la TG UFPE):

```
python3 scripts/validar.py prepare --n 10 --seed 1   # redações cegas + gabarito
# corrigir cada validacao/cegas/*.txt seguindo CORRETOR.md, preencher respostas.json
python3 scripts/validar.py score                     # → validacao/relatorio.md
```

## Fonte da metodologia

Silva & Araujo (UFPE, 2024), *"Automated ENEM Essay Scoring and Feedbacks: A
Prompt-Driven LLM Approach"*. Decomposição em sub-análises por competência +
chain-of-thought + adesão estrita à rubrica INEP. Detalhes em
`referencia/metodologia_correcao.md`.
