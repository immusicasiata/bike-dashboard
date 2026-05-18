import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

PLOT_TEMPLATE = "plotly_white"

# =========================================================
# graficas para la pagina resumen
# =========================================================

# =========================================================
# GRÁFICO 1.1 - VIAJES EN EL TIEMPO
# =========================================================

def plot_trips_over_time(df):

    trips_per_day = (
        df.groupby("date")
        .size()
        .reset_index(name="trips")
    )

    fig = px.line(
        trips_per_day,
        x="date",
        y="trips",
        title="Evolución de Viajes en el Tiempo",
        markers=True
    )

    fig.update_layout(
        template=PLOT_TEMPLATE,
        title={
            "x": 0.5
        },
        xaxis_title="Fecha",
        yaxis_title="Cantidad de viajes",
        height=450
    )

    return fig


# =========================================================
# GRÁFICO 1.2 - VIAJES POR HORA
# =========================================================

def plot_trips_by_hour(df):

    trips_by_hour = (
        df.groupby("hour")
        .size()
        .reset_index(name="trips")
    )

    fig = px.bar(
        trips_by_hour,
        x="hour",
        y="trips",
        title="Viajes por Hora"
    )

    fig.update_layout(
        template=PLOT_TEMPLATE,
        title={"x": 0.5},
        xaxis_title="Hora",
        yaxis_title="Cantidad de viajes",
        height=400
    )

    return fig


# =========================================================
# GRÁFICO 1.3 - TIPO DE USUARIO
# =========================================================

def plot_user_type_distribution(df):

    users_count = (
        df["member_casual"]
        .value_counts()
        .reset_index()
    )

    users_count.columns = [
        "user_type",
        "count"
    ]

    fig = px.pie(
        users_count,
        names="user_type",
        values="count",
        title="Distribución por Tipo de Usuario",
        hole=0.45
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    fig.update_layout(
        template=PLOT_TEMPLATE,
        title={"x": 0.5},
        height=400
    )

    return fig

# ===========================================================================================================================================================================

# =========================================================
# graficas para analisis geoespacial
# =========================================================

# =========================================================
# GRÁFICO 2.1 - Mapa de estaciones
# =========================================================
def plot_station_map(df):

    stations = (
        df.groupby('start_station_name').agg(
            trip_count=('ride_id', 'count'),           # número de viajes
            start_lat=('start_lat', 'mean'),    # media de latitud
            start_lng=('start_lng', 'mean')     # media de longitud
            ).reset_index()
    )

    stations = stations.rename(columns={'trip_count': 'Conteo de viajes'})
    fig = px.scatter_mapbox(
        stations,
        lat="start_lat",
        lon="start_lng",
        size="Conteo de viajes",
        color="Conteo de viajes",
        hover_name="start_station_name",
        hover_data={
            "Conteo de viajes": ":,.0f",
            "start_lat": False,
            "start_lng": False
        },
        zoom=10,
        title="Uso de Estaciones"
    )
    fig.update_traces(marker=dict(sizemin=2))
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={
            "r":0,
            "t":50,
            "l":0,
            "b":0
        },
        height=700
    )

    return fig


# =========================================================
# GRÁFICO 2.2 - distribución por niveles de demanda 
# =========================================================

def plot_station_activity_levels(df):

    # =====================================================
    # AGRUPAR ESTACIONES
    # =====================================================

    stations = (
        df.groupby('start_station_name').agg(
            trip_count=('ride_id', 'count'),           # número de viajes
            start_lat=('start_lat', 'mean'),    # media de latitud
            start_lng=('start_lng', 'mean')     # media de longitud
            ).reset_index()
    )
    
    stations = stations.rename(columns={'trip_count': 'Cantidad de Viajes'})
    # =====================================================
    # SEGMENTACIÓN
    # =====================================================

    q1 = stations["Cantidad de Viajes"].quantile(0.25)
    q2 = stations["Cantidad de Viajes"].quantile(0.50)
    q3 = stations["Cantidad de Viajes"].quantile(0.75)
    max_trips = stations["Cantidad de Viajes"].max()

    bins = [0, q1, q2, q3, max_trips + 1]


    stations["Nivel de Demanda"] = pd.cut(
        stations["Cantidad de Viajes"],
        bins,
        labels=[
            "Baja",
            "Media",
            "Alta",
            "Muy Alta"
        ],
    )

    # =====================================================
    # MAPA
    # =====================================================

    fig = px.scatter_mapbox(

        stations,

        lat="start_lat",
        lon="start_lng",

        size="Cantidad de Viajes",

        color="Nivel de Demanda",

        hover_name="start_station_name",

        hover_data={
            "Cantidad de Viajes": ":,.0f",
            "start_lat": False,
            "start_lng": False
        },

        zoom=10,

        title="Niveles de Demanda por Estación"
    )

    fig.update_traces(marker=dict(sizemin=2))

    fig.update_layout(

        mapbox_style="carto-positron",

        margin={
            "r":0,
            "t":60,
            "l":0,
            "b":0
        },

        height=700
    )

    return fig

