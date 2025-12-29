
import streamlit as st
import pandas as pd
from collections import Counter

# =====================
# CONFIGURACIÓN
# =====================
st.set_page_config(
    page_title="Pronósticos Lucky - TRIS",
    layout="centered"
)

st.title("🎲 Pronósticos Lucky – TRIS")
st.caption("Análisis estadístico basado en resultados reales")
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

st.success(f"Base cargada: {len(df)} sorteos")

# =====================
# FILTRO ÚLTIMOS 150
# =====================
df_150 = df.tail(150)

# =====================
# FUNCIONES ÚTILES
# =====================
def tipo_jugada(numero, jugada):
    if jugada == numero:
        return "Directa 5"
    if numero.endswith(jugada):
        if len(jugada) == 2:
            return "Par final"
        return "Número final"
    if numero.startswith(jugada):
        if len(jugada) == 2:
            return "Par inicial"
        return "Número inicial"
    if jugada in numero:
        if len(jugada) == 3:
            return "Directa 3"
        if len(jugada) == 4:
            return "Directa 4"
    return "No aplica"

# =====================
# 🔥 NÚMEROS CALIENTES / FRÍOS
# =====================
st.header("🔥❄️ Números calientes y fríos (últimos 150)")

conteo = Counter(df_150["numero"])

calientes = conteo.most_common(7)
frios = conteo.most_common()[:-8:-1]

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Calientes")
    st.write(calientes)

with col2:
    st.subheader("❄️ Fríos")
    st.write(frios)

# =====================
# 🧗 ESCALERAS Y PIRÁMIDES
# =====================
st.header("🧗 Escaleras y pirámides recomendadas")

def es_escalera(num):
    return all(int(num[i])+1 == int(num[i+1]) for i in range(len(num)-1))

def es_piramide(num):
    return num == num[::-1]

escaleras = [n for n in conteo if es_escalera(n)]
piramides = [n for n in conteo if es_piramide(n)]

st.subheader("🧗 Escaleras (top 7)")
st.write(escaleras[:7])

st.subheader("🔺 Pirámides (top 7)")
st.write(piramides[:7])

# =====================
# 🎯 TOP 7 COMBINACIONES
# =====================
st.header("🎯 Top 7 combinaciones sugeridas")

top7 = [n for n, _ in calientes][:5]
top7 += escaleras[:1]
top7 += piramides[:1]

st.write(top7)

# =====================
# 🔎 CONSULTA POR NÚMERO
# =====================
st.header("🔎 Consulta por número")

numero_usuario = st.text_input("Ingresa un número (1 a 5 cifras)")

if numero_usuario:
    numero_usuario = numero_usuario.zfill(len(numero_usuario))
    sub = df_150[df_150["numero"].str.contains(numero_usuario)]

    if len(sub) == 0:
        st.warning("Este número no ha salido en los últimos 150 sorteos")
    else:
        st.success(f"Salió {len(sub)} veces en los últimos 150 sorteos")

        ultima = sub.iloc[-1]

        st.write(f"📅 Última vez: {ultima['fecha']}")
        st.write(f"🕒 Sorteo: {ultima['tipo']}")

        por_sorteo = sub["tipo"].value_counts()
        st.subheader("📊 Por sorteo")
        st.write(por_sorteo)

# =====================
# 💰 CALCULADORA OFICIAL TRIS
# =====================
st.header("💰 Simulador de apuesta oficial")

tipo = st.selectbox(
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

ganancia = (apuesta + multiplicador) * pagos[tipo]

st.success(f"💵 Ganancia potencial: ${ganancia:,.0f}")
st.caption("🍀 Pronósticos Lucky te desea mucha suerte")

# =====================
# 📊 HISTORIAL
# =====================
st.header("📊 Últimos resultados")
st.dataframe(df.tail(20), use_container_width=True)
