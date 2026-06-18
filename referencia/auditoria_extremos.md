# Auditoria dos erros extremos (seed 6 + histórico)

Consultar **antes de fechar a calibração da nota central** (passo 5 da skill),
junto com `calibrador_total.md` e `calibracao_humildade.md`. Objetivo: não
repetir os dois erros sistemáticos medidos na validação.

## Tabela dos casos extremos

Humano = nota da banca (corpus). Meu = nota cega da seed 6 (ou histórico).
Δ por competência = meu − humano.

| id | tema | humano C1–C5 (tot) | meu C1–C5 (tot) | Δ por comp | Δtotal | causa principal | tipo |
|---|---|---|---|---|---|---|---|
| 7064 | Pedra angular no tráfico | 80/80/0/0/0 (160) | 160/120/120/120/120 (640→600) | +80/+40/+120/+120/+120 | **+440** | creditei C3/C4/C5 em texto sem projeto/coesão/proposta | inflação por forma (C3+C4+C5) + halo |
| 110 | A ciência na era da pós-verdade | 80/40/0/0/0 (120) | 120/80/80/120/40 (440) | +40/+40/+80/+120/+40 | **+320** | conectivo formal ("Conclui-se") lido como coesão | inflação por forma (C4+C3) |
| 6645 | Um fenômeno comum países ricos/pobres | 80/80/0/0/0 (160) | 80/120/120/80/40 (440) | 0/+40/+120/+80/+40 | **+280** | texto conversacional sem projeto, creditei C3 | inflação por forma (C3) |
| 3107 | Porte de armas pela população civil | 120/200/200/200/200 (920) | 120/120/120/120/40 (520) | 0/−80/−80/−80/−160 | **−400** | subestimei C2/C3/C4 (bem argumentado) + C5=200 humano sem proposta canônica | sub-leitura C2/C3/C4 + drift C5 + halo reverso |
| 3079 | Porte de armas pela população civil | 120/160/160/200/200 (840) | 160/160/120/120/40 (600) | +40/0/−40/−80/−160 | **−240** | subestimei C4; C5=200 humano sem proposta canônica | sub-leitura C4 + drift C5 |
| 3106 | Porte de armas pela população civil (hist) | 120/200/200/200/200 (920) | 160/160/160/160/120 | +40/−40/−40/−40/−80 | −160 | mesma onda: sub-leitura C2/C3/C4 + drift C5 | sub-leitura + drift C5 |
| 3464 | A ciência na era da pós-verdade (hist) | 160/160/120/160/120 (720) | 120/120/120/120/80 (560) | −40/−40/0/−40/−40 | −160 | deflação geral leve de texto decente | sub-leitura |

Leitura: **inflação** vem de creditar C3/C4 por forma (parágrafo + conectivo),
quando a banca viu **zero arquitetura argumentativa**. **Deflação** vem de
sub-ler C2/C3/C4 em texto realmente argumentado + **drift de C5** do corpus
pré-2025.

## Inflação: texto rebuscado mas vazio

### Padrões observados
- Nos 3 casos a banca deu **C3 = C4 = 0** e C5 = 0. Sobrou só C1/C2 (40–80).
- Eu dei C3 80–120 e C4 80–120 porque o texto **parecia** dissertativo: tem
  parágrafos, tem "Dessa forma / Em virtude / Conclui-se", tem vocabulário culto.
- A forma me enganou: confundi **formato** com **projeto de texto** (C3) e
  **conectivo presente** com **coesão funcional** (C4).

### Exemplos concretos
- **7064**: "passa-se a considerar os usuários como parcela fundamental... onde
  prevalece-se a lei da oferta e da procura" — frase abstrata, sem causa/efeito
  concreto, sem dado, sem agente. Banca: C3=0, C4=0.
- **110**: lista "a terra, vacinas, vírus de HIV e espécies" sem desenvolver
  nenhum; "Conclui-se que a ciência jamais será ignorada" — conclusão vazia.
  Banca: C3=0, C4=0.
- **6645**: "Acredito que um dos grandes desafio..." — opinião conversacional
  repetida em cada parágrafo, sem progressão. Banca: C3=0, C4=0.

