"""
Streamlit App for Interactive Educational Funnel Chart

Run with: streamlit run embudo_streamlit.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


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


@st.cache_data
def cargar_datos_matricula(csv_path='fuentes/matricula_escolar_por_entidad_federativa_por_grado.csv'):
    """Load and preprocess enrollment data."""
    matriculas = pd.read_csv(csv_path)
    for col in ['Total', 'Hombres', 'Mujeres']:
        matriculas[col] = matriculas[col].apply(limpiar_numero)
    return matriculas


def obtener_datos_por_estado(matriculas, estado='Estados Unidos Mexicanos'):
    """Get funnel data for a specific state."""
    datos_estado = matriculas[matriculas['Entidad federativa'] == estado].copy()
    niveles_orden = ['Primaria', 'Secundaria', 'Media superior', 'Superior']
    datos_estado = datos_estado[datos_estado['Nivel educativo'].isin(niveles_orden)]
    datos_estado['orden'] = datos_estado['Nivel educativo'].map({n: i for i, n in enumerate(niveles_orden)})
    datos_estado = datos_estado.sort_values('orden')
    
    if len(datos_estado) > 0:
        total_primaria = datos_estado['Total'].iloc[0]
        datos_estado['porcentaje'] = [round((t / total_primaria) * 100) for t in datos_estado['Total']]
    
    return datos_estado


def crear_funnel_chart(datos_estado, estado_nombre):
    """Create funnel chart for a specific state."""
    stages = ['Primaria', 'Secundaria', 'Media Superior', 'Superior']
    valores = datos_estado['porcentaje'].values.tolist()
    totales = datos_estado['Total'].values.tolist()
    
    # Create labels
    text_labels = []
    for t, p in zip(totales, valores):
        if t >= 1_000_000:
            label = f"<b>{t/1_000_000:.1f}M</b><br>{p}%"
        else:
            label = f"<b>{t/1_000:.0f}K</b><br>{p}%"
        text_labels.append(label)
    
    # Generate colors
    color_start = "#114038"
    color_end = "#8ee3d5"
    n_levels = len(stages)
    colors = [interpolate_color(color_start, color_end, i / (n_levels - 1)) for i in range(n_levels)]
    
    # Create annotations
    annotations = []
    for i, (stage, color, val) in enumerate(zip(stages, colors, valores)):
        annotations.append(dict(
            x=val + 5, y=stage, xref='x', yref='y',
            text=f"<b>{stage}</b>",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2,
            arrowcolor=color, font=dict(color=color, size=14),
            ax=40, ay=0, align='left', xanchor='left'
        ))
    
    fig = go.Figure(go.Funnel(
        y=stages, x=valores, text=text_labels,
        textposition="inside", textinfo="text",
        marker=dict(color=colors, line=dict(color="white", width=2)),
        connector=dict(line=dict(color="#cccccc", width=2)),
        opacity=0.95
    ))
    
    fig.update_layout(
        title={
            'text': f'Embudo Educativo: {estado_nombre}<br><sup>Retención Escolar (Base: Primaria = 100)</sup>',
            'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}
        },
        height=500, width=900, showlegend=False,
        paper_bgcolor="white", plot_bgcolor="white",
        annotations=annotations,
        yaxis=dict(showticklabels=False),
    )
    fig.update_xaxes(title_text="% respecto a Primaria")
    
    return fig


def main():
    st.set_page_config(
        page_title="Embudo Educativo - México",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Embudo Educativo en México")
    st.markdown("""
    Esta visualización muestra la retención escolar desde primaria hasta educación superior.
    Selecciona una entidad federativa para ver los datos específicos.
    """)
    
    # Load data
    matriculas = cargar_datos_matricula()
    
    # Get list of states
    estados = sorted(matriculas['Entidad federativa'].unique())
    if 'Estados Unidos Mexicanos' in estados:
        estados.remove('Estados Unidos Mexicanos')
        estados = ['Estados Unidos Mexicanos'] + estados
    
    # State selector
    estado_seleccionado = st.selectbox(
        "🏛️ Selecciona una entidad federativa:",
        estados,
        index=0
    )
    
    # Get data for selected state
    datos_estado = obtener_datos_por_estado(matriculas, estado_seleccionado)
    
    # Create columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display funnel chart
        fig = crear_funnel_chart(datos_estado, estado_seleccionado)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Display data table
        st.subheader("📊 Datos de Matrícula")
        
        display_data = datos_estado[['Nivel educativo', 'Total', 'porcentaje']].copy()
        display_data.columns = ['Nivel Educativo', 'Matrícula Total', '% vs Primaria']
        
        # Format numbers
        display_data['Matrícula Total'] = display_data['Matrícula Total'].apply(
            lambda x: f"{x:,}"
        )
        display_data['% vs Primaria'] = display_data['% vs Primaria'].apply(
            lambda x: f"{x}%"
        )
        
        st.dataframe(display_data, use_container_width=True, hide_index=True)
        
        # Show summary statistics
        st.subheader("📈 Estadísticas")
        
        if len(datos_estado) >= 2:
            primaria = datos_estado.iloc[0]['Total']
            secundaria = datos_estado.iloc[1]['Total']
            superior = datos_estado.iloc[-1]['Total']
            
            retencion_sec = (secundaria / primaria) * 100
            retencion_sup = (superior / primaria) * 100
            
            st.metric("Retención a Secundaria", f"{retencion_sec:.1f}%")
            st.metric("Retención a Superior", f"{retencion_sup:.1f}%")
            st.metric("Pérdida total", f"{100 - retencion_sup:.1f}%")
    
    # Footer
    st.markdown("---")
    st.caption("""
    **Fuente:** Datos de matrícula escolar por entidad federativa. 
    El embudo muestra el porcentaje de estudiantes que se retienen respecto a la matrícula de primaria (base 100%).
    """)


if __name__ == "__main__":
    main()
