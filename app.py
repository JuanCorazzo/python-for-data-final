import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Análisis de Transacciones por Adquiriente")

df = pd.read_csv("data/processed/transacciones_app.csv")

# --- Sidebar ---
st.sidebar.markdown("## Filtros")
st.sidebar.markdown("Usá el slider para filtrar las transacciones por importe.")

importe_min = int(df["Importe"].min())
importe_max = int(df["Importe"].max())

rango = st.sidebar.slider(
    "Rango de Importe",
    min_value=importe_min,
    max_value=importe_max,
    value=(importe_min, importe_max)
)

df_filtrado = df[(df["Importe"] >= rango[0]) & (df["Importe"] <= rango[1])]

st.markdown(f"**Transacciones mostradas:** {len(df_filtrado):,} de {len(df):,}")

# --- Resumen descriptivo ---
st.subheader("Resumen Descriptivo")

col1, col2, col3 = st.columns(3)
col1.metric("Media", f"{df_filtrado['Importe'].mean():,.0f}")
col2.metric("Mediana", f"{df_filtrado['Importe'].median():,.0f}")
col3.metric("Rango", f"{df_filtrado['Importe'].max() - df_filtrado['Importe'].min():,.0f}")

st.dataframe(df_filtrado["Importe"].describe().to_frame().T.round(2))

# --- Histograma del target ---
st.subheader("Distribución por Adquiriente")

fig_hist = px.histogram(
    df_filtrado,
    x="acquirer",
    color="acquirer",
    title="Cantidad de transacciones por Adquiriente",
    labels={"acquirer": "Adquiriente", "count": "Cantidad"},
    color_discrete_map={"COSMIC": "#636EFA", "INDIE": "#EF553B"}
)
st.plotly_chart(fig_hist, use_container_width=True)

# --- Scatter plot ---
st.subheader("Importe por Adquiriente y País")

fig_scatter = px.scatter(
    df_filtrado,
    x="Importe",
    y="country",
    color="acquirer",
    title="Distribución de Importes por País y Adquiriente",
    labels={"Importe": "Importe de la transacción", "country": "País", "acquirer": "Adquiriente"},
    color_discrete_map={"COSMIC": "#636EFA", "INDIE": "#EF553B"},
    opacity=0.4,
    category_orders={"country": sorted(df_filtrado["country"].unique())}
)
st.plotly_chart(fig_scatter, use_container_width=True)

