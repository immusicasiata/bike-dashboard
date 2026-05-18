import streamlit as st
import pandas as pd




def apply_filters(df):

    # =========================================================
    # DEFINICIÓN DE FILTROS
    # =========================================================

    st.sidebar.title("Filtros")

    # =====================================================
    # FILTRO FECHAS
    # =====================================================

    date_range = st.sidebar.date_input(
        "Rango de fechas",
        (
            df["started_at"].min().date(),
            df["started_at"].max().date()
        )
    )

    # =====================================================
    # FILTRO DE TIPO DE USUARIO
    # =====================================================

    user_types = st.sidebar.multiselect(
        "Tipo de usuario",
        options=df["member_casual"].unique(),
        default=df["member_casual"].unique()
    )

    # =====================================================
    # FILTRO HORARIO
    # =====================================================

    hour_range = st.sidebar.slider(
        "Rango horario",
        0,
        23,
        (0, 23)
    )

    # =========================================================
    # APLICACIÓN DE FILTROS
    # =========================================================

    df_filtered = df.copy()

    # -----------------------------------------------------

    # ---------------------------------------------------------
    # FILTRO FECHAS
    # ---------------------------------------------------------

    if len(date_range) == 2:

        start_date, end_date = date_range

        df_filtered = df_filtered[
            (df_filtered["started_at"].dt.date >= start_date) &
            (df_filtered["started_at"].dt.date <= end_date)
        ]

    # -----------------------------------------------------
    # ---------------------------------------------------------
    # FILTRO TIPO USUARIO
    # ---------------------------------------------------------

    if len(user_types) > 0:

        df_filtered = df_filtered[
            df_filtered["member_casual"].isin(user_types)
        ]

    # -----------------------------------------------------
    # ---------------------------------------------------------
    # FILTRO POR HORAS
    # ---------------------------------------------------------

    df_filtered = df_filtered[
        (df_filtered["hour"] >= hour_range[0]) &
        (df_filtered["hour"] <= hour_range[1])
    ]

    return df_filtered