# =========================================================
# GRÁFICO 2.3 - Top estaciones
# =========================================================

def plot_top_stations(df):

    top_stations = (
        df.groupby("start_station_name")
        .size()
        .nlargest(10)
        .sort_values()
        .reset_index(name="trips")
    )

    fig = px.bar(
        top_stations,
        x="trips",
        y="start_station_name",
        orientation="h",
        title="Top 10 Estaciones más usadas"
    )

    fig.update_layout(
        template=PLOT_TEMPLATE,
        title={"x": 0.5},
        xaxis_title="Viajes",
        yaxis_title="Estación",
        height=500
    )

    return fig

# ===========================================================================================================================================================================

# =========================================================
# graficas para analisis temporal
# =========================================================

# =========================================================
# GRÁFICO 3.1 - Viajes por día semana
# =========================================================

def plot_trips_by_weekday(df):

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    trips_weekday = (
        df.groupby("weekday")
        .size()
        .reindex(weekday_order)
        .reset_index(name="trips")
    )

    fig = px.bar(
        trips_weekday,
        x="weekday",
        y="trips",
        title="Viajes por Día de Semana"
    )

    fig.update_layout(
        template=PLOT_TEMPLATE,
        title={"x": 0.5},
        xaxis_title="Día",
        yaxis_title="Cantidad de viajes",
        height=450
    )

    return fig

# =========================================================
# GRÁFICO 3.2 - Duración por hora
# =========================================================

