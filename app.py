import streamlit as st
from utils import (
    load_data, ultimos_juegos, numero_fuerte,
    calientes_frios, consulta_numero, calcular_ganancia
)

st.set_page_config(page_title="Pronósticos Lucky", layout="centered")

df = load_data()
df_150 = ultimos_juegos(df)

st.title("🎲 Pronósticos Lucky")
st.caption("Análisis del TRIS – últimos 1000 sorteos")

# ---------- NÚMERO FUERTE ----------
st.header("⭐ Número fuerte por sorteo")
sorteo = st.selectbox("Selecciona sorteo", df["sorteo"].unique())
num, veces = numero_fuerte(df_150, sorteo)

if num:
    st.success(f"🎯 Número fuerte: {num} (salió {veces} veces)")

# ---------- CALIENTES Y FRÍOS ----------
st.header("🔥❄️ Números calientes y fríos")
calientes, frios = calientes_frios(df_150)

st.write("🔥 Calientes")
st.write(list(calientes.index))

st.write("❄️ Fríos")
st.write(list(frios.index))

# ---------- CONSULTA ----------
st.header("🔎 Consulta por número")
numero = st.text_input("Número (1 a 5 cifras)")

if numero:
    info = consulta_numero(df_150, numero)
    if not info:
        st.warning("Este número no ha salido en los últimos 150 sorteos")
    else:
        st.write(f"Salió {info['total']} veces")
        st.write(f"Última vez: {info['ultima_fecha']}")
        st.write("Por sorteo:")
        st.write(info["por_sorteo"])

# ---------- SIMULADOR ----------
st.header("💰 Simulador de apuesta")
tipo = st.selectbox("Tipo de jugada", [
    "Directa 5", "Directa 4", "Directa 3",
    "Par Inicial", "Par Final",
    "Número Inicial", "Número Final"
])

monto = st.number_input("Monto ($)", min_value=1)
multiplicador = st.number_input("Multiplicador ($)", min_value=0)

if st.button("Calcular"):
    ganancia = calcular_ganancia(tipo, monto, multiplicador)
    st.success(f"🏆 Ganancia total: ${ganancia:,}")
    st.caption("🍀 Pronósticos Lucky te desea mucha suerte")
