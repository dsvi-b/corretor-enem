# Calibrador empírico da nota central

Usar depois de atribuir C1–C5. A soma inicial é **nota bruta**. A nota exibida
no topo é **nota central calibrada**.

Base: validações seed 4 e seed 5. Observação forte: PAA por competência bom,
mas erro total aparece quando pequenos erros se acumulam. O calibrador corrige a
central sem mexer muito nas competências.

## Procedimento obrigatório

1. Calcular `nota_bruta = C1+C2+C3+C4+C5`.
2. Checar flags: texto_curto, paragrafo_unico, repertorio_generico,
   proposta_incompleta, argumentacao_generica, coesao_basica, c1_recorrente,
   central_800_mais, risco_superestimacao.
3. Aplicar ajustes abaixo (somar no máximo 2 ajustes principais; evitar
   overfitting). Arredondar para múltiplo de 40.
4. Exibir:
   - `Nota bruta`;
   - `Calibração da central` (ajuste, motivo, central calibrada);
   - faixa provável calculada sobre a **central calibrada**.

## Regras empíricas

### 1) Bruto 800–880 com C5 fraca
Se `nota_bruta` entre 800 e 880 **e C5 <= 120**, reduzir **80**.
Motivo: validações mostram inflação quando texto tem bom corpo, mas proposta
incompleta/genérica.

### 2) Bruto 760–880 com repertório + argumentação genéricos
Se `nota_bruta` entre 760 e 880 e houver `repertorio_generico` +
`argumentacao_generica`, reduzir **80**.
Se apenas um dos dois estiver presente, reduzir **40**.

### 3) Bruto 520–760 com superficialidade acumulada
Se `nota_bruta` entre 520 e 760 e houver 3+ flags entre:
`repertorio_generico`, `argumentacao_generica`, `proposta_incompleta`,
`coesao_basica`, `texto_curto`, `paragrafo_unico`, reduzir **40–80**.
Use -80 se houver `proposta_incompleta` ou `paragrafo_unico`.

### 4) Parágrafo único / desenvolvimento muito curto
Se a redação é `paragrafo_unico` ou tem desenvolvimento muito curto, aplicar teto
pedagógico de **640**, salvo se o texto tiver repertório produtivo e proposta
bem operacional.

### 5) C1 baixo não derruba tudo sozinho
Se C1 <= 120, mas C2/C3/C5 são fortes (>=160) e há projeto claro, **não reduzir
a central** só por erro gramatical. Manter ajuste 0 ou até +40 se o total foi
puxado para baixo por efeito halo.

### 6) Bruto >=800 exige prova explícita
Antes de manter central >=800, exigir:
- C5 operacional;
- repertório produtivo;
- desenvolvimento suficiente;
- C1 sem padrão recorrente grave;
- coesão funcional.

Se 1 item for duvidoso: reduzir **40** ou manter central, mas confiança média.
Se 2+ itens forem duvidosos: reduzir **80**.

### 7) Bruto >=920 é raríssimo
Se `nota_bruta >= 920`, só manter se todos os itens da regra 6 forem inequívocos.
Caso contrário, reduzir para **840–880**.

### 8) Bruto baixo com boa estrutura
Se `nota_bruta <= 520`, mas o texto tem tese clara, 2 argumentos reconhecíveis e
proposta com pelo menos 3 elementos, pode aumentar **+40**. Não subir acima de
600 sem repertório produtivo.

## Sinais práticos das flags

- `texto_curto`: 1–2 parágrafos ou desenvolvimento insuficiente para sustentar
  tese (não confundir com anulação oficial).
- `paragrafo_unico`: texto em bloco único ou quase único.
- `repertorio_generico`: "segundo pesquisas", citação sem fonte, filósofo usado
  sem conexão material.
- `proposta_incompleta`: faltam meio/efeito/detalhamento ou agente vago.
- `argumentacao_generica`: só afirma problema, sem explicar causa/consequência.
- `coesao_basica`: conectivos simples/repetidos, pouco encadeamento real.
- `c1_recorrente`: padrão de desvios repetidos, não typo isolado.
- `risco_superestimacao`: texto parece bonito/organizado, mas evidências de C2/C3/C5
  não sustentam 800+.

## Exemplos observados

- Seed 5: viés caiu para +11 com humildade; centrais >=800 ainda tinham viés +27.
- Seed 4: confiança alta falhou (alta capturou 20%); por isso confiança alta deve
  permanecer rara.
- Id 9920 (agrotóxicos): central 520 vs humano 280 — parágrafo único e proposta
  genérica; regra 3/4 reduziria.
