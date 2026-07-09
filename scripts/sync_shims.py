#!/usr/bin/env python3
"""Gera shims por agent a partir de CORRETOR.md (fonte canônica).

Shims = wrappers com frontmatter especifico de cada ferramenta + o corpo completo
de CORRETOR.md. Assim o auto-trigger (Claude skill, Cursor rule) funciona com a
metodologia inteira embutida, sem drift.

Uso:
    python3 scripts/sync_shims.py            # gera todos
    python3 scripts/sync_shims.py --check    # sai non-zero se desatualizado (CI)

Edite CORRETOR.md; nunca edite os shims à mão.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANON = ROOT / "CORRETOR.md"

# Alvos: (caminho, frontmatter)
GENERATED_HEADER = (
    "<!-- GERADO por scripts/sync_shims.py a partir de CORRETOR.md. "
    "Nao editar a mao -- edite CORRETOR.md e re-rode. -->\n"
)

CLAUDE_DESCRIPTION = (
    "Corrige redação dissertativo-argumentativa do ENEM nas 5 competências "
    "oficiais (0–200 cada, 0–1000 total), com nota por competência, "
    "justificativa, trechos citados e feedback acionável. Calibra o julgamento "
    "com redações reais já corrigidas por humanos do corpus Essay-BR. Use sempre "
    "que o usuário pedir pra corrigir/avaliar/dar nota numa redação do ENEM, "
    "soltar um texto de redação na pasta redacoes/, perguntar \"quanto tiraria "
    "nisso\", pedir feedback de competência, ou simular correção ENEM. Dispara "
    "mesmo sem a palavra \"corrigir\" — \"vê minha redação\", \"tá boa essa "
    "redação?\", \"qual nota disso\" também acionam."
)

CURSOR_DESCRIPTION = (
    "Correção de redação ENEM (5 competências, 0–1000). Aciona quando o usuário "
    "pede para corrigir/avaliar/dar nota em redação ENEM ou simular correção. "
    "Carrega a metodologia de CORRETOR.md."
)

TARGETS = [
    (
        ROOT / ".claude" / "skills" / "corretor-enem" / "SKILL.md",
        f"---\nname: corretor-enem\ndescription: {CLAUDE_DESCRIPTION}\n---\n\n",
    ),
    (
        ROOT / ".cursor" / "rules" / "corretor.mdc",
        (
            "---\n"
            "description: " + CURSOR_DESCRIPTION + "\n"
            "globs:\n"
            "  - redacoes/**\n"
            "  - validacao/cegas/**\n"
            "alwaysApply: false\n"
            "---\n\n"
        ),
    ),
]


def render(frontmatter: str, body: str) -> str:
    return GENERATED_HEADER + frontmatter + body


def main() -> int:
    if not CANON.exists():
        print(f"ERRO: {CANON} nao encontrado.", file=sys.stderr)
        return 1
    body = CANON.read_text(encoding="utf-8")
    check = "--check" in sys.argv
    stale = False
    for path, frontmatter in TARGETS:
        content = render(frontmatter, body)
        path.parent.mkdir(parents=True, exist_ok=True)
        if check:
            existing = path.read_text(encoding="utf-8") if path.exists() else ""
            if existing != content:
                print(f"DESATUALIZADO: {path.relative_to(ROOT)}", file=sys.stderr)
                stale = True
        else:
            path.write_text(content, encoding="utf-8")
            print(f"OK: {path.relative_to(ROOT)}")
    if check and stale:
        print("Rode: python3 scripts/sync_shims.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
