# Regras de correção por ano

**Ano vigente: 2025.** Última verificação: 2026-07-21.

A estrutura (5 competências, 0–200 cada, dissertativo-argumentativo) é estável.
O que muda é a **prática de correção** — às vezes sem alterar o texto oficial da
cartilha. Por isso há duas camadas:

- **Oficial** = Cartilha do Participante / Matriz de Referência (fonte primária
  em `manuais_inep/cartilha_2025.txt`).
- **Prática** = orientações aos corretores no ano, às vezes só reportadas pela
  imprensa. Aplicar quando corrigir "como o ENEM daquele ano corrigiu".

> **Manutenção:** revalidar a cada nova edição do ENEM. Atualizar o "ano
> vigente", baixar a nova cartilha em `manuais_inep/`, e registrar o diff aqui.

---

## ⚠️ Drift do corpus de calibração

O `dataset/corpus.db` (Essay-BR base + extended) foi corrigido por humanos sob
regras **anteriores a 2025**. Logo:

- Use-o como calibração **aproximada** (ordem de grandeza, faixa).
- **Espere divergência** justamente em C2, C4 e C5 (os critérios que 2025
  endureceu — ver abaixo). Se a regra 2025 disser nota mais baixa que o exemplo
  do corpus sugere, **seguir 2025** e anotar a divergência no laudo.

---

## 2025 (vigente)

### Oficial (cartilha 2025)
- Descritores das 5 competências **inalterados** em relação a anos recentes
  (texto qualitativo). C5 oficial segue "muito bem elaborada → ausente".
- **Direitos humanos**: proposta que desrespeita DH zera **só a Competência V**,
  não a redação (`cartilha_2025.txt:1618`).
- **Anulação total** (item 4): ≤7 linhas; fuga ao tema / não
  dissertativo-argumentativo; parte deliberadamente desconectada; identificação
  no texto.

### Prática reportada (orientação aos corretores — INEP nega mudança "oficial")
Documentos obtidos pela imprensa (g1 e outros) indicam correção 2025 mais rígida:

- **C4 (coesão)** — passou a ser avaliada por **categorias qualitativas** do uso
  de conectivos ("pontual", "regular", "constante", "expressiva") em vez de
  contagem objetiva de recursos. → Coesão rala/repetitiva derruba mais fácil.
- **C5 (intervenção)** — o elemento **ação** virou praticamente obrigatório:
  sem *ação* explícita, dificilmente passa de **80**; antes a ausência custava
  ~40, agora o impacto chega a ~120. → Priorizar checar *ação* + *agente*.
- **C2 (repertório)** — repertório **genérico ou mal contextualizado** passou a
  penalizar **duas** competências (C2 e a relacionada), não só uma. → Repertório
  solto/decorativo é punido com mais peso.

**Como aplicar em 2025:** usar os descritores oficiais como base, mas, na dúvida
entre dois níveis, **puxar pra baixo** em C2/C4/C5 conforme acima; tornar a
*ação* da proposta condição pra C5 > 80; exigir repertório articulado pra C2 alto.

Fontes: redacaonline.com.br/blog/a-correcao-da-redacao-do-enem-2025-mudou ·
98fmnatal.com.br (critérios mais rígidos 2025) · g1 (docs aos corretores) ·
cartilha oficial INEP 2025.

### Evidência dos microdados 2025 (divulgados em junho de 2026)

Os microdados oficiais confirmaram **variância interavaliador relevante**, em
especial na classificação de repertório de bolso:

- entre as 10 redações com nota final 1000, 4 passaram por correções com
  divergência; esse recorte é selecionado pelo resultado final e **não estima a
  taxa de divergência de todas as redações**;
- em um caso, os dois primeiros avaliadores deram 600 e 760, o terceiro deu 960
  e a banca extraordinária fixou 1000; portanto, não foram dois avaliadores
  individuais dando 600 e 1000;
- em redações que terminaram com 1000, a C2 do mesmo texto variou de **120 a
  200** entre avaliadores oficiais, associada à leitura divergente sobre
  repertório de bolso.

**Como aplicar:** a nota oficial é soberana para seleção e resultado do exame,
mas não deve ser tratada como medida pedagógica sem ruído. Se o texto usar
repertório legítimo, porém abstrato, transferível ou ligado ao tema apenas por
analogia, marcar `fronteira_repertorio_bolso`. Nessa fronteira:

- não conceder C2=200 só pelo prestígio ou pela autenticidade da referência;
- distinguir pertinência direta, contextualização e contribuição causal;
- usar faixa de C2 que comporte até 80 pontos de oscilação quando houver duas
  leituras oficiais plausíveis;
- não concluir que várias correções coincidentes são independentes: humanos de
  cursinho e IAs podem compartilhar o mesmo halo de sofisticação;
- não usar o caso extremo para declarar toda correção aleatória.

Fontes: [microdados do Enem — Inep](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) ·
[levantamento do g1, 26/06/2026](https://g1.globo.com/educacao/noticia/2026/06/26/divergencia-notas-redacao-enem-2025.ghtml).

---

## ≤ 2024 (base do corpus)
- Critérios "clássicos": C4 por presença/diversidade de recursos coesivos
  (contagem), C5 por contagem dos 5 elementos, repertório genérico penaliza
  geralmente só C2. É sob essas regras que as notas do `corpus.db` foram dadas.
- 2024: desrespeito aos DH já zerava apenas C5 (não a redação).