def plot_avg_duration_by_hour(df):

    duration_hour = (
        df.groupby("hour")["trip_duration_min"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        duration_hour,
        x="hour",
        y="trip_duration_min",
        markers=True,
        title="⏱Duración Promedio por Hora"
    )

    fig.update_layout(
        template=PLOT_TEMPLATE,
        title={"x": 0.5},
        xaxis_title="Hora",
        yaxis_title="Duración promedio (min)",
        height=450
    )

    return fig

# =========================================================
# GRÁFICO 3.3 - heatmap temporal
# =========================================================

def plot_temporal_heatmap(df):



    # =====================================================
    # ORDEN DE DÍAS
    # =====================================================

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    # =====================================================
    # AGRUPAR VIAJES
    # =====================================================

    heatmap_data = (
        df.groupby(["weekday", "hour"])
        .size()
        .reset_index(name="Cantidad de Viajes")
    )

    # =====================================================
    # ORDENAR DÍAS
    # =====================================================

    heatmap_data["weekday"] = pd.Categorical(
        heatmap_data["weekday"],
        categories=weekday_order,
        ordered=True
    )

    heatmap_data = heatmap_data.sort_values(
        ["weekday", "hour"]
    )

    # =====================================================
    # TABLA PIVOTE
    # =====================================================

    pivot_table = heatmap_data.pivot(

        index="weekday",

        columns="hour",

        values="Cantidad de Viajes"
    )

    # =====================================================
    # HEATMAP
    # =====================================================

    fig = px.imshow(

        pivot_table,

        aspect="auto",

        color_continuous_scale="YlOrRd",

        labels={
            "x": "Hora del Día",
            "y": "Día de la Semana",
            "color": "Cantidad de Viajes"
        },

        title="Intensidad Temporal de Viajes"
    )

    # =====================================================
    # PERSONALIZACIÓN HOVER
    # =====================================================

    fig.update_traces(

        hovertemplate=
        "<b>Día:</b> %{y}<br>" +
        "<b>Hora:</b> %{x}:00<br>" +
        "<b>Viajes:</b> %{z:,.0f}<br>" +
        "<extra></extra>"
    )

    # =====================================================
    # LAYOUT
    # =====================================================

    fig.update_layout(

        template="plotly_white",

        title={
            "x": 0.5,
            "xanchor": "center"
        },

        xaxis_title="Hora del Día",

        yaxis_title="Día de la Semana",

        height=500
    )

    return fig


# ===========================================================================================================================================================================

# =========================================================
# graficas para analisis de mobilidad
# =========================================================

# =========================================================
# GRÁFICO 4.1 - Top rutas
# =========================================================
def plot_top_routes(df):

    routes = (
        df.groupby([
            "start_station_name",
            "end_station_name"
        ])
        .size()
        .reset_index(name="Cantidad de Viajes")
    )

    routes["Ruta"] = ( "De :"+
        routes["start_station_name"]
        + " A: " +
        routes["end_station_name"]
    )

    top_routes = (
        routes
        .nlargest(10, "Cantidad de Viajes")
        .sort_values("Cantidad de Viajes")
    )

    fig = px.bar(

        top_routes,

        x="Cantidad de Viajes",

        y="Ruta",

        orientation="h",

        title="Top 10 Rutas"
    )

    fig.update_layout(

        template="plotly_white",

        title={
            "x": 0.5
        },

        xaxis_title="Cantidad de Viajes",

        yaxis_title="Ruta",

        height=600
    )

    return fig

# =========================================================
# GRÁFICO 4.2 - Sankey Diagram
# =========================================================
def plot_sankey_routes(df):

    import plotly.graph_objects as go

    routes = (
        df.groupby([
            "start_station_name",
            "end_station_name"
        ])
        .size()
        .reset_index(name="count")
        .nlargest(50, "count")
    )

    labels = list(

        set(routes["start_station_name"])

        .union(

            set(routes["end_station_name"])
        )
    )

    source = routes["start_station_name"].apply(
        labels.index
    )

    target = routes["end_station_name"].apply(
        labels.index
    )

    value = routes["count"]

    fig = go.Figure(

        data=[

            go.Sankey(

                node=dict(

                    pad=15,

                    thickness=20,

                    label=labels
                ),

                link=dict(

                    source=source,

                    target=target,

                    value=value
                )
            )
        ]
    )

    fig.update_layout(

        title_text="Flujo entre Estaciones",

        height=700
    )

    return fig


# =========================================================
# GRÁFICO 4.3 - Origen Destino Matrix
# =========================================================

def plot_od_matrix(df):

    od_matrix = (

        df.groupby([
            "start_station_name",
            "end_station_name"
        ]).size().reset_index(name="Cantidad de Viajes")
    )

    top_origins = (
        od_matrix.groupby("start_station_name")
        ["Cantidad de Viajes"].sum().nlargest(10).index
    )

    
    top_destinations = (

        od_matrix.groupby("end_station_name")
        ["Cantidad de Viajes"].sum().nlargest(10).index
    )

    od_matrix = od_matrix[
        od_matrix["start_station_name"]
        .isin(top_origins)
         &
        od_matrix["end_station_name"]
        .isin(top_destinations)
    ]

    pivot_table = od_matrix.pivot(

        index="start_station_name",

        columns="end_station_name",

        values="Cantidad de Viajes"
    )

    pivot_table = pivot_table.fillna(0)

    fig = px.imshow(

        pivot_table,

        aspect="auto",

        color_continuous_scale="Blues",

        labels={

            "x": "Destino",

            "y": "Origen",

            "color": "Viajes"
        },

        title="Matriz Origen-Destino"
    )

    fig.update_layout(

        template="plotly_white",

        title={
            "x": 0.5
        },

        height=700
    )

    return fig
# =========================================================
# GRÁFICO 4.4 - Distribución de distancias
# =========================================================

def plot_trip_distance_distribution(df):

    fig = px.histogram(

        df,

        x="trip_distance_km",

        nbins=50,

        title="Distribución de Distancias",

        marginal="box"
    )

    fig.update_layout(

        template="plotly_white",

        title={
            "x": 0.5
        },

        xaxis_title="Distancia (km)",

        yaxis_title="Cantidad de Viajes",

        height=500
    )

    return fig