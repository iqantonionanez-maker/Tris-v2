import streamlit as st
import pandas as pd
from collections import Counter
import random

# =====================
# CONFIGURACIÓN
# =====================
st.set_page_config(
    page_title="Pronósticos Lucky – TRIS",
    layout="centered"
)

st.title("🎲 Pronósticos Lucky – TRIS")
st.caption("Apoyo estadístico basado en resultados reales")
st.divider()

# =====================
# CARGA DE DATOS
# =====================
@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/tris_limpio.csv")
    df["numero"] = df["numero"].astype(str).str.zfill(5)
    return df

df = cargar_datos()

st.success(f"Base activa con {len(df)} sorteos")

# =====================
# USAR ÚLTIMOS 1000
# =====================
df_analisis = df.tail(1000)

# =====================
# FUNCIONES
# =====================
def es_escalera(num):
    return all(int(num[i])+1 == int(num[i+1]) for i in range(len(num)-1))

def es_piramide(num):
    return num == num[::-1]

def lenguaje_comercial():
    frases = [
        "🍀 Este número está fuerte hoy",
        "⭐ Buena opción para este sorteo",
        "🔥 Viene saliendo seguido",
        "🎯 Muchos jugadores lo están usando",
        "👀 Número que no hay que perder de vista"
    ]
    return random.choice(frases)

# =====================
# 🔥❄️ CALIENTES Y FRÍOS
# =====================
st.header("🔥❄️ Números calientes y fríos")

conteo = Counter(df_analisis["numero"])

calientes = conteo.most_common(7)
frios = conteo.most_common()[:-8:-1]

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Calientes")
    for n, v in calientes:
        st.write(f"**{n}** — {lenguaje_comercial()}")

with col2:
    st.subheader("❄️ Fríos")
    for n, v in frios:
        st.write(f"**{n}** — Poco movimiento reciente")

# =====================
# 🧗 ESCALERAS / PIRÁMIDES
# =====================
st.header("🧗 Escaleras y pirámides recomendadas")

escaleras = [n for n in conteo if es_escalera(n)]
piramides = [n for n in conteo if es_piramide(n)]

st.subheader("🧗 Escaleras fuertes")
st.write(escaleras[:7])

st.subheader("🔺 Pirámides fuertes")
st.write(piramides[:7])

# =====================
# 🎯 TOP 7 RECOMENDADAS
# =====================
st.header("🎯 Top 7 combinaciones recomendadas")

top7 = [n for n, _ in calientes][:5]
if escaleras:
    top7.append(escaleras[0])
if piramides:
    top7.append(piramides[0])

for i, n in enumerate(top7, 1):
    st.write(f"{i}️⃣ **{n}** — {lenguaje_comercial()}")

# =====================
# ⏰ RECOMENDACIÓN POR HORARIO
# =====================
st.header("⏰ Número fuerte por sorteo")

sorteos = df_analisis["tipo"].unique()

for s in sorteos:
    sub = df_analisis[df_analisis["tipo"] == s]
    if len(sub) > 0:
        fuerte = sub["numero"].value_counts().idxmax()
        veces = sub["numero"].value_counts().max()
        st.success(
            f"⭐ **{s}** → {fuerte} (salió {veces} veces)\n\n{lenguaje_comercial()}"
        )

# =====================
# 🔎 CONSULTA POR NÚMERO
# =====================
st.header("🔎 Consulta por número")

num_usuario = st.text_input("Número (1 a 5 cifras)")

if num_usuario:
    sub = df_analisis[df_analisis["numero"].str.contains(num_usuario)]

    if len(sub) == 0:
        st.warning("Este número no ha salido recientemente")
    else:
        ultima = sub.iloc[-1]
        st.success(
            f"""
Este número salió **{len(sub)} veces** en los últimos 1000 sorteos  
📅 Última vez: {ultima['fecha']}  
🕒 Sorteo: {ultima['tipo']}
"""
        )

        st.subheader("📊 Apariciones por sorteo")
        st.write(sub["tipo"].value_counts())

# =====================
# 💰 SIMULADOR OFICIAL TRIS
# =====================
st.header("💰 Simulador de apuesta")

tipo_jugada = st.selectbox(
    "Tipo de jugada",
    [
        "Número inicial",
        "Número final",
        "Par inicial",
        "Par final",
        "Directa 3",
        "Directa 4",
        "Directa 5"
    ]
)

apuesta = st.number_input("Monto apostado ($)", min_value=1, value=5)
multiplicador = st.number_input("Monto al multiplicador ($)", min_value=0, value=0)

pagos = {
    "Número inicial": 5,
    "Número final": 5,
    "Par inicial": 50,
    "Par final": 50,
    "Directa 3": 500,
    "Directa 4": 5000,
    "Directa 5": 50000
}

ganancia = (apuesta + multiplicador) * pagos[tipo_jugada]

st.success(f"💵 Podrías ganar **${ganancia:,.0f}**")
st.caption("🍀 Pronósticos Lucky te desea mucha suerte")

# =====================
# 📊 HISTORIAL
# =====================
st.header("📊 Últimos resultados")
st.dataframe(df.tail(20), use_container_width=True)
