import streamlit as st

from utils.data_loader import load_data
from utils.filters import apply_filters

from utils.plots import (
    plot_station_map,
    plot_station_activity_levels,
    plot_top_stations
)

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Analisis Geoespacial",
    page_icon="🌎",
    layout="wide"
)

# =========================================================
# CARGA DE DATOS
# =========================================================

df = load_data()

# =========================================================
# FILTROS GLOBALES
# =========================================================

df_filtered = apply_filters(df)

# =========================================================
# HEADER
# =========================================================

st.title("Analisis Geoespacial")

st.markdown("""
### Análisis Espacial del Sistema de Bicicletas Compartidas

Esta sección permite explorar:

- estaciones con mayor demanda
- distribución geográfica de viajes
- hotspots urbanos
- concentración espacial de movilidad
""")

st.markdown("---")

# =========================================================
# KPIs GEOESPACIALES
# =========================================================

# ---------------------------------------------------------
# TOTAL ESTACIONES
# ---------------------------------------------------------

total_stations = (
    df_filtered["start_station_name"]
    .nunique()
)

# ---------------------------------------------------------
# ESTACIÓN MÁS UTILIZADA
# ---------------------------------------------------------

top_station = (
    df_filtered["start_station_name"]
    .value_counts()
    .idxmax()
)

top_station_trips = (
    df_filtered["start_station_name"]
    .value_counts()
    .max()
)

# ---------------------------------------------------------
# VIAJES GEOLOCALIZADOS
# ---------------------------------------------------------

geo_trips = len(df_filtered)

# ---------------------------------------------------------
# PROMEDIO VIAJES POR ESTACIÓN
# ---------------------------------------------------------

avg_station_trips = round(
    geo_trips / total_stations,
    2
)

# =========================================================
# DISPLAY KPIs
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Estaciones Activas",
    f"{total_stations:,}"
)

col2.metric(
    "Estación con mmas viajes",
    top_station
)

col3.metric(
    "Viajes Geolocalizados",
    f"{geo_trips:,}"
)

col4.metric(
    "Promedio de viajes por estación",
    avg_station_trips
)

st.markdown("---")

# =========================================================
# MAPA PRINCIPAL
# =========================================================

st.subheader("Uso de Estaciones")

st.markdown("""
El tamaño y color de cada punto representan la intensidad de uso
de las estaciones de bicicletas.
""")

fig_station_map = plot_station_map(df_filtered)

st.plotly_chart(
    fig_station_map,
    use_container_width=True
)

st.markdown("---")

# =========================================================
# SEGUNDA FILA
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# TOP ESTACIONES
# =========================================================

with col1:

    st.subheader("Top Estaciones")

    st.markdown("""
    Estaciones con mayor cantidad de viajes iniciados.
    """)

    fig_top_stations = plot_top_stations(df_filtered)

    st.plotly_chart(
        fig_top_stations,
        use_container_width=True
    )

# =========================================================
# HEATMAP ESPACIAL
# =========================================================

with col2:

    st.subheader("Niveles de demanda")

    st.markdown("""
    Distribución de las esatciones por niveles de demanda.
    """)

    fig_density = plot_station_activity_levels(df_filtered)

    st.plotly_chart(
        fig_density,
        use_container_width=True
    )

st.markdown("---")

# =========================================================
# TABLA RESUMEN
# =========================================================

## st.subheader("Resumen por Estación")
## 
## station_summary = (
##     df_filtered
##     .groupby("start_station_name")
##     .agg({
##         "trip_duration_min": "mean",
##         "ride_id": "count"
##     })
##     .reset_index()
## )
## 
## station_summary.columns = [
##     "Estación",
##     "Duración Promedio (min)",
##     "Cantidad Viajes"
## ]
## 
## station_summary = station_summary.sort_values(
##     "Cantidad Viajes",
##     ascending=False
## )
## 
## st.dataframe(
##     station_summary,
##     use_container_width=True
## )
## 
# =========================================================
# INSIGHTS AUTOMÁTICOS
# =========================================================

st.markdown("---")

st.subheader("Insights Automáticos")

st.info(f"""
La estación más utilizada es **{top_station}**
con **{top_station_trips:,} viajes registrados**.

Se analizaron un total de **{geo_trips:,} viajes**
en **{total_stations:,} estaciones activas**.

El mapa de densidad permite identificar hotspots
de movilidad urbana y posibles zonas de alta demanda.
""")