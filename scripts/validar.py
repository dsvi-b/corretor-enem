#!/usr/bin/env python3
"""Harness de validação do corretor contra o corpus (adjacent agreement).

Fluxo:
    python3 scripts/validar.py prepare --n 10 --seed 1
    # corrigir validacao/cegas/*.txt às cegas e preencher respostas.json
    python3 scripts/validar.py score --clean
    python3 scripts/validar.py export-history --seed 1
    python3 scripts/validar.py calibrate

Importante: ao corrigir, NÃO ler gabarito.json (vaza a resposta).
"""
import argparse
import json
import random
import sqlite3
import statistics
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DB = RAIZ / "dataset/corpus.db"
VAL = RAIZ / "validacao"
CEGAS = VAL / "cegas"
GABARITO = VAL / "gabarito.json"
RESPOSTAS = VAL / "respostas.json"
RELATORIO = VAL / "relatorio.md"
HISTORICO = VAL / "historico_validacoes.jsonl"
CALIBRACAO = VAL / "calibracao_total.md"

BANDAS = [(0, 199), (200, 399), (400, 599), (600, 799), (800, 1000)]
COMPS = ["c1", "c2", "c3", "c4", "c5"]
FLAGS = [
    "texto_curto", "paragrafo_unico", "repertorio_generico", "proposta_incompleta",
    "argumentacao_generica", "coesao_basica", "c1_recorrente", "central_800_mais",
    "risco_superestimacao",
]


def prepare(args):
    if not DB.exists():
        sys.exit(f"{DB} não existe — rode: python3 scripts/build_db.py")
    random.seed(args.seed)
    con = sqlite3.connect(DB)
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
            "total_central": None, "total_min": None, "total_max": None, "confianca": None,
            **{flag: False for flag in FLAGS},
        }
    con.close()
    GABARITO.write_text(json.dumps(gabarito, ensure_ascii=False, indent=2), encoding="utf-8")
    RESPOSTAS.write_text(json.dumps(respostas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(escolhidos)} redações cegas em {CEGAS.relative_to(RAIZ)}/", file=sys.stderr)
    print(f"Corrija cada .txt e preencha {RESPOSTAS.relative_to(RAIZ)} (NÃO abra gabarito.json).",
          file=sys.stderr)


def corpo_cega(eid):
    cega = CEGAS / f"{eid}.txt"
    bruto = cega.read_text(encoding="utf-8") if cega.exists() else ""
    return bruto.split("\n\n", 1)[1].strip() if "\n\n" in bruto else bruto.strip()


def motivo_ruido(eid, score_humano):
    corpo = corpo_cega(eid)
    if len(corpo) == 0 and score_humano != 0:
        return "texto vazio com nota humana diferente de zero"
    if score_humano == 0 and len(corpo) > 400:
        return "score 0 com texto completo — rótulo suspeito"
    return None


def montar_pares(clean=False):
    if not (GABARITO.exists() and RESPOSTAS.exists()):
        sys.exit("Rode 'prepare' primeiro.")
    gab = json.loads(GABARITO.read_text(encoding="utf-8"))
    resp = json.loads(RESPOSTAS.read_text(encoding="utf-8"))
    pares, ruidosos = [], []
    for eid, meu in resp.items():
        if eid not in gab or any(meu.get(c) is None for c in COMPS):
            continue
        th = gab[eid]["score"]
        tm = int(meu.get("total_central") if meu.get("total_central") is not None else sum(int(meu[c]) for c in COMPS))
        motivo = motivo_ruido(eid, th) if clean else None
        if motivo:
            ruidosos.append((eid, motivo, th, tm))
            continue
        faixa = None
        if all(meu.get(k) is not None for k in ("total_min", "total_max", "confianca")):
            faixa = {"min": int(meu["total_min"]), "max": int(meu["total_max"]),
                     "confianca": str(meu["confianca"]).lower()}
        d = {c: (gab[eid][c], int(meu[c])) for c in COMPS}
        pares.append((eid, d, th, tm, faixa, gab[eid], meu))
    return pares, ruidosos


def score(args):
    pares, ruidosos = montar_pares(clean=args.clean)
    if not pares:
        sys.exit("Nenhuma resposta preenchida em respostas.json.")

    n = len(pares)
    titulo = "# Relatório de validação (clean)" if args.clean else "# Relatório de validação"
    L = [titulo, "", f"Redações avaliadas: **{n}**  |  Adjacência: ±80/competência, ±100 total", ""]
    if args.clean:
        L += [f"Casos ruidosos separados: **{len(ruidosos)}**", ""]
    L += ["| Métrica | C1 | C2 | C3 | C4 | C5 | Total |",
          "|---|---|---|---|---|---|---|"]

    def pct(x):
        return f"{100*x/n:.0f}%"

    pea = {c: 0 for c in COMPS}; paa = {c: 0 for c in COMPS}; vies = {c: 0 for c in COMPS}
    pea_t = paa_t = vies_t = mae_t = 0
    for _, d, th, tm, _, _, _ in pares:
        for c in COMPS:
            h, m = d[c]
            pea[c] += (h == m)
            paa[c] += (abs(h - m) <= 80)
            vies[c] += (m - h)
        pea_t += (th == tm)
        paa_t += (abs(th - tm) <= 100)
        vies_t += (tm - th)
        mae_t += abs(tm - th)

    L.append("| PEA (exato) | " + " | ".join(pct(pea[c]) for c in COMPS) + f" | {pct(pea_t)} |")
    L.append("| PAA (adjacente) | " + " | ".join(pct(paa[c]) for c in COMPS) + f" | {pct(paa_t)} |")
    L.append("| Viés médio | " + " | ".join(f"{vies[c]/n:+.0f}" for c in COMPS) + f" | {vies_t/n:+.0f} |")
    L.append(f"| Erro abs. médio | - | - | - | - | - | {mae_t/n:.0f} |")
    L += ["", "Viés médio = (minha nota − humana). Positivo = eu inflo; negativo = eu deflaciono.", ""]

    com_faixa = [(eid, th, tm, faixa) for eid, _, th, tm, faixa, _, _ in pares if faixa]
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
            L += ["", "### Casos em que confiança alta falhou", "| id | humano | central | faixa |", "|---|---:|---:|---|"]
            for eid, th, tm, f in falhas_alta:
                L.append(f"| {eid} | {th} | {tm} | {f['min']}–{f['max']} |")
        falhas_faixa = [(eid, th, tm, f) for eid, th, tm, f in com_faixa if not (f["min"] <= th <= f["max"])]
        if falhas_faixa:
            L += ["", "### Casos em que a faixa não capturou a nota humana",
                  "| id | humano | central | faixa | confiança |", "|---|---:|---:|---|---|"]
            for eid, th, tm, f in sorted(falhas_faixa, key=lambda x: abs(x[1]-x[2]), reverse=True):
                L.append(f"| {eid} | {th} | {tm} | {f['min']}–{f['max']} | {f['confianca']} |")
        L.append("")

    L.append("## Por redação")
    L.append("| id | tema | humano | meu | Δtotal |")
    L.append("|---|---|---|---|---|")
    for eid, _, th, tm, _, gab, _ in sorted(pares, key=lambda x: abs(x[3] - x[2]), reverse=True):
        tema = (gab["theme"] or "")[:40]
        L.append(f"| {eid} | {tema} | {th} | {tm} | {tm-th:+d} |")

    if args.clean:
        L += ["", "## Dados ruidosos separados (não entram nas métricas)",
              "| id | motivo | humano | meu |", "|---|---|---|---|"]
        for eid, motivo, th, tm in ruidosos:
            L.append(f"| {eid} | {motivo} | {th} | {tm} |")

    RELATORIO.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"OK: {RELATORIO.relative_to(RAIZ)} ({n} redações)", file=sys.stderr)
    print(f"PAA total: {pct(paa_t)} | viés total médio: {vies_t/n:+.0f} | EAM total: {mae_t/n:.0f}", file=sys.stderr)


