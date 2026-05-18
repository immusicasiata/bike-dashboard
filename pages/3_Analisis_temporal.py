import streamlit as st

from utils.data_loader import load_data
from utils.filters import apply_filters

from utils.plots import (
    plot_trips_over_time,
    plot_trips_by_hour,
    plot_trips_by_weekday,
    plot_avg_duration_by_hour,
    plot_temporal_heatmap
)

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Analsis Temporal",
    page_icon="📈",
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

st.title("Analsis Temporal")

st.markdown("""
### Análisis Temporal del Sistema de Bicicletas Compartidas

Esta sección permite analizar:

- patrones horarios
- comportamiento semanal
- tendencias temporales
- horas pico
- duración de viajes
""")

st.markdown("---")

# =========================================================
# KPIs TEMPORALES
# =========================================================

# ---------------------------------------------------------
# HORA PICO
# ---------------------------------------------------------

peak_hour = (
    df_filtered["hour"]
    .mode()[0]
)

peak_hour_trips = (
    df_filtered[df_filtered["hour"] == peak_hour]
    .shape[0]
)

# ---------------------------------------------------------
# DÍA MÁS ACTIVO
# ---------------------------------------------------------

top_day = (
    df_filtered["weekday"]
    .value_counts()
    .idxmax()
)

top_day_trips = (
    df_filtered["weekday"]
    .value_counts()
    .max()
)

# ---------------------------------------------------------
# PROMEDIO VIAJES DIARIOS
# ---------------------------------------------------------

daily_avg = round(
    df_filtered
    .groupby("date")
    .size()
    .mean(),
    2
)

# ---------------------------------------------------------
# DURACIÓN PROMEDIO
# ---------------------------------------------------------

avg_duration = round(
    df_filtered["trip_duration_min"]
    .mean(),
    2
)

# =========================================================
# DISPLAY KPIs
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Hora Pico",
    f"{peak_hour}:00"
)

col2.metric(
    "Día Más Activo",
    top_day
)

col3.metric(
    "Promedio Viajes/Día",
    f"{daily_avg:,.0f}"
)

col4.metric(
    "Duración Promedio",
    f"{avg_duration} min"
)

st.markdown("---")

# =========================================================
# EVOLUCIÓN TEMPORAL
# =========================================================

st.subheader("Evolución Temporal de Viajes")

st.markdown("""
Cantidad de viajes registrados a lo largo del tiempo.
""")

fig_trend = plot_trips_over_time(df_filtered)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

st.markdown("---")

# =========================================================
# SEGUNDA FILA
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# VIAJES POR HORA
# =========================================================

with col1:

    st.subheader("Viajes por Hora")

    st.markdown("""
    Distribución de viajes según la hora del día.
    """)

    fig_hour = plot_trips_by_hour(df_filtered)

    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )

# =========================================================
# VIAJES POR DÍA
# =========================================================

with col2:

    st.subheader("Viajes por Día de Semana")

    st.markdown("""
    Comportamiento semanal del sistema.
    """)

    fig_weekday = plot_trips_by_weekday(df_filtered)

    st.plotly_chart(
        fig_weekday,
        use_container_width=True
    )

st.markdown("---")

# =========================================================
# DURACIÓN PROMEDIO
# =========================================================

st.subheader("Duración Promedio por Hora")

st.markdown("""
Permite identificar en qué horarios ocurren
los viajes más largos.
""")

fig_duration = plot_avg_duration_by_hour(df_filtered)

st.plotly_chart(
    fig_duration,
    use_container_width=True
)

st.markdown("---")

# =========================================================
# HEATMAP TEMPORAL
# =========================================================

st.subheader("Heatmap Temporal")

st.markdown("""
Mapa de intensidad temporal que muestra
la concentración de viajes por:
- hora
- día de la semana
""")

fig_heatmap = plot_temporal_heatmap(df_filtered)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

st.markdown("---")

# =========================================================
# INSIGHTS AUTOMÁTICOS
# =========================================================

st.subheader("Insights Automáticos")

st.info(f"""
La hora pico del sistema es las **{peak_hour}:00**
con aproximadamente **{peak_hour_trips:,} viajes**.

El día más activo es **{top_day}**
con **{top_day_trips:,} viajes registrados**.

El sistema registra en promedio
**{daily_avg:,.0f} viajes diarios**.

La duración promedio de los viajes es
de **{avg_duration} minutos**.
""")