# Calibração empírica da nota total

Casos no histórico: **61**

Erro médio absoluto do total: **112**
Viés médio: **+30**

## Erro por faixa de total_pred_bruto

| Faixa | n | viés | EAM |
|---|---:|---:|---:|
| 0-399 | 11 | -18 | 98 |
| 400-519 | 11 | +102 | 124 |
| 520-639 | 14 | +29 | 160 |
| 640-759 | 8 | -25 | 95 |
| 760-879 | 17 | +40 | 82 |

## Erro por competência (viés médio)

| Comp | viés |
|---|---:|
| C1 | +6 |
| C2 | +11 |
| C3 | +22 |
| C4 | +2 |
| C5 | -7 |

## total_pred_central >= 800
n=8 · viés=+35 · EAM=55

## C5 alta (>=160)
n=15 · viés=+40 · EAM=77

## C3 alta (>=160)
n=23 · viés=+19 · EAM=85

## Padrões de inflação
- id 7064 (Pedra angular no tráfico): +440 · pred 640 vs humano 160 · repertorio_generico, proposta_incompleta, argumentacao_generica, risco_superestimacao
- id 110 (A ciência na era da pós-verdade): +320 · pred 440 vs humano 120 · repertorio_generico, proposta_incompleta, argumentacao_generica, coesao_basica
- id 6645 (Um fenômeno comum entre países ricos e p): +280 · pred 440 vs humano 160 · proposta_incompleta, argumentacao_generica, coesao_basica, c1_recorrente
- id 9920 (Efeitos Dos Agrotóxicos No Brasil): +240 · pred 520 vs humano 280 · sem flags
- id 8901 (A importância das vacinas para a socieda): +240 · pred 760 vs humano 520 · c1_recorrente
- id 4722 (Debate sobre o marco temporal): +200 · pred 600 vs humano 360 · proposta_incompleta, coesao_basica
- id 6732 (Escravizar): +200 · pred 440 vs humano 240 · repertorio_generico, proposta_incompleta, argumentacao_generica, coesao_basica
- id 6555 (Viagem sem volta a Marte: pioneirismo ou): +160 · pred 240 vs humano 80 · sem flags
- id 124 (Posse de armas: mais segurança ou mais p): +160 · pred 360 vs humano 200 · repertorio_generico, proposta_incompleta, argumentacao_generica, coesao_basica, c1_recorrente
- id 2484 (Reforma da Previdência: uma solução ou u): +160 · pred 880 vs humano 680 · proposta_incompleta, central_800_mais, risco_superestimacao

## Padrões de deflação
- id 3107 (Porte de armas pela população civil): -400 · pred 520 vs humano 920 · proposta_incompleta, argumentacao_generica, c1_recorrente
- id 3079 (Porte de armas pela população civil): -240 · pred 600 vs humano 840 · proposta_incompleta
- id 7033 (Melhorar a educação sem valorizar o prof): -200 · pred 160 vs humano 360 · sem flags
- id 3106 (Porte de armas pela população civil): -160 · pred 760 vs humano 920 · sem flags
- id 3464 (A ciência na era da pós-verdade): -160 · pred 560 vs humano 720 · sem flags
- id 9466 (Gravidez precoce): -160 · pred 360 vs humano 520 · sem flags

## Recomendações concretas de ajuste da central

- Se total bruto 760+ e proposta incompleta, reduzir 80 (ou mais se C5<=120).
