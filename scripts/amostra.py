#!/usr/bin/env python3
"""Consulta o banco corpus.db — redações reais Essay-BR já corrigidas por humanos.

Usado pelo corretor pra calibrar nota: puxa exemplos por faixa, por nível de uma
competência, ou por busca full-text (repertório/tema/conteúdo).

Exemplos:
    python3 scripts/amostra.py --faixa 900-1000 --n 2
    python3 scripts/amostra.py --comp 5 --nivel 200 --n 2      # C5 nota máxima
    python3 scripts/amostra.py --busca "Krenak" --n 1          # quem citou Krenak
    python3 scripts/amostra.py --faixa 500-600 --tema armas --n 2
"""
import argparse
import random
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "dataset/corpus.db"


def main():
    p = argparse.ArgumentParser(description="Consulta redações Essay-BR (corpus.db)")
    p.add_argument("--faixa", default="0-1000", help="faixa de nota total, ex: 900-1000")
    p.add_argument("--n", type=int, default=2, help="quantas redações")
    p.add_argument("--tema", default="", help="filtra tema por substring")
    p.add_argument("--busca", default="", help="busca full-text no texto (FTS5)")
    p.add_argument("--comp", type=int, choices=range(1, 6), help="competência 1-5 p/ filtrar nível")
    p.add_argument("--nivel", type=int, choices=[0, 40, 80, 120, 160, 200], help="nível da competência escolhida")
    p.add_argument("--escala", action="store_true", help="com --comp N: 1 exemplo de cada nível 0-200 da competência")
    p.add_argument("--base", choices=["base", "extended", "all"], default="all")
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    if not DB.exists():
        p.error(f"{DB} não existe — rode: python3 scripts/build_db.py")
    if args.escala:
        if args.comp is None:
            p.error("--escala exige --comp N")
        escala(args)
        return
    if (args.comp is None) != (args.nivel is None):
        p.error("--comp e --nivel devem ser usados juntos")

    lo, hi = (int(x) for x in args.faixa.split("-"))
    con = sqlite3.connect(DB)

    where = ["e.score BETWEEN ? AND ?"]
    params = [lo, hi]
    if args.base != "all":
        where.append("e.source = ?"); params.append(args.base)
    if args.tema:
        where.append("e.theme LIKE ?"); params.append(f"%{args.tema}%")
    if args.comp:
        where.append(f"e.c{args.comp} = ?"); params.append(args.nivel)

    join = ""
    if args.busca:
        join = "JOIN essays_fts f ON f.rowid = e.id"
        where.append("essays_fts MATCH ?"); params.append(args.busca)

    sql = (f"SELECT e.theme,e.source,e.c1,e.c2,e.c3,e.c4,e.c5,e.score,e.text "
           f"FROM essays e {join} WHERE " + " AND ".join(where))
    rows = con.execute(sql, params).fetchall()
    con.close()

    if not rows:
        print("Nenhuma redação com esses filtros.", file=sys.stderr)
        sys.exit(1)

    if args.seed is not None:
        random.seed(args.seed)
    amostra = random.sample(rows, min(args.n, len(rows)))

    filtro_desc = f"faixa {args.faixa}"
    if args.comp:
        filtro_desc += f" | C{args.comp}={args.nivel}"
    if args.tema:
        filtro_desc += f" | tema~{args.tema}"
    if args.busca:
        filtro_desc += f" | busca:{args.busca}"
    print(f"# {len(rows)} redações ({filtro_desc}) | mostrando {len(amostra)}\n")
    for i, r in enumerate(amostra, 1):
        bloco(r, f"## Exemplo {i}")


def bloco(r, rotulo):
    theme, source, c1, c2, c3, c4, c5, score, text = r
    print(f"{rotulo} — nota {score} [{source}]")
    print(f"Tema: {theme or '(sem título)'}")
    print(f"Competências: C1={c1} C2={c2} C3={c3} C4={c4} C5={c5}\n")
    print(text)
    print("\n" + "-" * 70 + "\n")


def escala(args):
    """Mostra 1 exemplo de cada nível (0..200) da competência --comp."""
    con = sqlite3.connect(DB)
    if args.seed is not None:
        random.seed(args.seed)
    print(f"# Escala da Competência {args.comp} — 1 exemplo por nível\n")
    for nivel in (0, 40, 80, 120, 160, 200):
        rows = con.execute(
            f"SELECT theme,source,c1,c2,c3,c4,c5,score,text FROM essays WHERE c{args.comp}=?",
            (nivel,),
        ).fetchall()
        if not rows:
            print(f"## C{args.comp} = {nivel}: (sem exemplo no corpus)\n")
            continue
        bloco(random.choice(rows), f"## C{args.comp} = {nivel}")
    con.close()


if __name__ == "__main__":
    main()
