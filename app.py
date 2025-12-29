import streamlit as st
from utils import (
    load_data,
    analizar_numero,
    numeros_calientes,
    calcular_premio
)

st.set_page_config(page_title="Pronósticos Lucky", layout="centered")

df = load_data()

st.title("🎲 Pronósticos Lucky – TRIS")
st.caption("Análisis inteligente para jugadores de TRIS")

# =========================
# CONSULTA POR NUMERO
# =========================

st.header("🔎 Consulta por número")

numero = st.text_input("Número (1 a 5 cifras)").strip()

tipo_opciones = {
    1: ["Numero Inicial", "Numero Final"],
    2: ["Par Inicial", "Par Final"],
    3: ["Directa 3"],
    4: ["Directa 4"],
    5: ["Directa 5"]
}

tipo = None

if numero.isdigit() and 1 <= len(numero) <= 5:
    tipo = st.selectbox(
        "Tipo de jugada",
        tipo_opciones[len(numero)]
    )

if numero and tipo:
    info = analizar_numero(df, numero, tipo)

    if not info:
        st.warning("Este número no ha salido en la base de datos")
    else:
        st.success(f"📊 Salió {info['total']} veces")
        st.write(f"📅 Última vez: {info['ultima_fecha']} – {info['ultima_hora']}")
        st.write(f"🎯 Sorteo: {info['ultimo_sorteo']}")
        st.write("📍 Apariciones por sorteo:")
        st.write(info["por_sorteo"])

# =========================
# NUMEROS CALIENTES Y FRIOS
# =========================

st.header("🔥❄️ Números calientes y fríos")

tipo_calor = st.selectbox(
    "Tipo de análisis",
    ["Numero Final", "Par Final", "Directa 3"]
)

calientes, frios = numeros_calientes(df, tipo_calor)

st.write("🔥 Calientes:", calientes)
st.write("❄️ Fríos:", frios)

# =========================
# SIMULADOR
# =========================

st.header("💰 Simulador de apuesta")

apuesta_base = st.number_input("Apuesta base ($)", min_value=0, value=5)
apuesta_multi = st.number_input("Apuesta multiplicador ($)", min_value=0, value=0)

if st.button("Calcular premio") and numero and tipo:
    base, multi, total = calcular_premio(tipo, apuesta_base, apuesta_multi)
    st.success(f"💵 Premio base: ${base:,.0f}")
    st.success(f"💵 Premio multiplicador: ${multi:,.0f}")
    st.success(f"🎉 Total posible a ganar: ${total:,.0f}")
    st.caption("🍀 Pronósticos Lucky te desea mucha suerte")
