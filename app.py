import streamlit as st
import pandas as pd
from utils import (
    contar_frecuencias,
    numeros_calientes_frios,
    analizar_numero
)

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
st.set_page_config(
    page_title="Pronósticos Lucky - TRIS",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 Pronósticos Lucky - TRIS")
st.caption("Análisis inteligente para jugadores de TRIS")

# -----------------------------
# CARGAR DATOS
# -----------------------------
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/tris.csv", dtype={"numero": str})

df = cargar_datos()

# -----------------------------
# SECCIÓN 1: CONSULTA POR NÚMERO
# -----------------------------
st.header("🔎 Consulta por número")

numero_usuario = st.text_input(
    "Número (1 a 5 cifras)",
    max_chars=5
)

if numero_usuario:
    numero_usuario = numero_usuario.zfill(5)
    resultado = analizar_numero(numero_usuario, df)

    st.subheader("📊 Resultados")
    st.json(resultado)
