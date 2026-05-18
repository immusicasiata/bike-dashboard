
import streamlit as st

from utils.data_loader import load_data
from utils.filters import apply_filters

from utils.plots import (
    plot_top_routes,
    plot_sankey_routes,
    plot_od_matrix,
    plot_trip_distance_distribution
)

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Flujo de movilidad",
    page_icon="🔁",
    layout="wide"
)

# =========================================================
# CARGA DE DATOS
# =========================================================

df = load_data()

# =========================================================
# FILTROS
# =========================================================

df_filtered = apply_filters(df)

# =========================================================
# HEADER
# =========================================================

st.title("Analisis de flujo de movilidad")

st.markdown("""
### Análisis de Flujos y Movilidad Urbana

Esta sección permite explorar:

- rutas más frecuentes
- patrones de movilidad
- conexiones entre estaciones
- flujos origen-destino
- comportamiento espacial de usuarios
""")

st.markdown("---")

# =========================================================
# FEATURE ENGINEERING
# =========================================================

df_filtered["route"] = (
    df_filtered["start_station_name"]
    + " → " +
    df_filtered["end_station_name"]
)

# =========================================================
# KPIs
# =========================================================

# ---------------------------------------------------------
# RUTA MÁS USADA
# ---------------------------------------------------------

top_route = (
    df_filtered["route"]
    .value_counts()
    .idxmax()
)

top_route_trips = (
    df_filtered["route"]
    .value_counts()
    .max()
)

# ---------------------------------------------------------
# RUTAS ÚNICAS
# ---------------------------------------------------------

unique_routes = (
    df_filtered["route"]
    .nunique()
)

# ---------------------------------------------------------
# ORIGEN MÁS USADO
# ---------------------------------------------------------

top_origin = (
    df_filtered["start_station_name"]
    .value_counts()
    .idxmax()
)

# ---------------------------------------------------------
# DESTINO MÁS USADO
# ---------------------------------------------------------

top_destination = (
    df_filtered["end_station_name"]
    .value_counts()
    .idxmax()
)

# =========================================================
# DISPLAY KPIs
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Rutas Únicas",
    f"{unique_routes:,}"
)

col2.metric(
    "Ruta Más Frecuente",
    f"{top_route_trips:,}"
)

col3.metric(
    "Origen Top",
    top_origin
)

col4.metric(
    "Destino Top",
    top_destination
)

st.markdown("---")

# =========================================================
# TOP RUTAS
# =========================================================

st.subheader("Top Rutas")

st.markdown("""
Rutas con mayor cantidad de viajes registrados.
""")

fig_routes = plot_top_routes(df_filtered)

st.plotly_chart(
    fig_routes,
    use_container_width=True
)

st.markdown("---")

# =========================================================
# SANKEY DIAGRAM
# =========================================================

st.subheader("Flujo entre Estaciones")

st.markdown("""
Visualización de flujos de movilidad entre
estaciones origen y destino.
""")

fig_sankey = plot_sankey_routes(df_filtered)

st.plotly_chart(
    fig_sankey,
    use_container_width=True
)

st.markdown("---")

# =========================================================
# MATRIZ ORIGEN-DESTINO
# =========================================================

st.subheader("Matriz Origen-Destino entre las top 10 estaciones")

st.markdown("""
Mapa matricial de intensidad de conexiones
entre estaciones.
""")

fig_od = plot_od_matrix(df_filtered)

st.plotly_chart(
    fig_od,
    use_container_width=True
)

st.markdown("---")

# =========================================================
# DISTRIBUCIÓN DE DISTANCIAS
# =========================================================

st.subheader("Distribución de Distancias")

st.markdown("""
Distribución estimada de distancias recorridas
por los usuarios.
""")

fig_distance = plot_trip_distance_distribution(
    df_filtered
)

st.plotly_chart(
    fig_distance,
    use_container_width=True
)

st.markdown("---")

# =========================================================
# INSIGHTS AUTOMÁTICOS
# =========================================================

st.subheader("Insights Automáticos")

st.info(f"""
La ruta más frecuente es:

**{top_route}**  con **{top_route_trips:,} viajes registrados**.

 La estación origen con más actividad es:
**{top_origin}**

 La estación destino más utilizada es:
**{top_destination}**

 Se identificaron un total de
**{unique_routes:,} rutas únicas**
en el sistema.
""")