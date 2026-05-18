import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.filters import apply_filters


from utils.plots import (
    plot_trips_over_time,
    plot_trips_by_hour,
    plot_user_type_distribution
)


st.set_page_config(
    page_title="Citi Bike Resumen",
    page_icon="🚲",
    layout="wide"
)

# =====================================================
# DATA
# =====================================================

df = load_data()

# =====================================================
# FILTROS
# =====================================================

df_filtered = apply_filters(df)

st.title("Resumen de bicicletas compartidas")

st.markdown("""
Análisis general del sistema de bicicletas compartidas
""")

st.markdown("---")

# =========================================================
# KPIs
# =========================================================

# =========================================================
# calculo de KPIs
# =========================================================

total_trips = len(df_filtered)

avg_duration = round(
    df_filtered["trip_duration_min"].mean(),
    2
)

active_stations = (
    df_filtered["start_station_name"]
    .nunique()
)

peak_hour = (
    df_filtered["hour"]
    .mode()[0]
)

# ---------------------------------------------------------
# VISUALIZACIÓN KPIs
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Viajes",
    f"{total_trips:,}"
)

col2.metric(
    "Duración Promedio",
    f"{avg_duration} min"
)

col3.metric(
    "Estaciones Activas",
    active_stations
)

col4.metric(
    "Hora Pico",
    f"{peak_hour}:00"
)

st.markdown("---")

# =========================================================
# GRÁFICO 1 - VIAJES EN EL TIEMPO
# =========================================================

st.plotly_chart(
    plot_trips_over_time(df_filtered),
    use_container_width=True
)

# =========================================================
# SEGUNDA FILA DE GRÁFICOS
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# GRÁFICO 2 - VIAJES POR HORA
# =========================================================

col1.plotly_chart(
    plot_trips_by_hour(df_filtered),
    use_container_width=True
)

# =========================================================
# GRÁFICO 3 - TIPO DE USUARIO
# =========================================================

col2.plotly_chart(
    plot_user_type_distribution(df_filtered),
    use_container_width=True
)

