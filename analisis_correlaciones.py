#!/usr/bin/env python3
"""
Script para calcular correlaciones entre diversos indicadores y el abandono escolar.
Usa el coeficiente de correlación de Pearson.
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import os

# Configuración de pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def cargar_datos():
    """Carga los datos consolidados de porcentajes.csv"""
    df = pd.read_csv('fuentes/porcentajes.csv')
    # Eliminar fila de Estados Unidos Mexicanos para análisis por entidad
    df = df[df['estado'] != 'Estados Unidos Mexicanos'].copy()
    return df

def calcular_correlacion(df, var_x, var_y, nombre_correlacion, descripcion):
    """
    Calcula la correlación de Pearson entre dos variables.
    Retorna el coeficiente, p-value y número de observaciones.
    """
    # Filtrar datos donde ambas variables no sean nulas
    datos = df[[var_x, var_y]].dropna()
    
    if len(datos) < 3:
        return {
            'correlacion': np.nan,
            'p_value': np.nan,
            'n': len(datos),
            'descripcion': descripcion,
            'variables': f"{var_x} vs {var_y}"
        }
    
    corr, p_val = pearsonr(datos[var_x], datos[var_y])
    
    return {
        'correlacion': corr,
        'p_value': p_val,
        'n': len(datos),
        'descripcion': descripcion,
        'variables': f"{var_x} vs {var_y}"
    }

def main():
    print("Cargando datos...")
    df = cargar_datos()
    print(f"Datos cargados: {len(df)} registros de {df['estado'].nunique()} entidades")
    
    resultados = []
    
    # ============================================================
    # 1. REZAGO EDUCATIVO Y TASA DE ABANDONO
    # ============================================================
    print("\nCalculando correlaciones de rezago educativo...")
    
    # 1.1 Rezago educativo (3-21 años no asisten) vs Abandono primaria
    r = calcular_correlacion(
        df, 'porc_pob_3_21_no_asist_sin_oblig', 'tasa_abandono_primaria',
        "Rezago educativo (3-21 años que no asisten) vs Tasa abandono primaria",
        "Población de 3 a 21 años que no asiste a la escuela y no cuenta con educación obligatoria"
    )
    resultados.append(r)
    
    # 1.2 Rezago educativo vs Abandono secundaria
    r = calcular_correlacion(
        df, 'porc_pob_3_21_no_asist_sin_oblig', 'tasa_abandono_secundaria',
        "Rezago educativo vs Tasa abandono secundaria",
        "Misma población vs abandono en secundaria"
    )
    resultados.append(r)
    
    # 1.3 Población sin secundaria completa vs Abandono secundaria
    r = calcular_correlacion(
        df, 'porc_pob_16mas_sin_secu', 'tasa_abandono_secundaria',
        "Población sin secundaria completa vs Abandono secundaria",
        "Porcentaje de población de 16+ años sin educación media superior completa"
    )
    resultados.append(r)
    
    # 1.4 Población sin primaria completa vs Abandono primaria
    r = calcular_correlacion(
        df, 'porc_pob_16mas_sin_prim', 'tasa_abandono_primaria',
        "Población sin primaria completa vs Abandono primaria",
        "Población de 16+ años nacida antes de 1982 sin primaria completa"
    )
    resultados.append(r)
    
    # 1.5 Tasa inasistencia 3-15 años vs Abandono primaria
    r = calcular_correlacion(
        df, 'porc_tasa_inasistencia_3_15', 'tasa_abandono_primaria',
        "Tasa de inasistencia (3-15 años) vs Abandono primaria",
        "Porcentaje de niños de 3-15 años que no asisten a la escuela"
    )
    resultados.append(r)
    
    # ============================================================
    # 2. CARENCIA SOCIAL Y ABANDONO
    # ============================================================
    print("Calculando correlaciones de carencia social...")
    
    # 2.1 Carencia menores 18 vs Abandono primaria
    r = calcular_correlacion(
        df, 'porc_carencia_menor18', 'tasa_abandono_primaria',
        "Carencia social menores 18 años vs Abandono primaria",
        "Porcentaje de menores de 18 años en situación de carencia social"
    )
    resultados.append(r)
    
    # 2.2 Carencia menores 18 vs Abandono secundaria
    r = calcular_correlacion(
        df, 'porc_carencia_menor18', 'tasa_abandono_secundaria',
        "Carencia social menores 18 años vs Abandono secundaria",
        "Mismo indicador vs abandono en secundaria"
    )
    resultados.append(r)
    
    # 2.3 Carencia 6-11 años vs Abandono primaria
    r = calcular_correlacion(
        df, 'porc_carencia_6_11', 'tasa_abandono_primaria',
        "Carencia social (6-11 años) vs Abandono primaria",
        "Porcentaje de niños de 6-11 años en situación de carencia social"
    )
    resultados.append(r)
    
    # 2.4 Carencia 12-17 años vs Abandono secundaria
    r = calcular_correlacion(
        df, 'porc_carencia_12_17', 'tasa_abandono_secundaria',
        "Carencia social (12-17 años) vs Abandono secundaria",
        "Porcentaje de jóvenes de 12-17 años en situación de carencia social"
    )
    resultados.append(r)
    
    # ============================================================
    # 3. SEGURIDAD ALIMENTARIA Y ABANDONO
    # ============================================================
    print("Calculando correlaciones de seguridad alimentaria...")
    
    # 3.1 Seguridad alimentaria vs Abandono secundaria (inversa)
    r = calcular_correlacion(
        df, 'porc_seg_aliment', 'tasa_abandono_secundaria',
        "Seguridad alimentaria vs Abandono secundaria",
        "Porcentaje de población con seguridad alimentaria (CORRELACIÓN ESPERADA: NEGATIVA)"
    )
    resultados.append(r)
    
    # 3.2 Inseguridad alimentaria severa vs Abandono secundaria
    r = calcular_correlacion(
        df, 'porc_inseg_aliment_seve', 'tasa_abandono_secundaria',
        "Inseguridad alimentaria severa vs Abandono secundaria",
        "Porcentaje de población con inseguridad alimentaria severa"
    )
    resultados.append(r)
    
    # 3.3 Limitación en consumo de alimentos vs Abandono secundaria
    r = calcular_correlacion(
        df, 'porc_limit_consumo', 'tasa_abandono_secundaria',
        "Limitación en consumo de alimentos vs Abandono secundaria",
        "Porcentaje de hogares con limitación en consumo de alimentos (dieta pobre o limítrofe)"
    )
    resultados.append(r)
    
    # 3.4 Inseguridad alimentaria moderada vs Abandono primaria
    r = calcular_correlacion(
        df, 'porc_inseg_aliment_mode', 'tasa_abandono_primaria',
        "Inseguridad alimentaria moderada vs Abandono primaria",
        "Porcentaje de población con inseguridad alimentaria moderada"
    )
    resultados.append(r)
    
    # ============================================================
    # 4. INTERRELACIONES ENTRE ABANDONO
    # ============================================================
    print("Calculando correlaciones entre niveles de abandono...")
    
    # 4.1 Abandono primaria vs Abandono secundaria
    r = calcular_correlacion(
        df, 'tasa_abandono_primaria', 'tasa_abandono_secundaria',
        "Abandono primaria vs Abandono secundaria (mismo año)",
        "Relación entre tasas de abandono en primaria y secundaria por entidad"
    )
    resultados.append(r)
    
    # ============================================================
    # 5. RELACIONES COMPUESTAS
    # ============================================================
    print("Calculando correlaciones compuestas...")
    
    # 5.1 Rezago educativo vs Carencia social (ambos factores de riesgo)
    r = calcular_correlacion(
        df, 'porc_pob_3_21_no_asist_sin_oblig', 'porc_carencia_menor18',
        "Rezago educativo vs Carencia social",
        "Correlación entre rezago educativo y carencia social (factores de riesgo relacionados)"
    )
    resultados.append(r)
    
    # 5.2 Inasistencia temprana (3-15) vs Inasistencia tardía (16-21)
    r = calcular_correlacion(
        df, 'porc_tasa_inasistencia_3_15', 'porc_tasa_inasistencia_16_21',
        "Inasistencia temprana (3-15 años) vs Inasistencia tardía (16-21 años)",
        "Continuidad del problema de inasistencia escolar por edad"
    )
    resultados.append(r)
    
    # 5.3 Sin primaria completa vs Sin secundaria completa
    r = calcular_correlacion(
        df, 'porc_pob_16mas_sin_prim', 'porc_pob_16mas_sin_secu',
        "Sin primaria completa vs Sin secundaria completa",
        "Continuidad del rezago educativo entre generaciones"
    )
    resultados.append(r)
    
    # 5.4 Seguridad alimentaria vs Carencia social (inversa esperada)
    r = calcular_correlacion(
        df, 'porc_seg_aliment', 'porc_carencia_menor18',
        "Seguridad alimentaria vs Carencia social",
        "Relación inversa esperada entre seguridad alimentaria y carencias sociales"
    )
    resultados.append(r)
    
    # ============================================================
    # 6. CORRELACIONES ESPECÍFICAS DE PRIMARIA
    # ============================================================
    print("Calculando correlaciones específicas de primaria...")
    
    # 6.1 Tasa inasistencia 3-15 vs Carencia 6-11
    r = calcular_correlacion(
        df, 'porc_tasa_inasistencia_3_15', 'porc_carencia_6_11',
        "Inasistencia (3-15 años) vs Carencia social (6-11 años)",
        "Factores de riesgo en edad primaria"
    )
    resultados.append(r)
    
    # 6.2 Rezago educativo vs Abandono (análisis adicional)
    r = calcular_correlacion(
        df, 'porc_tasa_inasistencia_16_21', 'tasa_abandono_primaria',
        "Inasistencia juvenil (16-21) vs Abandono primaria",
        "Relación entre inasistencia de jóvenes y abandono primario"
    )
    resultados.append(r)
    
    # ============================================================
    # 7. CARGAR DATOS ADICIONALES
    # ============================================================
    print("\nCargando datos adicionales...")
    
    # Intentar cargar IRS (Índice de Rezago Social)
    try:
        irs_df = pd.read_csv('fuentes/rezago_social/irs-localidad-2020.csv', encoding='utf-8')
        # Agregar por entidad usando promedio ponderado por población
        irs_estado = irs_df.groupby('entidad_federativa').apply(
            lambda x: np.average(x['irs'], weights=x['poblacion'])
        ).reset_index()
        irs_estado.columns = ['estado', 'irs_ponderado']
        
        # Merge con datos principales
        df_irs = df.merge(irs_estado, on='estado', how='left')
        
        # Correlación IRS vs Abandono
        r = calcular_correlacion(
            df_irs, 'irs_ponderado', 'tasa_abandono_secundaria',
            "Índice de Rezago Social (IRS) 2020 vs Abandono secundaria",
            "Índice de Rezago Social ponderado por población - RELACIÓN MÁS FUERTE CONOCIDA (~0.3)"
        )
        resultados.append(r)
        
        # IRS vs Abandono primaria
        r = calcular_correlacion(
            df_irs, 'irs_ponderado', 'tasa_abandono_primaria',
            "Índice de Rezago Social (IRS) 2020 vs Abandono primaria",
            "Índice de Rezago Social ponderado por población"
        )
        resultados.append(r)
        
    except Exception as e:
        print(f"No se pudo cargar IRS: {e}")
    
    # ============================================================
    # GUARDAR RESULTADOS
    # ============================================================
    print("\nGuardando resultados...")
    
    # Crear DataFrame de resultados
    resultados_df = pd.DataFrame(resultados)
    
    # Ordenar por valor absoluto de correlación (de mayor a menor)
    resultados_df['abs_correlacion'] = resultados_df['correlacion'].abs()
    resultados_df = resultados_df.sort_values('abs_correlacion', ascending=False)
    
    # Generar reporte en markdown
    with open('ideas.md', 'w', encoding='utf-8') as f:
        f.write("# Análisis de Correlaciones con Abandono Escolar\n\n")
        f.write("Este documento contiene el análisis de 20+ correlaciones entre diversos indicadores ")
        f.write("socioeconómicos y el índice de abandono escolar por entidad federativa.\n\n")
        f.write("**Metodología:** Coeficiente de correlación de Pearson\n\n")
        f.write("---\n\n")
        
        # Resumen
        f.write("## Resumen de Resultados\n\n")
        f.write(f"- **Total de correlaciones probadas:** {len(resultados)}\n")
        f.write(f"- **Correlaciones significativas (|r| > 0.3):** {len(resultados_df[resultados_df['abs_correlacion'] > 0.3])}\n")
        f.write(f"- **Correlaciones moderadas (0.1 < |r| <= 0.3):** {len(resultados_df[(resultados_df['abs_correlacion'] > 0.1) & (resultados_df['abs_correlacion'] <= 0.3)])}\n")
        f.write(f"- **Correlaciones débiles (|r| <= 0.1):** {len(resultados_df[resultados_df['abs_correlacion'] <= 0.1])}\n\n")
        
        # Tabla de resultados ordenados
        f.write("## Resultados Detallados (Ordenados por fuerza de correlación)\n\n")
        f.write("| # | Correlación | Coef. Pearson | p-value | N | Interpretación |\n")
        f.write("|---|-------------|---------------|---------|---|----------------|\n")
        
        for i, row in resultados_df.iterrows():
            corr_val = row['correlacion']
            if pd.isna(corr_val):
                interpretacion = "Sin datos suficientes"
                corr_str = "N/A"
                p_str = "N/A"
            else:
                abs_corr = abs(corr_val)
                if abs_corr > 0.5:
                    interpretacion = "Correlación FUERTE"
                elif abs_corr > 0.3:
                    interpretacion = "Correlación MODERADA"
                elif abs_corr > 0.1:
                    interpretacion = "Correlación DÉBIL"
                else:
                    interpretacion = "Sin correlación"
                
                corr_str = f"{corr_val:.4f}"
                p_str = f"{row['p_value']:.4f}" if not pd.isna(row['p_value']) else "N/A"
            
            f.write(f"| {len(resultados) - list(resultados_df.index).index(i)} | {row['descripcion']} | {corr_str} | {p_str} | {row['n']} | {interpretacion} |\n")
        
        f.write("\n---\n\n")
        
        # Análisis detallado
        f.write("## Análisis Detallado por Categoría\n\n")
        
        # Categoría: Rezago Educativo
        f.write("### 1. Factores de Rezago Educativo\n\n")
        for i, row in resultados_df.iterrows():
            if 'Rezago' in row['descripcion'] or 'Sin secundaria' in row['descripcion'] or 'Sin primaria' in row['descripcion'] or 'Inasistencia' in row['descripcion']:
                f.write(f"**{row['descripcion']}**\n")
                corr_str = f"{row['correlacion']:.4f}" if not pd.isna(row['correlacion']) else 'N/A'
                f.write(f"- Coeficiente: {corr_str}\n")
                f.write(f"- Variables: `{row['variables']}`\n")
                f.write(f"- Observaciones: {row['n']}\n\n")
        
        # Categoría: Carencia Social
        f.write("### 2. Factores de Carencia Social\n\n")
        for i, row in resultados_df.iterrows():
            if 'Carencia' in row['descripcion'] and 'Rezago' not in row['descripcion']:
                f.write(f"**{row['descripcion']}**\n")
                corr_str = f"{row['correlacion']:.4f}" if not pd.isna(row['correlacion']) else 'N/A'
                f.write(f"- Coeficiente: {corr_str}\n")
                f.write(f"- Variables: `{row['variables']}`\n")
                f.write(f"- Observaciones: {row['n']}\n\n")
        
        # Categoría: Seguridad Alimentaria
        f.write("### 3. Factores de Seguridad Alimentaria\n\n")
        for i, row in resultados_df.iterrows():
            if 'alimentaria' in row['descripcion'] or 'consumo' in row['descripcion']:
                f.write(f"**{row['descripcion']}**\n")
                corr_str = f"{row['correlacion']:.4f}" if not pd.isna(row['correlacion']) else 'N/A'
                f.write(f"- Coeficiente: {corr_str}\n")
                f.write(f"- Variables: `{row['variables']}`\n")
                f.write(f"- Observaciones: {row['n']}\n\n")
        
        # Categoría: Índice de Rezago Social
        f.write("### 4. Índice de Rezago Social (IRS)\n\n")
        for i, row in resultados_df.iterrows():
            if 'IRS' in row['descripcion'] or 'Rezago Social' in row['descripcion']:
                f.write(f"**{row['descripcion']}**\n")
                corr_str = f"{row['correlacion']:.4f}" if not pd.isna(row['correlacion']) else 'N/A'
                f.write(f"- Coeficiente: {corr_str}\n")
                f.write(f"- Variables: `{row['variables']}`\n")
                f.write(f"- Observaciones: {row['n']}\n\n")
        
        # Categoría: Otras correlaciones
        f.write("### 5. Otras Correlaciones Exploradas\n\n")
        for i, row in resultados_df.iterrows():
            if 'Abandono primaria vs Abandono secundaria' in row['descripcion'] or 'Rezago educativo vs Carencia' in row['descripcion']:
                f.write(f"**{row['descripcion']}**\n")
                corr_str = f"{row['correlacion']:.4f}" if not pd.isna(row['correlacion']) else 'N/A'
                f.write(f"- Coeficiente: {corr_str}\n")
                f.write(f"- Variables: `{row['variables']}`\n")
                f.write(f"- Observaciones: {row['n']}\n\n")
        
        # Conclusiones
        f.write("## Conclusiones y Hallazgos Principales\n\n")
        
        # Top 5 correlaciones más fuertes
        top5 = resultados_df[resultados_df['abs_correlacion'].notna()].head(5)
        f.write("### Top 5 Correlaciones más Fuertes:\n\n")
        for idx, row in top5.iterrows():
            f.write(f"{list(resultados_df.index).index(idx) + 1}. **{row['descripcion']}**\n")
            f.write(f"   - r = {row['correlacion']:.4f} (|r| = {row['abs_correlacion']:.4f})\n\n")
        
        f.write("\n---\n\n")
        f.write("*Nota: Las correlaciones con |r| < 0.1 se consideran despreciables, entre 0.1-0.3 débiles, ")
        f.write("entre 0.3-0.5 moderadas, y > 0.5 fuertes. El IRS sigue siendo el indicador con mayor correlación ")
        f.write("conocida (~0.3).*\n")
    
    print(f"\n✅ Análisis completado. Se probaron {len(resultados)} correlaciones.")
    print(f"📄 Resultados guardados en 'ideas.md'")
    print(f"\nResumen:")
    print(f"  - Correlaciones fuertes (|r| > 0.5): {len(resultados_df[resultados_df['abs_correlacion'] > 0.5])}")
    print(f"  - Correlaciones moderadas (0.3 < |r| <= 0.5): {len(resultados_df[(resultados_df['abs_correlacion'] > 0.3) & (resultados_df['abs_correlacion'] <= 0.5)])}")
    print(f"  - Correlaciones débiles (0.1 < |r| <= 0.3): {len(resultados_df[(resultados_df['abs_correlacion'] > 0.1) & (resultados_df['abs_correlacion'] <= 0.3)])}")
    print(f"  - Sin correlación (|r| <= 0.1): {len(resultados_df[resultados_df['abs_correlacion'] <= 0.1])}")

if __name__ == "__main__":
    main()
