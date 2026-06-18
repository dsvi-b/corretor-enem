---
name: corretor-enem
description: Corrige redação dissertativo-argumentativa do ENEM nas 5 competências oficiais (0–200 cada, 0–1000 total), com nota por competência, justificativa, trechos citados e feedback acionável. Calibra o julgamento com redações reais já corrigidas por humanos do corpus Essay-BR. Use sempre que o usuário pedir pra corrigir/avaliar/dar nota numa redação do ENEM, soltar um texto de redação na pasta redacoes/, perguntar "quanto tiraria nessa redação", pedir feedback de competência, ou simular correção ENEM. Dispara mesmo sem a palavra "corrigir" — "vê minha redação", "tá boa essa redação?", "qual nota disso" também acionam.
---

# Corretor ENEM — 5 competências

Corretor de redação ENEM rodando no Claude Code. Aplica a rubrica oficial INEP
e a metodologia prompt-driven (decomposição por competência, chain-of-thought,
calibração com exemplos reais) validada no TG UFPE.

## Arquivos de apoio (ler antes de corrigir)

- `referencia/regras_por_ano.md` — **LER PRIMEIRO.** Regra vigente (2025) + o que mudou por ano + drift do corpus. Define como pontuar neste ano.
- `referencia/cartilha_competencias.md` — rubrica oficial, 6 níveis por competência, elementos contáveis (C5), situações que zeram.
- `referencia/manuais_inep/cartilha_2025.txt` — fonte primária INEP (Cartilha do Participante 2025).
- `referencia/metodologia_correcao.md` — roteiro de sub-análises por competência + calibração.
- `referencia/repertorio.md` — banco de repertório legítimo por categoria (checar autenticidade + sugerir).
- `referencia/redacoes_nota_1000/` — exemplos comentados (2021–2025) como padrão-ouro.
- `dataset/corpus.db` — **banco SQLite com 11.147 redações reais** já corrigidas por humanos (Essay-BR base + extended), com nota por competência e índice full-text. Memória empírica de calibração (pré-2025 — ver drift).
- `scripts/amostra.py` — consulta o `corpus.db` (faixa, nível, tema, busca full-text, `--escala`).
- `scripts/validar.py` — harness de auto-validação (mede adjacent agreement vs nota humana).
- `referencia/temas/lista_temas.md` — temas do corpus + categorias.

Se `dataset/corpus.db` não existir, gerar com `python3 scripts/build_db.py`.

## Fluxo de correção

0. **Carregar regra do ano.** Ler `referencia/regras_por_ano.md`: confirmar o
   **ano vigente** (hoje: 2025) e os ajustes de prática (C4 qualitativa; C5 exige
   *ação* pra >80; C2 repertório genérico penaliza 2 competências). O laudo
   **declara** qual ano de regra está aplicando.

1. **Obter a redação.** Da pasta `redacoes/` (arquivo .txt/.md mais recente ou
   o indicado pelo usuário) ou colada na conversa. Pegar também o **tema** — se
   não informado, perguntar OU inferir do conteúdo e confirmar.

2. **Triagem de anulação.** Antes de pontuar: fuga ao tema? não é
   dissertativo-argumentativo? ≤ 7 linhas? identificação no texto? Se sim,
   sinalizar e tratar conforme a cartilha (não inventar nota cheia). Cópia dos
   motivadores não zera, mas os trechos copiados são desconsiderados.

3. **Corrigir competência por competência**, na ordem C1→C5, seguindo a cadeia
   de sub-análises de `metodologia_correcao.md`. Para cada uma:
   - Pensar passo a passo (chain-of-thought) sobre os critérios.
   - Citar **trechos literais** da redação como evidência.
   - Atribuir **um dos 6 níveis** (0/40/80/120/160/200) — nunca intermediário.
   - **C2**: checar se o repertório é **legítimo** (conferir em `repertorio.md`
     ou `amostra.py --busca`) e **articulado**; genérico/inventado derruba (e em
     2025 penaliza 2 competências).
   - **C5**: contar explicitamente os 5 elementos (ação, agente, modo/meio,
     efeito, detalhamento); cuidado com agente nulo. Em 2025, **sem *ação*
     explícita não passa de 80**.

