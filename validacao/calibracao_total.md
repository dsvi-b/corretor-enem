# Calibração empírica da nota total

Casos no histórico: **26**

Erro médio absoluto do total: **94**
Viés médio: **+11**

## Erro por faixa de total_pred_bruto

| Faixa | n | viés | EAM |
|---|---:|---:|---:|
| 0-399 | 6 | -20 | 113 |
| 400-519 | 4 | +30 | 70 |
| 520-639 | 6 | +40 | 133 |
| 640-759 | 3 | +27 | 80 |
| 760-879 | 7 | -6 | 63 |

## Erro por competência (viés médio)

| Comp | viés |
|---|---:|
| C1 | -2 |
| C2 | +14 |
| C3 | +15 |
| C4 | -8 |
| C5 | -9 |

## total_pred_bruto >= 800
n=3 · viés=+27 · EAM=27

## C5 alta (>=160)
n=5 · viés=+32 · EAM=48

## C3 alta (>=160)
n=10 · viés=+4 · EAM=68

## Padrões de inflação
- id 9920 (Efeitos Dos Agrotóxicos No Brasil): +240 · pred 520 vs humano 280 · sem flags
- id 6555 (Viagem sem volta a Marte: pioneirismo ou): +160 · pred 240 vs humano 80 · sem flags

## Padrões de deflação
- id 7033 (Melhorar a educação sem valorizar o prof): -200 · pred 160 vs humano 360 · sem flags
- id 3106 (Porte de armas pela população civil): -160 · pred 760 vs humano 920 · sem flags
- id 3464 (A ciência na era da pós-verdade): -160 · pred 560 vs humano 720 · sem flags
- id 9466 (Gravidez precoce): -160 · pred 360 vs humano 520 · sem flags

## Recomendações concretas de ajuste da central

- Histórico ainda pequeno: manter regras conservadoras e acumular mais validações.
