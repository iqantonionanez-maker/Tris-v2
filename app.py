import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------------
# CONFIGURACIÓN GENERAL
# ----------------------------------
st.set_page_config(
    page_title="Pronósticos Lucky - TRIS",
    layout="wide"
)

st.title("🎲 Pronósticos Lucky")
st.caption("Análisis estadístico basado en el histórico completo del TRIS")

# ----------------------------------
# CARGA DE DATOS
# ----------------------------------
RUTA_DATOS = "data/trishistorico.csv"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(RUTA_DATOS)

    # Normalizar columnas
    df.columns = [c.lower().strip() for c in df.columns]

    # Asegurar columnas necesarias
    columnas_esperadas = ["fecha", "hora", "sorteo", "numero"]
    df = df[columnas_esperadas]

    # Tipos correctos
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["numero"] = df["numero"].astype(str).str.zfill(5)

    return df.sort_values("fecha", ascending=False)

df = cargar_datos()

# ----------------------------------
# SIDEBAR
# ----------------------------------
st.sidebar.header("⚙️ Configuración")

ventana = st.sidebar.selectbox(
    "Sorteos a analizar",
