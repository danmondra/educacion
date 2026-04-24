"""
Example usage of the interactive funnel module.

This script demonstrates how to use the embudo_interactivo module
to create an interactive funnel chart with state selection.
"""

from embudo_interactivo import (
    cargar_datos_matricula,
    obtener_datos_por_estado,
    crear_embudo_interactivo,
    mostrar_embudo,
    exportar_html
)

# Method 1: Simply display the interactive funnel
# This opens a browser window with the interactive chart
print("Opening interactive funnel chart...")
fig = mostrar_embudo()

# Method 2: Export to HTML for sharing
# exportar_html(fig, 'mi_embudo.html')

# Method 3: Get data programmatically and create custom visualizations
# matriculas = cargar_datos_matricula()
# datos_nacional = obtener_datos_por_estado(matriculas, 'Estados Unidos Mexicanos')
# datos_jalisco = obtener_datos_por_estado(matriculas, 'Jalisco')
# print("Nacional:", datos_nacional[['Nivel educativo', 'Total', 'porcentaje']])
# print("\nJalisco:", datos_jalisco[['Nivel educativo', 'Total', 'porcentaje']])
