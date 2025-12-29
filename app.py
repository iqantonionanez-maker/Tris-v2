import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lucky TRIS", layout="centered")

st.title("🍀 Lucky TRIS")
st.write("Análisis y apoyo para el juego TRIS (Lotería Nacional)")

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/tris_limpio.csv")

df = cargar_datos()

st.success(f"Datos cargados: {len(df)} sorteos")

st.divider()

# Mostrar últimos resultados
st.subheader("📊 Últimos resultados")
st.dataframe(df.tail(10), use_container_width=True)

st.divider()

# Selección de número
st.subheader("🎯 Revisión de número")

numero_usuario = st.text_input(
    "Ingresa un número (2 a 5 cifras)",
    max_chars=5
)

if numero_usuario:
    resultados = df[df["numero"].astype(str).str.contains(numero_usuario)]

    if len(resultados) > 0:
        st.success(f"Coincidencias encontradas: {len(resultados)}")
        st.dataframe(resultados, use_container_width=True)
    else:
        st.warning("No se encontraron coincidencias")