def export_history(args):
    pares, ruidosos = montar_pares(clean=True)
    ruido_ids = {eid for eid, _, _, _ in ruidosos}
    VAL.mkdir(exist_ok=True)
    with HISTORICO.open("a", encoding="utf-8") as f:
        for eid, _, th, tm, faixa, gab, meu in pares:
            rec = {
                "seed": args.seed,
                "id": eid,
                "tema": gab.get("theme") or "",
                **{f"{c}_pred": int(meu[c]) for c in COMPS},
                "total_pred_bruto": sum(int(meu[c]) for c in COMPS),
                "total_pred_central": tm,
                "total_min": faixa["min"] if faixa else None,
                "total_max": faixa["max"] if faixa else None,
                "confianca": faixa["confianca"] if faixa else None,
                **{f"{c}_humano": int(gab[c]) for c in COMPS},
                "total_humano": th,
                "erro_total": tm - th,
                "erro_abs_total": abs(tm - th),
            }
            for flag in FLAGS:
                rec[flag] = bool(meu.get(flag, False))
            rec["central_800_mais"] = tm >= 800
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"OK: anexados {len(pares)} casos limpos em {HISTORICO.relative_to(RAIZ)}", file=sys.stderr)
    if ruido_ids:
        print(f"Ignorados por ruído: {len(ruido_ids)}", file=sys.stderr)


def pred_total(r):
    return r.get("total_pred_central", r["total_pred_bruto"])


def faixa_total(x):
    if x < 400: return "0-399"
    if x < 520: return "400-519"
    if x < 640: return "520-639"
    if x < 760: return "640-759"
    if x < 880: return "760-879"
    return "880-1000"


