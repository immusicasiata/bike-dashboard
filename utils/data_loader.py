import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data       # Cargar información en cache para eficiencia ##############
######## No vuelvas a ejecutar esta función cada vez que el usuario interactúe #########
def load_data():

    df = pd.read_csv(
        "data/202603-capitalbikeshare-tripdata.csv"
    )

    # -----------------------------------------------------
    # CONVERSIÓN DE FECHAS
    # -----------------------------------------------------

    df["started_at"] = pd.to_datetime(df["started_at"])
    df["ended_at"] = pd.to_datetime(df["ended_at"])

    # -----------------------------------------------------
    # VARIABLES DE TIEMPO
    # -----------------------------------------------------

    df["date"] = df["started_at"].dt.date
    df["hour"] = df["started_at"].dt.hour
    df["weekday"] = df["started_at"].dt.day_name()
    df["month"] = df["started_at"].dt.month_name()

    # -----------------------------------------------------
    # DURACIÓN EN MINUTOS
    # -----------------------------------------------------

    df["trip_duration_min"] = (
        (df["ended_at"] - df["started_at"])
        .dt.total_seconds() / 60
    )

    # -----------------------------------------------------
    # DISTANCIA EN KM
    # -----------------------------------------------------
    df["trip_distance_km"] = haversine(

    df["start_lat"],
    df["start_lng"],

    df["end_lat"],
    df["end_lng"]
    )

    # -----------------------------------------------------
    # LIMPIEZA BÁSICA
    # -----------------------------------------------------

    df = df[df["trip_duration_min"] > 0]

    return df



def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    lat1, lon1, lat2, lon2 = map(
        np.radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))

    return R * c

