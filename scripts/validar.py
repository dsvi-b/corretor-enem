#!/usr/bin/env python3
"""Harness de validação do corretor contra o corpus (adjacent agreement).

Mede se as notas que EU (corretor) atribuo reproduzem a nota humana real do
Essay-BR, à la TG UFPE (PEA exato + PAA adjacente ±80/comp, ±100 total).

Fluxo:
    1) python3 scripts/validar.py prepare --n 10 --seed 1
       → gera validacao/cegas/<id>.txt (tema+texto, SEM notas),
         validacao/gabarito.json (notas reais — NÃO abrir ao corrigir),
         validacao/respostas.json (esqueleto a preencher)
    2) corrigir cada arquivo de validacao/cegas/ com a skill, às cegas,
       preenchendo c1..c5 em validacao/respostas.json
    3) python3 scripts/validar.py score
       → validacao/relatorio.md com PEA/PAA/viés

Importante: ao corrigir o passo 2, NÃO ler gabarito.json (vaza a resposta).
"""
import argparse
import json
import random
import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DB = RAIZ / "dataset/corpus.db"
VAL = RAIZ / "validacao"
CEGAS = VAL / "cegas"
GABARITO = VAL / "gabarito.json"
RESPOSTAS = VAL / "respostas.json"
RELATORIO = VAL / "relatorio.md"

BANDAS = [(0, 199), (200, 399), (400, 599), (600, 799), (800, 1000)]


def prepare(args):
    if not DB.exists():
        sys.exit(f"{DB} não existe — rode: python3 scripts/build_db.py")
    random.seed(args.seed)
    con = sqlite3.connect(DB)
    # estratificar por banda de nota p/ cobrir o espectro
    por_banda = args.n // len(BANDAS)
    resto = args.n - por_banda * len(BANDAS)
    escolhidos = []
    for i, (lo, hi) in enumerate(BANDAS):
        ids = [r[0] for r in con.execute(
            "SELECT id FROM essays WHERE score BETWEEN ? AND ?", (lo, hi)).fetchall()]
        k = por_banda + (1 if i < resto else 0)
        escolhidos += random.sample(ids, min(k, len(ids)))

    CEGAS.mkdir(parents=True, exist_ok=True)
    for f in CEGAS.glob("*.txt"):
        f.unlink()
    gabarito, respostas = {}, {}
    for eid in escolhidos:
        theme, source, c1, c2, c3, c4, c5, score, text = con.execute(
            "SELECT theme,source,c1,c2,c3,c4,c5,score,text FROM essays WHERE id=?",
            (eid,)).fetchone()
        (CEGAS / f"{eid}.txt").write_text(
            f"Tema: {theme or '(sem título)'}\n\n{text}\n", encoding="utf-8")
        gabarito[str(eid)] = {"theme": theme, "source": source,
                              "c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5, "score": score}
        respostas[str(eid)] = {"c1": None, "c2": None, "c3": None, "c4": None, "c5": None}
    con.close()
    GABARITO.write_text(json.dumps(gabarito, ensure_ascii=False, indent=2), encoding="utf-8")
    RESPOSTAS.write_text(json.dumps(respostas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(escolhidos)} redações cegas em {CEGAS.relative_to(RAIZ)}/", file=sys.stderr)
    print(f"Corrija cada .txt e preencha {RESPOSTAS.relative_to(RAIZ)} (NÃO abra gabarito.json).",
          file=sys.stderr)


def score(args):
    if not (GABARITO.exists() and RESPOSTAS.exists()):
        sys.exit("Rode 'prepare' primeiro.")
    gab = json.loads(GABARITO.read_text(encoding="utf-8"))
    resp = json.loads(RESPOSTAS.read_text(encoding="utf-8"))

    comps = ["c1", "c2", "c3", "c4", "c5"]
    pares = []  # (id, {comp: (humano, meu)}, total_humano, total_meu)
    for eid, meu in resp.items():
        if eid not in gab or any(meu[c] is None for c in comps):
            continue
        d = {c: (gab[eid][c], meu[c]) for c in comps}
        th = gab[eid]["score"]
        tm = sum(meu[c] for c in comps)
        pares.append((eid, d, th, tm))

    if not pares:
        sys.exit("Nenhuma resposta preenchida em respostas.json.")

    n = len(pares)
    L = ["# Relatório de validação", "",
         f"Redações avaliadas: **{n}**  |  Adjacência: ±80/competência, ±100 total", ""]
    L += ["| Métrica | C1 | C2 | C3 | C4 | C5 | Total |",
          "|---|---|---|---|---|---|---|"]

    def pct(x):
        return f"{100*x/n:.0f}%"

    pea = {c: 0 for c in comps}; paa = {c: 0 for c in comps}
    vies = {c: 0 for c in comps}
    pea_t = paa_t = vies_t = 0
    for _, d, th, tm in pares:
        for c in comps:
            h, m = d[c]
            if h == m:
                pea[c] += 1
            if abs(h - m) <= 80:
                paa[c] += 1
            vies[c] += (m - h)
        if th == tm:
            pea_t += 1
        if abs(th - tm) <= 100:
            paa_t += 1
        vies_t += (tm - th)

    L.append("| PEA (exato) | " + " | ".join(pct(pea[c]) for c in comps) + f" | {pct(pea_t)} |")
    L.append("| PAA (adjacente) | " + " | ".join(pct(paa[c]) for c in comps) + f" | {pct(paa_t)} |")
    L.append("| Viés médio | " + " | ".join(f"{vies[c]/n:+.0f}" for c in comps) + f" | {vies_t/n:+.0f} |")
    L += ["", "Viés médio = (minha nota − humana). Positivo = eu inflo; negativo = eu deflaciono.", ""]

    L.append("## Por redação")
    L.append("| id | tema | humano | meu | Δtotal |")
    L.append("|---|---|---|---|---|")
    for eid, d, th, tm in sorted(pares, key=lambda x: abs(x[3] - x[2]), reverse=True):
        tema = (gab[eid]["theme"] or "")[:40]
        L.append(f"| {eid} | {tema} | {th} | {tm} | {tm-th:+d} |")

    RELATORIO.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"OK: {RELATORIO.relative_to(RAIZ)} ({n} redações)", file=sys.stderr)
    print(f"PAA total: {pct(paa_t)} | viés total médio: {vies_t/n:+.0f}", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description="Validação do corretor vs corpus")
    sub = p.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("prepare", help="gera amostra cega + gabarito")
    pp.add_argument("--n", type=int, default=10)
    pp.add_argument("--seed", type=int, default=1)
    pp.set_defaults(func=prepare)
    ps = sub.add_parser("score", help="compara respostas vs gabarito")
    ps.set_defaults(func=score)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