4. **Calibrar** consultando o banco `corpus.db` (11.147 redações reais):
   ```
   python3 scripts/amostra.py --faixa <lo>-<hi> --n 2     # faixa do total estimado
   python3 scripts/amostra.py --escala --comp 4           # régua 0→200 da competência
   python3 scripts/amostra.py --busca "<repertório>" --n 1
   python3 scripts/amostra.py --tema <palavra> --faixa 800-1000 --n 1
   ```
   Comparar com os exemplos reais da mesma faixa/nível. **Atenção ao drift:** o
   corpus é pré-2025 — se a regra 2025 (passo 0) pedir nota menor que o exemplo
   sugere (típico em C2/C4/C5), **seguir 2025** e anotar a divergência. Para o
   teto, `--escala` ou `--faixa 1000-1000`.

5. **Fechar nota e escrever o relatório** no formato abaixo.

## Formato de saída

```
# Correção — <tema>
Regra aplicada: ENEM <ano vigente> (ver regras_por_ano.md)

| Competência | Nota |
|-------------|------|
| C1 — Norma padrão            | XXX |
| C2 — Tema/tipo textual       | XXX |
| C3 — Projeto de texto        | XXX |
| C4 — Coesão                  | XXX |
| C5 — Proposta de intervenção | XXX |
| **TOTAL**                    | **XXXX** |

## C1 — Norma padrão (XXX)
<justificativa do nível, com trechos citados e desvios apontados>

## C2 — Tema e tipo textual (XXX)
<inclui veredito do repertório: legítimo/genérico/inventado, articulado ou não>

## C3 — Projeto de texto (XXX)
<...>

## C4 — Coesão (XXX)
<classificar o uso coesivo: pontual/regular/constante/expressiva — prática 2025>

## C5 — Proposta de intervenção (XXX)
Elementos: ação [✓/✗] · agente [✓/✗] · modo/meio [✓/✗] · efeito [✓/✗] · detalhamento [✓/✗]
<...>

## Redação anotada
<o texto da redação reproduzido com marcação inline:
  [!desvio: explicação]  erro de norma (C1)
  **conectivo**          recurso coesivo (C4)
  [rep: fonte]           repertório usado (C2)
  {C5-ação|agente|meio|efeito|detalhe: trecho}  elementos da proposta>

## Reescrita modelo
<pegar a competência de MENOR nota; reescrever o trecho mais problemático como
modelo e explicar em 1–2 linhas o que mudou e por que sobe de nível>

## Como subir de faixa
<3–5 ações concretas e priorizadas — o que daria mais pontos primeiro>

## Calibração
Comparada com N redações reais do Essay-BR (faixa <x>). Drift pré-2025: <se houve
divergência por regra 2025, anotar aqui>.
```

## Regras

- **Regra do ano vigente manda.** Em conflito entre cartilha clássica, corpus e
  prática 2025, seguir a prática do ano (`regras_por_ano.md`) e anotar.
- **Honestidade de nota.** Não inflar. Nota baixa com caminho de melhoria ajuda
  mais que elogio vazio. Se zeraria, dizer e explicar.
- **Sempre citar trecho** como evidência de cada apontamento — não afirmar no
  vácuo.
- **Adjacência > exatidão.** Acertar a faixa (±80/comp) importa mais que o ponto
  exato; calibrar com exemplos reais reduz viés.
- **Repertório:** na dúvida se é real, conferir (`repertorio.md` / `--busca`);
  não tratar invenção como repertório produtivo.
- Feedback **acionável e priorizado**: o que rende mais ponto primeiro.
- Redação manuscrita (foto): pode-se transcrever via leitura de imagem, mas
  avisar que erros de transcrição não contam como desvio de C1.

## Auto-validação (medir a própria precisão)

Pra checar se as notas reproduzem a humana (adjacent agreement, à la TG UFPE):

1. `python3 scripts/validar.py prepare --n 10 --seed 1` — gera redações cegas em
   `validacao/cegas/` + gabarito oculto.
2. Corrigir **cada** `.txt` de `validacao/cegas/` com este fluxo, **às cegas**
   (NÃO abrir `validacao/gabarito.json`), preenchendo c1–c5 em
   `validacao/respostas.json`.
3. `python3 scripts/validar.py score` — gera `validacao/relatorio.md` com
   PEA/PAA/viés por competência.
4. Se houver viés sistemático (ex: inflar C2), ajustar a leitura da cartilha/skill.
   Lembrar: corpus é pré-2025 → divergência esperada em C2/C4/C5 não é erro, é drift.
