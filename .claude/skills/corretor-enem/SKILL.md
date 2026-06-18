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
- `referencia/calibracao_humildade.md` — travas anti-inflação, confiança alta rara, faixas prováveis; consultar antes de fechar central/faixa/confiança.
- `referencia/calibrador_total.md` — regras empíricas para ajustar a **nota central** a partir da soma bruta C1–C5 e flags do texto.
- `referencia/auditoria_extremos.md` — auditoria dos erros extremos: por que o corretor infla texto rebuscado vazio (creditar C3/C4 por forma) e deflaciona argumento forte/proposta fraca (halo reverso + drift de C5). Consultar antes de fechar a calibração.
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

2. **Modo de correção.** Padrão = `modo_treino`.
   - `modo_treino` (padrão): **não para por anulação**. Se houver fuga ao tema,
     tipo inadequado, texto insuficiente, desconexão/ininteligibilidade,
     identificação ou outra hipótese grave, criar bloco **Alerta de risco** e
     corrigir normalmente C1–C5. A nota final se chama **nota pedagógica
     estimada**.
   - `modo_banca`: usar **apenas se o usuário pedir explicitamente**. Nesse modo,
     o gate é bloqueante; se cair em anulação oficial, parar e emitir só nota 0.

   Em ambos os modos, verificar antes:
   - **Fuga total ao tema** — o assunto do texto corresponde ao **tema dado**?
     Tema dado é soberano. Em treino, alertar; em banca, zerar.
   - **Não atende ao tipo dissertativo-argumentativo** (predomínio de narração,
     descrição, poema, carta, etc.).
   - **Texto insuficiente** — regra oficial: até 7 linhas. Trechos copiados dos
     motivadores são desconsiderados. Não inventar limite próprio (ex: "<15
     linhas"). Texto curto acima de 7 linhas pode ser penalizado, não zerado.
   - **Texto desconexo / ininteligível** — não permite leitura/compreensão.
   - **Parte deliberadamente desconectada**, identificação no espaço do texto, ou
     outra hipótese de anulação prevista na cartilha do ano.

   Saída em `modo_treino` quando houver risco:
   ```
   ## Alerta de risco
   Risco: <hipótese>
   Evidências no texto: <trechos literais>
   Efeito provável em banca: <pode zerar / derruba competências>
   O que deveria ter sido feito: <caminho correto>
   ```

   Saída em `modo_banca` se anulada:
   ```
   Nota: 0
   Motivo da anulação: <hipótese exata>
   Evidências no texto: <trechos literais>
   O que deveria ter sido feito: <o caminho correto>
   ```

3. **Corrigir competência por competência**, na ordem C1→C5, seguindo a cadeia
   de sub-análises de `metodologia_correcao.md`. Para cada uma:
   - Pensar passo a passo (chain-of-thought) sobre os critérios.
   - Citar **trechos literais** da redação como evidência.
   - Atribuir **um dos 6 níveis** (0/40/80/120/160/200) — nunca intermediário.
   - **Regra anti-halo:** separar julgamento global e julgamento específico.
     Boa tese **não** sobe automaticamente C1/C4/C5. Erros gramaticais **não**
     derrubam automaticamente C2/C3/C5. Cada competência precisa de evidência
     própria no texto.
   - **C1**: pesar mais **padrão recorrente** de norma-padrão (acentuação,
     concordância, regência, pontuação, grafia) que aparece várias vezes. Erro
     isolado/typo não derruba muito; reincidência sim.
   - **C2**: checar se o repertório é **legítimo** (conferir em `repertorio.md`
     ou `amostra.py --busca`) e **articulado**; genérico/inventado derruba (e em
     2025 penaliza 2 competências).
   - **C5**: contar explicitamente os 5 elementos (ação, agente, modo/meio,
     efeito, detalhamento); cuidado com agente nulo. Em 2025, **sem *ação*
     explícita não passa de 80**.
   - **Calibração do piso (0–400) — sem nota de consolo, sem zerar em treino.**
     Redação muito fraca leva nota pedagógica baixa de verdade. Texto curto que
     NÃO anula ainda assim é penalizado por desenvolvimento raso. Puxar pra baixo
     (faixa 0–400) quando houver vários de: **tese ausente/confusa**,
     **argumentação embrionária**, **repertório solto**, **proposta incompleta**,
     **coesão mínima**, **desenvolvimento muito curto**. Não dar ~360 automático
     a redação rasa — vários desses sinais juntos = ~80–240.

4. **Sanity-check do total (reduzir variância sem piorar competência).** Depois
   de atribuir C1–C5, revisar a soma final antes de fechar:
   - Se **3+ competências** foram empurradas pra cima pela mesma impressão geral
     (ex: texto parece "bom"), revisar pra evitar inflação.
   - Se **3+ competências** foram empurradas pra baixo por uma impressão geral
     ruim (ex: muitos erros gramaticais), revisar pra evitar punição em cascata.
   - Perguntar: "cada competência tem evidência própria?" Se não, ajustar.
   - Não mexer por estética geral; mexer só quando a nota de uma competência não
     tem prova textual suficiente.
   - Registrar no laudo se o sanity-check corrigiu inflação ou punição excessiva.

5. **Calibrar a nota central.** A soma C1–C5 é a **nota bruta**, não a nota final.
   Antes de fechar, consultar `referencia/calibrador_total.md` **e
   `referencia/auditoria_extremos.md`** (regras finas F1–F8: não derrubar C2/C3
   por C5 fraca; não creditar C3/C4 por forma/conectivo; marcar drift de C5 do
   corpus), marcar as flags aplicáveis (texto_curto, paragrafo_unico,
   repertorio_generico, proposta_incompleta, argumentacao_generica, coesao_basica,
   c1_recorrente, risco_superestimacao) e aplicar ajuste empírico (-XX/+XX/0). Exibir no laudo:
   `Nota bruta`, `Calibração da central`, `ajuste aplicado`, `motivo` e `nota
   central calibrada`. A nota exibida no topo é a **central calibrada**.

6. **Definir faixa provável e confiança (calibração de humildade).** Consultar
   `referencia/calibracao_humildade.md` antes de fechar. Não tentar vender nota
   exata: usar a nota central calibrada e comunicar incerteza.
   - **Confiança padrão = média.**
   - **Confiança alta é rara** e só pode ser usada se TODAS as condições forem
     satisfeitas: tema informado; texto completo; estrutura ENEM nítida; C1 sem
     padrão recorrente de erro; C2 com repertório legítimo/produtivo; C3 com
     projeto claro e desenvolvimento consistente; C4 variada e funcional; C5
     completa; nenhuma competência depende de interpretação generosa; nenhuma
     evidência fraca. Se faltar qualquer item, NÃO usar alta.
   - **Confiança média**: caso padrão; há alguma ambiguidade ou variação provável
     de banca, mas o texto é avaliável com segurança razoável.
   - **Confiança baixa**: tema pouco claro, texto muito curto, repertório duvidoso,
     argumentação confusa, risco de fuga/tangenciamento, ou nota central muito
     sensível a poucos trechos.
   - Faixas: **alta ±100**, **média ±160**, **baixa ±240**, limitadas a 0–1000.
   - Por competência, faixa provável padrão = nota central ±40 (alta), ±80
     (média/baixa), limitada a 0–200.
   - **Trava 760/640:** se houver 2+ sinais de superficialidade (argumentação
     genérica, repertório pouco articulado, tese previsível, proposta genérica,
     coesão básica, desenvolvimento curto, períodos vagos, pouca causa/consequência),
     central não passa de 760 sem justificativa forte; com 3+ sinais, não passa de
     640 sem justificativa muito forte.
   - **Trava 800/880/920:** texto bonito/organizado não é automaticamente 880+.
     Para 800+, exigir repertório produtivo, C3 consistente e C5 não genérica. Para
     880+, exigir C5 completa operacional, C1 forte, C4 funcional, dois
     desenvolvimentos suficientes. 920+ só padrão-ouro, sem leitura generosa.

7. **Calibrar com exemplos** consultando o banco `corpus.db` (uso normal; NÃO usar durante validação cega):
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

8. **Fechar a nota central calibrada, faixa provável, confiança e relatório** no formato abaixo.

## Formato de saída

**Modo treino (padrão):** sempre usar a tabela abaixo. Se houver risco de
anulação, inserir antes dela o bloco `## Alerta de risco`; não parar a correção.

**Modo banca (só se pedido explicitamente):** se anulada no gate, emitir apenas
`Nota: 0 / Motivo / Evidências / O que deveria ter sido feito` — não usar a
tabela abaixo.

```
# Correção — <tema>
Modo: treino
Regra aplicada: ENEM <ano vigente> (ver regras_por_ano.md)

Nota central estimada: XXX/1000
Faixa provável: XXX–XXX
Confiança: baixa/média/alta

| Competência | Nota central | Faixa provável | Principal motivo |
| ----------- | ------------ | -------------- | ---------------- |
| C1 — Norma padrão            | XXX | XXX–XXX | <motivo curto> |
| C2 — Tema/tipo textual       | XXX | XXX–XXX | <motivo curto> |
| C3 — Projeto de texto        | XXX | XXX–XXX | <motivo curto> |
| C4 — Coesão                  | XXX | XXX–XXX | <motivo curto> |
| C5 — Proposta de intervenção | XXX | XXX–XXX | <motivo curto> |

## Nota bruta
Soma inicial C1–C5: XXX

## Calibração da central
Ajuste aplicado: -XX / +XX / 0
Motivo do ajuste: <regra de calibrador_total.md + evidência>
Nota central calibrada: XXX

## Diagnóstico principal
<1–3 frases: maior gargalo de nota + maior força do texto>

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

## Trecho reescrito
<pegar a competência de MENOR nota; reescrever o trecho mais problemático como
modelo e explicar em 1–2 linhas o que mudou e por que sobe de nível>

## Sanity-check do total
<informar se houve ajuste: "corrigiu inflação", "corrigiu punição excessiva" ou "sem ajuste"; citar qual competência mudou e a evidência>

## Checagem de superestimação
<obrigatória se central 800+: responder: por que não seria apenas 680–760? o que justifica passar de 800? há competência avaliada com generosidade? Se a resposta for fraca, baixar central ou confiança antes de fechar.>

## Como subir de faixa
<3–5 ações concretas e priorizadas — o que daria mais pontos primeiro>

## Plano de treino para a próxima redação
<2–4 exercícios concretos para praticar antes da próxima redação>

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
