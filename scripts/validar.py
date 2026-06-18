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
        respostas[str(eid)] = {
            "c1": None, "c2": None, "c3": None, "c4": None, "c5": None,
            "total_min": None, "total_max": None, "confianca": None,
        }
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
    pares = []  # (id, {comp: (humano, meu)}, total_humano, total_meu, faixa_info)
    ruidosos = []  # (id, motivo, score_humano, score_meu)
    for eid, meu in resp.items():
        if eid not in gab or any(meu[c] is None for c in comps):
            continue
        th = gab[eid]["score"]
        tm = sum(meu[c] for c in comps)
        cega = CEGAS / f"{eid}.txt"
        bruto = cega.read_text(encoding="utf-8") if cega.exists() else ""
        corpo = bruto.split("\n\n", 1)[1].strip() if "\n\n" in bruto else bruto.strip()
        motivo = None
        if args.clean:
            if len(corpo) == 0 and th != 0:
                motivo = "texto vazio com nota humana diferente de zero"
            elif th == 0 and len(corpo) > 400:
                motivo = "score 0 com texto completo — rótulo suspeito"
        if motivo:
            ruidosos.append((eid, motivo, th, tm))
            continue
        faixa = None
        if all(meu.get(k) is not None for k in ("total_min", "total_max", "confianca")):
            faixa = {
                "min": int(meu["total_min"]),
                "max": int(meu["total_max"]),
                "confianca": str(meu["confianca"]).lower(),
            }
        d = {c: (gab[eid][c], meu[c]) for c in comps}
        pares.append((eid, d, th, tm, faixa))

    if not pares:
        sys.exit("Nenhuma resposta preenchida em respostas.json.")

    n = len(pares)
    titulo = "# Relatório de validação (clean)" if args.clean else "# Relatório de validação"
    L = [titulo, "",
         f"Redações avaliadas: **{n}**  |  Adjacência: ±80/competência, ±100 total", ""]
    if args.clean:
        L += [f"Casos ruidosos separados: **{len(ruidosos)}**", ""]
    L += ["| Métrica | C1 | C2 | C3 | C4 | C5 | Total |",
          "|---|---|---|---|---|---|---|"]

    def pct(x):
        return f"{100*x/n:.0f}%"

    pea = {c: 0 for c in comps}; paa = {c: 0 for c in comps}
    vies = {c: 0 for c in comps}
    pea_t = paa_t = vies_t = 0
    for _, d, th, tm, _ in pares:
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

    com_faixa = [(eid, th, tm, faixa) for eid, _, th, tm, faixa in pares if faixa]
    falhas_faixa = []
    if com_faixa:
        cap = sum(f["min"] <= th <= f["max"] for _, th, _, f in com_faixa)
        largura_media = sum(f["max"] - f["min"] for _, _, _, f in com_faixa) / len(com_faixa)
        L += ["## Captura pela faixa provável", "",
              f"Casos com faixa: **{len(com_faixa)}**",
              f"Taxa de captura: **{100*cap/len(com_faixa):.0f}%**",
              f"Largura média da faixa: **{largura_media:.0f} pontos**", "",
              "| Confiança | n | captura | largura média |",
              "|---|---:|---:|---:|"]
        for conf in ("alta", "média", "media", "baixa"):
            ks = [(th, tm, f) for _, th, tm, f in com_faixa if f["confianca"] == conf]
            if not ks:
                continue
            capt = sum(f["min"] <= th <= f["max"] for th, _, f in ks)
            larg = sum(f["max"] - f["min"] for _, _, f in ks) / len(ks)
            rotulo = "média" if conf == "media" else conf
            L.append(f"| {rotulo} | {len(ks)} | {100*capt/len(ks):.0f}% | {larg:.0f} |")
        centrais_altas = [(th, tm) for _, th, tm, _ in com_faixa if tm >= 800]
        confianca_alta = [(eid, th, tm, f) for eid, th, tm, f in com_faixa if f["confianca"] == "alta"]
        L += ["", "### Humildade da nota",
              f"Casos com confiança alta: **{len(confianca_alta)}**",
              f"Viés médio dos casos com central >=800: **{(sum(tm-th for th,tm in centrais_altas)/len(centrais_altas)):+.0f}**" if centrais_altas else "Viés médio dos casos com central >=800: **n/a**",
              f"Viés médio dos casos com confiança alta: **{(sum(tm-th for _,th,tm,_ in confianca_alta)/len(confianca_alta)):+.0f}**" if confianca_alta else "Viés médio dos casos com confiança alta: **n/a**"]
        falhas_alta = [(eid, th, tm, f) for eid, th, tm, f in confianca_alta if not (f["min"] <= th <= f["max"])]
        if falhas_alta:
            L += ["", "### Casos em que confiança alta falhou",
                  "| id | humano | central | faixa |", "|---|---:|---:|---|"]
            for eid, th, tm, f in falhas_alta:
                L.append(f"| {eid} | {th} | {tm} | {f['min']}–{f['max']} |")
        falhas_faixa = [(eid, th, tm, f) for eid, th, tm, f in com_faixa if not (f["min"] <= th <= f["max"])]
        if falhas_faixa:
            L += ["", "### Casos em que a faixa não capturou a nota humana",
                  "| id | humano | central | faixa | confiança |",
                  "|---|---:|---:|---|---|"]
            for eid, th, tm, f in sorted(falhas_faixa, key=lambda x: abs(x[1]-x[2]), reverse=True):
                L.append(f"| {eid} | {th} | {tm} | {f['min']}–{f['max']} | {f['confianca']} |")
        L.append("")

    L.append("## Por redação")
    L.append("| id | tema | humano | meu | Δtotal |")
    L.append("|---|---|---|---|---|")
    for eid, d, th, tm, faixa in sorted(pares, key=lambda x: abs(x[3] - x[2]), reverse=True):
        tema = (gab[eid]["theme"] or "")[:40]
        L.append(f"| {eid} | {tema} | {th} | {tm} | {tm-th:+d} |")

    if args.clean:
        L += ["", "## Dados ruidosos separados (não entram nas métricas)",
              "| id | motivo | humano | meu |", "|---|---|---|---|"]
        for eid, motivo, th, tm in ruidosos:
            L.append(f"| {eid} | {motivo} | {th} | {tm} |")

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
    ps.add_argument("--clean", action="store_true", help="separa casos ruidosos do corpus antes de calcular métricas")
    ps.set_defaults(func=score)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
