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

## Regras finas por competência (auditoria de extremos)

Estas regras corrigem **a soma bruta** ajustando a leitura das competências —
**não** criam teto bruto automático. Ver `auditoria_extremos.md` para os casos.
Aplicar na atribuição C1–C5, antes de somar.

### F1) C5 fraca afeta só C5
Proposta fraca/incompleta/ausente penaliza **C5**. **Não** derruba C2/C3/C4
automaticamente. (3107/3079: humano deu C2/C3/C4 = 160–200 com proposta não
canônica; eu derrubei tudo por halo reverso.)

### F2) C2/C3 fortes com C5 fraca → manter C2/C3
Se C2/C3 têm evidência textual própria (dado, exemplo nomeado, causa→efeito,
repertório explicado), **manter** mesmo com C5 baixa. Registrar no laudo: "C5
baixa não rebaixou C2/C3 — prova própria". Julgar C2/C3/C4 **antes** de olhar a
proposta.

### F3) Texto rebuscado exige prova de progressão antes de C3 alto
Vocabulário formal não sobe C3. Só dar **C3 >= 120** se houver tese → argumento
com causa/consequência **concreta** → fechamento. Sem progressão real, C3 <= 80
mesmo com parágrafos bem formatados. (7064/110/6645: humano deu C3 = 0.)

### F4) Repertório só citado não sobe C2/C3
Nome de filósofo/lei/pesquisa **sem explicar a conexão material** com o tema é
decorativo: C2 não passa de 120. Aparência culta ≠ repertório produtivo.

### F5) Linguagem formal + pouca análise → limitar C3
Se há período formal mas pouca análise (só afirma, não explica), **limitar C3**.
Teste: "apagando conectivos e palavras difíceis, ainda sobra argumento?" Se não,
baixar C3 (e C4).

### F6) Conectivo presente não garante C4
Conectivo formal sobre frases que não progridem = coesão protocolar → **C4
baixa/zero**. Avaliar encadeamento referencial real, não a presença do conectivo.
(110: humano deu C4 = 0 apesar de "Em uma segunda análise / Conclui-se".)

### F7) Proposta fraca só derruba C3 se o desenvolvimento não tiver projeto
Penalizar **C5** pela proposta. Só baixar **C3** se a falta de proposta vier
junto de desenvolvimento sem projeto (sem tese sustentada, sem causa/consequência)
— problema no **desenvolvimento**, não na conclusão.

### F8) Drift de C5 do corpus (não é acerto humano)
Corpus é pré-2025. Vários textos receberam C5 = 160–200 **sem** os 5 elementos
exigidos hoje. Ao comparar e ver C5 alto sem proposta canônica, marcar **"drift
de corpus"** no laudo. **Para uso ENEM atual, seguir a cartilha 2025**: sem
*ação* explícita C5 não passa de 80.

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
