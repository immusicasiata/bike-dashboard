
import streamlit as st

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Dashboard analisis biciletas compartidas",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Dashboard de analisis para biciletas compartidas")

st.sidebar.markdown("""
### 
Dashboard interactivo desarrollado con:

- Python
- Streamlit
- Plotly
- Pandas

para análisis de:
- movilidad urbana
- comportamiento temporal
- análisis geoespacial
- flujos de movilidad
""")

st.sidebar.markdown("---")

st.sidebar.info("""
Navega entre las páginas usando el menú lateral de Streamlit.
""")

# =========================================================
# PÁGINA PRINCIPAL
# =========================================================

st.title("Dashboard de analisis para biciletas compartidas")

st.markdown("""
## Plataforma de Analítica de Movilidad Urbana

Este dashboard interactivo permite explorar patrones
de uso del sistema de bicicletas compartidas mediante
visualizaciones avanzadas y análisis de datos.

---

# Secciones del Dashboard

""")

# =========================================================
# SECCIONES
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# OVERVIEW
# =========================================================

with col1:

    st.subheader("Resumen Ejecutivo")

    st.markdown("""
    Resumen ejecutivo del sistema:
    
    - KPIs principales
    - métricas generales
    - tendencias básicas
    - comportamiento global
    """)

# =========================================================
# GEOESPACIAL
# =========================================================

with col2:

    st.subheader("Analisis Geoespacial")

    st.markdown("""
    Análisis espacial del sistema:
    
    - mapas interactivos
    - estaciones más usadas
    - distribución geográfica
    - patrones espaciales
    """)

# =========================================================
# SEGUNDA FILA
# =========================================================

col3, col4 = st.columns(2)

# =========================================================
# TEMPORAL
# =========================================================

with col3:

    st.subheader("Analisis Temporal")

    st.markdown("""
    Exploración temporal de los viajes:
    
    - horas pico
    - comportamiento semanal
    - tendencias temporales
    - heatmaps de actividad
    """)

# =========================================================
# FLOW
# =========================================================

with col4:

    st.subheader("Flujo de movilidad")

    st.markdown("""
    Análisis de flujos urbanos:
    
    - rutas más frecuentes
    - matrices OD
    - Sankey diagrams
    - patrones de movilidad
    """)

st.markdown("---")

# =========================================================
# TECNOLOGÍAS
# =========================================================


# =========================================================
# ESTRUCTURA DEL PROYECTO
# =========================================================

st.header("📁 Estructura del Proyecto")

st.code("""
project/
│
├── dash_bicis.py
├── requirements.txt
│
├── data/
│   └── 202603-capitalbikeshare-tripdata.csv
│
├── pages/
│   ├── 1_Executive_Overview.py
│   ├── 2_Geospatial_Analysis.py
│   ├── 3_Temporal_Analysis.py
│   └── 4_Mobility_Flow.py
│
├── utils/
│   ├── data_loader.py
│   ├── filters.py
│   └── plots.py
""")

st.markdown("---")

# =========================================================
# FOOTER
# =========================================================

st.caption("""
Dashboard académico desarrollado para el curso de
Analítica de Datos.
""")