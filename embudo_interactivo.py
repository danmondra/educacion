"""
Interactive Educational Funnel Chart with State Selector

This module creates an interactive funnel chart showing educational retention
data that can be filtered by Mexican state. The default view shows national
data ("Estados Unidos Mexicanos").
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def limpiar_numero(valor):
    """Convert numbers with commas to integers."""
    if isinstance(valor, str):
        return int(valor.replace(',', ''))
    return valor


def interpolate_color(color1, color2, factor):
    """Interpolate between two hex colors."""
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    
    return f"#{r:02x}{g:02x}{b:02x}"


def cargar_datos_matricula(csv_path='fuentes/matricula_escolar_por_entidad_federativa_por_grado.csv'):
    """Load and preprocess enrollment data."""
    matriculas = pd.read_csv(csv_path)
    
    # Clean numeric columns
    for col in ['Total', 'Hombres', 'Mujeres']:
        matriculas[col] = matriculas[col].apply(limpiar_numero)
    
    return matriculas


def obtener_datos_por_estado(matriculas, estado='Estados Unidos Mexicanos'):
    """
    Get funnel data for a specific state.
    
    Args:
        matriculas: DataFrame with enrollment data
        estado: State name (default: 'Estados Unidos Mexicanos' for national data)
    
    Returns:
        DataFrame with funnel data for the selected state
    """
    # Filter by state
    datos_estado = matriculas[matriculas['Entidad federativa'] == estado].copy()
    
    # Select only levels from primary to higher education (exclude Total, Inicial, Preescolar)
    niveles_orden = ['Primaria', 'Secundaria', 'Media superior', 'Superior']
    datos_estado = datos_estado[datos_estado['Nivel educativo'].isin(niveles_orden)]
    
    # Sort by educational level order
    datos_estado['orden'] = datos_estado['Nivel educativo'].map({n: i for i, n in enumerate(niveles_orden)})
    datos_estado = datos_estado.sort_values('orden')
    
    # Calculate percentages (base: Primary = 100%)
    if len(datos_estado) > 0:
        total_primaria = datos_estado['Total'].iloc[0]
        datos_estado['porcentaje'] = [round((t / total_primaria) * 100) for t in datos_estado['Total']]
    
    return datos_estado


def crear_funnel_data(datos_estado):
    """
    Create funnel chart data from state data.
    
    Returns:
        Tuple of (stages, valores, totales, text_labels, colors)
    """
    stages = ['Primaria', 'Secundaria', 'Media Superior', 'Superior']
    valores = datos_estado['porcentaje'].values.tolist()
    totales = datos_estado['Total'].values.tolist()
    
    # Create labels with totals and percentages
    text_labels = []
    for t, p in zip(totales, valores):
        if t >= 1_000_000:
            label = f"<b>{t/1_000_000:.1f}M</b><br>{p}%"
        else:
            label = f"<b>{t/1_000:.0f}K</b><br>{p}%"
        text_labels.append(label)
    
    # Generate color gradient from #114038 to #8ee3d5
    color_start = "#114038"
    color_end = "#8ee3d5"
    n_levels = len(stages)
    colors = [interpolate_color(color_start, color_end, i / (n_levels - 1)) for i in range(n_levels)]
    
    return stages, valores, totales, text_labels, colors


def crear_embudo_interactivo(csv_path='fuentes/matricula_escolar_por_entidad_federativa_por_grado.csv'):
    """
    Create an interactive funnel chart with state selector dropdown.
    
    Args:
        csv_path: Path to the enrollment data CSV file
    
    Returns:
        Plotly Figure object with interactive state selector
    """
    # Load data
    matriculas = cargar_datos_matricula(csv_path)
    
    # Get list of available states (excluding 'Total' rows, keeping national as first)
    estados = sorted(matriculas['Entidad federativa'].unique())
    # Move 'Estados Unidos Mexicanos' to the front as default
    if 'Estados Unidos Mexicanos' in estados:
        estados.remove('Estados Unidos Mexicanos')
        estados = ['Estados Unidos Mexicanos'] + estados
    
    # Create figure with initial data (national)
    datos_inicial = obtener_datos_por_estado(matriculas, 'Estados Unidos Mexicanos')
    stages, valores, totales, text_labels, colors = crear_funnel_data(datos_inicial)
    
    fig = go.Figure()
    
    # Add initial funnel trace
    fig.add_trace(go.Funnel(
        y=stages,
        x=valores,
        text=text_labels,
        textposition="inside",
        textinfo="text",
        marker=dict(
            color=colors,
            line=dict(color="white", width=2)
        ),
        connector=dict(line=dict(color="#cccccc", width=2)),
        opacity=0.95,
        name='Embudo Educativo'
    ))
    
    # Create dropdown buttons for each state
    dropdown_buttons = []
    for estado in estados:
        datos_estado = obtener_datos_por_estado(matriculas, estado)
        
        if len(datos_estado) > 0:
            _, valores_estado, _, text_labels_estado, _ = crear_funnel_data(datos_estado)
            
            # Create annotation update for this state
            annotations = []
            for i, (stage, color, val) in enumerate(zip(stages, colors, valores_estado)):
                annotations.append(dict(
                    x=val,
                    y=stage,
                    xref='x',
                    yref='y',
                    text=f"<b>{stage}</b>",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1.5,
                    arrowwidth=2,
                    arrowcolor=color,
                    font=dict(color=color, size=16),
                    ax=15,
                    ay=0,
                    align='left',
                    xanchor='left'
                ))
            
            button = dict(
                label=estado,
                method="update",
                args=[
                    {
                        "y": [stages],
                        "x": [valores_estado],
                        "text": [text_labels_estado],
                    },
                    {
                        "title": {
                            'text': f'Embudo Educativo: {estado}<br><sup>Retención Escolar (Base: Primaria = 100)</sup>',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18}
                        },
                        "annotations": annotations
                    }
                ]
            )
            dropdown_buttons.append(button)
    
    # Create initial annotations
    initial_annotations = []
    for i, (stage, color, val) in enumerate(zip(stages, colors, valores)):
        initial_annotations.append(dict(
            x=val,
            y=stage,
            xref='x',
            yref='y',
            text=f"<b>{stage}</b>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor=color,
            font=dict(color=color, size=16),
            ax=15,
            ay=0,
            align='left',
            xanchor='left'
        ))
    
    # Update layout with dropdown menu
    fig.update_layout(
        title={
            'text': 'Embudo Educativo: Estados Unidos Mexicanos<br><sup>Retención Escolar (Base: Primaria = 100)</sup>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        height=800,
        width=1000,
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        annotations=initial_annotations,
        yaxis=dict(showticklabels=False),
        updatemenus=[
            dict(
                active=0,
                buttons=dropdown_buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.15,
                yanchor="top",
                bgcolor="white",
                bordercolor="#114038",
                font=dict(color="#114038", size=12),
            )
        ],
    )
    
    # Add label for dropdown
    fig.add_annotation(
        x=0.02,
        y=1.12,
        xref="paper",
        yref="paper",
        text="<b>Selecciona una entidad:</b>",
        showarrow=False,
        font=dict(size=14, color="#114038"),
        align="left"
    )
    
    # Update x-axis
    fig.update_xaxes(title_text="% respecto a Primaria")
    
    return fig


def mostrar_embudo(csv_path='fuentes/matricula_escolar_por_entidad_federativa_por_grado.csv'):
    """
    Display the interactive funnel chart.
    
    Args:
        csv_path: Path to the enrollment data CSV file
    """
    fig = crear_embudo_interactivo(csv_path)
    fig.show()
    return fig


def exportar_html(fig, output_path='embudo_educativo_interactivo.html'):
    """
    Export the funnel chart to an HTML file.
    
    Args:
        fig: Plotly Figure object
        output_path: Path to save the HTML file
    """
    fig.write_html(output_path)
    print(f"Funnel chart exported to: {output_path}")


if __name__ == "__main__":
    # Create and display the interactive funnel
    fig = mostrar_embudo()
    
    # Optionally export to HTML
    # exportar_html(fig, 'embudo_educativo_interactivo.html')
