# Corretor de Redação ENEM

Projeto de correção de redação dissertativo-argumentativa do ENEM (5
competências, 0–1000). Agnóstico de ferramenta.

- **Metodologia canônica:** `CORRETOR.md` (fluxo, formato de saída, regras).
- **Entrada cross-agent:** `AGENTS.md` (quickstart + estrutura).
- **Shim Claude Code (auto-trigger):** `.claude/skills/corretor-enem/SKILL.md`
  — gerado de `CORRETOR.md` por `scripts/sync_shims.py`.

Quando o usuário pedir correção/avaliação/nota de redação ENEM, carregar
`CORRETOR.md` e seguir o fluxo. Antes de pontuar, ler a regra do ano em
`referencia/regras_por_ano.md`.

Setup: se `dataset/corpus.db` não existir, `python3 scripts/build_db.py`.
