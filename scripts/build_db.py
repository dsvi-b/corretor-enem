#!/usr/bin/env python3
"""Constrói dataset/corpus.db a partir dos corpora Essay-BR (base + extended).

Tabela `essays` (uma redação por linha) + índice FTS5 `essays_fts` (busca full-text
no texto e no tema). Idempotente: recria do zero a cada execução.

    python3 scripts/build_db.py
"""
import ast
import csv
import sqlite3
import sys
from pathlib import Path

csv.field_size_limit(10_000_000)

RAIZ = Path(__file__).resolve().parent.parent
DB = RAIZ / "dataset/corpus.db"
EXT = RAIZ / "dataset/extended/extended-corpus"
BASE = RAIZ / "dataset/essay-br/essay-br"


def texto(raw):
    try:
        return "\n\n".join(ast.literal_eval(raw))
    except (ValueError, SyntaxError):
        return raw


def temas_extended():
    """prompt_id -> (title, category) do extended."""
    m = {}
    with open(EXT / "prompts.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m[r["id"]] = (r["title"].strip(), r.get("category", "").strip())
    return m


def linhas_extended():
    temas = temas_extended()
    with open(EXT / "extended_essay-br.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t, cat = temas.get(r["prompt"], ("", ""))
            yield ("extended", r["prompt"], t, cat,
                   int(r["c1"]), int(r["c2"]), int(r["c3"]), int(r["c4"]), int(r["c5"]),
                   int(r["score"]), texto(r["essay"]))


def linhas_base():
    with open(BASE / "essay-br.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c = [int(x) for x in ast.literal_eval(r["competence"])]
            yield ("base", r["prompt"], r["title"].strip(), "",
                   c[0], c[1], c[2], c[3], c[4], int(r["score"]), texto(r["essay"]))


def main():
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript("""
        CREATE TABLE essays (
            id INTEGER PRIMARY KEY,
            source TEXT, prompt_id TEXT, theme TEXT, category TEXT,
            c1 INT, c2 INT, c3 INT, c4 INT, c5 INT, score INT, text TEXT
        );
        CREATE VIRTUAL TABLE essays_fts USING fts5(
            theme, text, content='essays', content_rowid='id', tokenize='unicode61'
        );
    """)
    cols = "source,prompt_id,theme,category,c1,c2,c3,c4,c5,score,text"
    ph = ",".join("?" * 11)
    n = 0
    for fonte in (linhas_extended, linhas_base):
        for row in fonte():
            con.execute(f"INSERT INTO essays ({cols}) VALUES ({ph})", row)
            n += 1
    con.execute(
        "INSERT INTO essays_fts (rowid, theme, text) SELECT id, theme, text FROM essays"
    )
    con.executescript("""
        CREATE INDEX idx_score ON essays(score);
        CREATE INDEX idx_source ON essays(source);
    """)
    con.commit()
    tot = con.execute("SELECT COUNT(*) FROM essays").fetchone()[0]
    mil = con.execute("SELECT COUNT(*) FROM essays WHERE score=1000").fetchone()[0]
    con.close()
    print(f"OK: {tot} redações em {DB.relative_to(RAIZ)} (nota 1000: {mil})", file=sys.stderr)


if __name__ == "__main__":
    main()
