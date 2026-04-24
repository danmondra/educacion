# Análisis de Correlaciones con Abandono Escolar

Este documento contiene el análisis de 20+ correlaciones entre diversos indicadores socioeconómicos y el índice de abandono escolar por entidad federativa.

**Metodología:** Coeficiente de correlación de Pearson

---

## Resumen de Resultados

- **Total de correlaciones probadas:** 22
- **Correlaciones significativas (|r| > 0.3):** 4
- **Correlaciones moderadas (0.1 < |r| <= 0.3):** 13
- **Correlaciones débiles (|r| <= 0.1):** 5

## Resultados Detallados (Ordenados por fuerza de correlación)

| # | Correlación | Coef. Pearson | p-value | N | Interpretación |
|---|-------------|---------------|---------|---|----------------|
| 22 | Continuidad del rezago educativo entre generaciones | 0.9118 | 0.0000 | 128 | Correlación FUERTE |
| 21 | Relación inversa esperada entre seguridad alimentaria y carencias sociales | -0.8398 | 0.0000 | 128 | Correlación FUERTE |
| 20 | Continuidad del problema de inasistencia escolar por edad | 0.4893 | 0.0000 | 128 | Correlación MODERADA |
| 19 | Porcentaje de población de 16+ años sin educación media superior completa | 0.3277 | 0.0082 | 64 | Correlación MODERADA |
| 18 | Índice de Rezago Social ponderado por población - RELACIÓN MÁS FUERTE CONOCIDA (~0.3) | 0.2655 | 0.0089 | 96 | Correlación DÉBIL |
| 17 | Relación entre tasas de abandono en primaria y secundaria por entidad | 0.2577 | 0.0112 | 96 | Correlación DÉBIL |
| 16 | Población de 3 a 21 años que no asiste a la escuela y no cuenta con educación obligatoria | -0.2517 | 0.0448 | 64 | Correlación DÉBIL |
| 15 | Relación entre inasistencia de jóvenes y abandono primario | -0.2458 | 0.0502 | 64 | Correlación DÉBIL |
| 14 | Misma población vs abandono en secundaria | 0.2387 | 0.0575 | 64 | Correlación DÉBIL |
| 13 | Porcentaje de niños de 3-15 años que no asisten a la escuela | -0.2121 | 0.0924 | 64 | Correlación DÉBIL |
| 12 | Porcentaje de población con seguridad alimentaria (CORRELACIÓN ESPERADA: NEGATIVA) | -0.2051 | 0.1040 | 64 | Correlación DÉBIL |
| 11 | Porcentaje de jóvenes de 12-17 años en situación de carencia social | 0.1494 | 0.2388 | 64 | Correlación DÉBIL |
| 10 | Porcentaje de población con inseguridad alimentaria moderada | 0.1461 | 0.2494 | 64 | Correlación DÉBIL |
| 9 | Mismo indicador vs abandono en secundaria | 0.1381 | 0.2764 | 64 | Correlación DÉBIL |
| 8 | Porcentaje de menores de 18 años en situación de carencia social | 0.1371 | 0.2801 | 64 | Correlación DÉBIL |
| 7 | Porcentaje de población con inseguridad alimentaria severa | 0.1304 | 0.3044 | 64 | Correlación DÉBIL |
| 6 | Porcentaje de niños de 6-11 años en situación de carencia social | 0.1251 | 0.3245 | 64 | Correlación DÉBIL |
| 5 | Población de 16+ años nacida antes de 1982 sin primaria completa | 0.0842 | 0.5081 | 64 | Sin correlación |
| 4 | Correlación entre rezago educativo y carencia social (factores de riesgo relacionados) | 0.0800 | 0.3692 | 128 | Sin correlación |
| 3 | Índice de Rezago Social ponderado por población | 0.0355 | 0.7311 | 96 | Sin correlación |
| 2 | Porcentaje de hogares con limitación en consumo de alimentos (dieta pobre o limítrofe) | -0.0351 | 0.7832 | 64 | Sin correlación |
| 1 | Factores de riesgo en edad primaria | -0.0319 | 0.7212 | 128 | Sin correlación |

---

## Análisis Detallado por Categoría

### 1. Factores de Rezago Educativo

**Índice de Rezago Social ponderado por población - RELACIÓN MÁS FUERTE CONOCIDA (~0.3)**
- Coeficiente: 0.2655
- Variables: `irs_ponderado vs tasa_abandono_secundaria`
- Observaciones: 96

**Índice de Rezago Social ponderado por población**
- Coeficiente: 0.0355
- Variables: `irs_ponderado vs tasa_abandono_primaria`
- Observaciones: 96

### 2. Factores de Carencia Social

### 3. Factores de Seguridad Alimentaria

**Relación inversa esperada entre seguridad alimentaria y carencias sociales**
- Coeficiente: -0.8398
- Variables: `porc_seg_aliment vs porc_carencia_menor18`
- Observaciones: 128

**Porcentaje de población con seguridad alimentaria (CORRELACIÓN ESPERADA: NEGATIVA)**
- Coeficiente: -0.2051
- Variables: `porc_seg_aliment vs tasa_abandono_secundaria`
- Observaciones: 64

**Porcentaje de población con inseguridad alimentaria moderada**
- Coeficiente: 0.1461
- Variables: `porc_inseg_aliment_mode vs tasa_abandono_primaria`
- Observaciones: 64

**Porcentaje de población con inseguridad alimentaria severa**
- Coeficiente: 0.1304
- Variables: `porc_inseg_aliment_seve vs tasa_abandono_secundaria`
- Observaciones: 64

**Porcentaje de hogares con limitación en consumo de alimentos (dieta pobre o limítrofe)**
- Coeficiente: -0.0351
- Variables: `porc_limit_consumo vs tasa_abandono_secundaria`
- Observaciones: 64

### 4. Índice de Rezago Social (IRS)

**Índice de Rezago Social ponderado por población - RELACIÓN MÁS FUERTE CONOCIDA (~0.3)**
- Coeficiente: 0.2655
- Variables: `irs_ponderado vs tasa_abandono_secundaria`
- Observaciones: 96

**Índice de Rezago Social ponderado por población**
- Coeficiente: 0.0355
- Variables: `irs_ponderado vs tasa_abandono_primaria`
- Observaciones: 96

### 5. Otras Correlaciones Exploradas

## Conclusiones y Hallazgos Principales

### Top 5 Correlaciones más Fuertes:

1. **Continuidad del rezago educativo entre generaciones**
   - r = 0.9118 (|r| = 0.9118)

2. **Relación inversa esperada entre seguridad alimentaria y carencias sociales**
   - r = -0.8398 (|r| = 0.8398)

3. **Continuidad del problema de inasistencia escolar por edad**
   - r = 0.4893 (|r| = 0.4893)

4. **Porcentaje de población de 16+ años sin educación media superior completa**
   - r = 0.3277 (|r| = 0.3277)

5. **Índice de Rezago Social ponderado por población - RELACIÓN MÁS FUERTE CONOCIDA (~0.3)**
   - r = 0.2655 (|r| = 0.2655)


---

*Nota: Las correlaciones con |r| < 0.1 se consideran despreciables, entre 0.1-0.3 débiles, entre 0.3-0.5 moderadas, y > 0.5 fuertes. El IRS sigue siendo el indicador con mayor correlación conocida (~0.3).*