### Sinais objetivos de "parece bom, mas é fraco"
1. Frase abstrata sem sujeito concreto do problema (quem? onde? quando?).
2. Vocabulário formal/raro **sem** dado, exemplo nomeado ou causa→efeito explícita.
3. Parágrafos que reafirmam a mesma opinião com sinônimos — sem argumento novo.
4. Conectivos ligando frases que **não progridem** (coesão protocolar → C4 baixa).
5. Repertório citado sem explicar **como** sustenta o ponto (decorativo).
6. Conclusão sem agente+ação+meio+efeito (proposta genérica/ausente).
7. Texto curto (2–3 parágrafos) com muita adjetivação e pouca evidência.

### Regras para não inflar C2/C3/C4
- **C3**: só dá 120+ se houver progressão real — tese → argumento com
  causa/consequência **concreta** → fechamento. Sem isso, C3 ≤ 80, mesmo com
  parágrafos bonitos. Texto que só repete opinião: C3 pode ser 0–40.
- **C4**: conectivo presente **não** garante nota. Avaliar se há encadeamento
  referencial real entre períodos/parágrafos. Conectivo formal sobre frases
  soltas = coesão protocolar → C4 baixa.
- **C2**: repertório só citado (nome do filósofo/lei, sem explicar a conexão
  material) não sobe C2 acima de 120. Aparência culta ≠ repertório produtivo.
- Antes de fechar: "se eu apagar os conectivos e o vocabulário difícil, ainda
  sobra argumento?" Se não, baixar C3/C4.

## Deflação: argumento forte com C5/proposta problemática

### Padrões observados
- "Porte de armas pela população civil" (3107, 3079, 3106): banca deu
  **C2/C3/C4 = 160–200 e C5 = 200**, mesmo quando a conclusão **não** traz
  proposta canônica de 5 elementos.
- Dois erros se somaram do meu lado:
  1. **Sub-leitura de C2/C3/C4**: dei 120 onde o texto sustentava 160–200
     (argumentação com dado: Estatuto do Desarmamento, OMS 10/100 mil, 70% dos
     homicídios). Texto realmente bem construído.
  2. **Halo reverso**: a impressão de "proposta fraca" me fez derrubar C2/C3
     junto (em 3107 dei C2=120 vs humano 200).
- **C5 = 200 sem proposta de 5 elementos** é **drift do corpus pré-2025**, não
  acerto do humano pela régua 2025.

### Quando C5 deve afetar só C5
- Proposta ausente/genérica/incompleta, mas **desenvolvimento** tem projeto
  claro e progressão: penalizar **só C5**. C2/C3/C4 seguem a evidência do
  desenvolvimento.

### Quando C5 indica problema global
- A falta de proposta vem junto de desenvolvimento sem projeto (sem tese
  sustentada, sem causa/consequência) → aí C3 também cai, mas por **falta de
  projeto no desenvolvimento**, não por causa da conclusão.

### Como não derrubar C2/C3 por causa de proposta fraca
- Julgar C2/C3/C4 **antes** de olhar a proposta, com trecho citado.
- Se C2/C3 têm evidência textual forte, **manter** mesmo com C5 baixa.
- Registrar no laudo: "C5 baixa não rebaixou C2/C3 — ambas têm prova própria".

### Alertas de drift Essay-BR / corpus antigo vs regra atual
- O corpus é **pré-2025**. Em C5, vários textos receberam 160–200 **sem** os 5
  elementos exigidos hoje. Isso infla a referência humana de C5.
- **Para uso pessoal ENEM atual: seguir a cartilha 2025**, não o corpus. Na
  régua 2025, sem **ação** explícita C5 não passa de 80; proposta sem
  agente/meio/efeito/detalhamento não chega a 200.
- Ao comparar com o corpus e ver C5 alto sem proposta canônica: marcar
  **"drift de corpus"** no laudo, não tratar como erro do corretor.
- Drift afeta principalmente **C5** (e em parte C2/C4). C3 forte do corpus
  costuma ser argumentação real — esse sinal vale seguir.