def media(xs):
    return sum(xs) / len(xs) if xs else 0


def calibrate(args):
    if not HISTORICO.exists():
        sys.exit(f"{HISTORICO} não existe — rode export-history primeiro")
    rows = [json.loads(l) for l in HISTORICO.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not rows:
        sys.exit("Histórico vazio")

    L = ["# Calibração empírica da nota total", "", f"Casos no histórico: **{len(rows)}**", ""]
    erros = [r["erro_total"] for r in rows]
    abses = [r["erro_abs_total"] for r in rows]
    L += [f"Erro médio absoluto do total: **{media(abses):.0f}**",
          f"Viés médio: **{media(erros):+.0f}**", ""]

    L += ["## Erro por faixa de total_pred_bruto", "", "| Faixa | n | viés | EAM |", "|---|---:|---:|---:|"]
    by = defaultdict(list)
    for r in rows:
        by[faixa_total(pred_total(r))].append(r)
    for k in ("0-399", "400-519", "520-639", "640-759", "760-879", "880-1000"):
        rs = by.get(k, [])
        if rs:
            L.append(f"| {k} | {len(rs)} | {media([r['erro_total'] for r in rs]):+.0f} | {media([r['erro_abs_total'] for r in rs]):.0f} |")

    L += ["", "## Erro por competência (viés médio)", "", "| Comp | viés |", "|---|---:|"]
    for c in COMPS:
        L.append(f"| {c.upper()} | {media([r[f'{c}_pred'] - r[f'{c}_humano'] for r in rows]):+.0f} |")

    for label, pred in (("total_pred_central >= 800", lambda r: pred_total(r) >= 800),
                        ("C5 alta (>=160)", lambda r: r["c5_pred"] >= 160),
                        ("C3 alta (>=160)", lambda r: r["c3_pred"] >= 160)):
        rs = [r for r in rows if pred(r)]
        L += ["", f"## {label}"]
        if rs:
            L += [f"n={len(rs)} · viés={media([r['erro_total'] for r in rs]):+.0f} · EAM={media([r['erro_abs_total'] for r in rs]):.0f}"]
        else:
            L += ["n=0"]

    L += ["", "## Padrões de inflação"]
    infl = sorted([r for r in rows if r["erro_total"] >= 160], key=lambda r: r["erro_total"], reverse=True)[:10]
    if infl:
        for r in infl:
            flags = ", ".join([f for f in FLAGS if r.get(f)]) or "sem flags"
            L.append(f"- id {r['id']} ({r['tema'][:40]}): +{r['erro_total']} · pred {r['total_pred_bruto']} vs humano {r['total_humano']} · {flags}")
    else:
        L.append("- Nenhum caso com inflação >=160.")

    L += ["", "## Padrões de deflação"]
    deff = sorted([r for r in rows if r["erro_total"] <= -160], key=lambda r: r["erro_total"])[:10]
    if deff:
        for r in deff:
            flags = ", ".join([f for f in FLAGS if r.get(f)]) or "sem flags"
            L.append(f"- id {r['id']} ({r['tema'][:40]}): {r['erro_total']} · pred {r['total_pred_bruto']} vs humano {r['total_humano']} · {flags}")
    else:
        L.append("- Nenhum caso com deflação <=-160.")

    L += ["", "## Recomendações concretas de ajuste da central", ""]
    hi = [r for r in rows if 800 <= r["total_pred_bruto"] <= 1000]
    if hi and media([r["erro_total"] for r in hi]) > 40:
        L.append("- Centrais >=800 ainda inflam: aplicar redução empírica de 40–80 quando C5/C3 não forem inequivocamente 200.")
    mid = [r for r in rows if 520 <= r["total_pred_bruto"] < 760]
    if mid and media([r["erro_total"] for r in mid]) > 40:
        L.append("- Faixa 520–759 infla: reduzir 40 quando houver repertório genérico ou argumentação genérica.")
    if any(r.get("proposta_incompleta") and r["total_pred_bruto"] >= 760 and r["erro_total"] > 0 for r in rows):
        L.append("- Se total bruto 760+ e proposta incompleta, reduzir 80 (ou mais se C5<=120).")
    if not L[-1].startswith("-"):
        L.append("- Histórico ainda pequeno: manter regras conservadoras e acumular mais validações.")

    CALIBRACAO.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"OK: {CALIBRACAO.relative_to(RAIZ)}", file=sys.stderr)


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
    pe = sub.add_parser("export-history", help="anexa respostas+gabarito limpos ao histórico JSONL")
    pe.add_argument("--seed", type=int, required=True)
    pe.set_defaults(func=export_history)
    pc = sub.add_parser("calibrate", help="gera relatório empírico de calibração do total")
    pc.set_defaults(func=calibrate)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
