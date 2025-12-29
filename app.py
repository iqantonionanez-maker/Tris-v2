import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRIS Predictor", layout="wide")

st.title("🎲 TRIS – Análisis y Calculadora")
st.caption("Datos históricos automáticos")

# =====================
# CARGAR DATOS
# =====================
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/tris.csv")

df = cargar_datos()

st.success(f"Registros cargados: {len(df)}")

# Normalizar columna
df.columns = [c.lower() for c in df.columns]

# Detectar columna de número ganador
col_numero = None
for c in df.columns:
    if "combin" in c or "ganador" in c or "numero" in c:
        col_numero = c
        break

if col_numero is None:
    st.error("No se encontró la columna del número ganador")
    st.stop()

df["numero"] = df[col_numero].astype(str).str.zfill(5)

# =====================
# BUSCADOR
# =====================
st.divider()
st.subheader("🔎 Buscar número")

numero_usuario = st.text_input(
    "Ingresa número (1 a 5 dígitos)",
    max_chars=5
)

def clasificar(numero, buscado):
    numero = str(numero)
    buscado = str(buscado)

    if numero == buscado.zfill(5):
        return "🎯 Directa exacta"
    elif numero.startswith(buscado):
        return "🔢 Inicial"
    elif numero.endswith(buscado):
        return "🔢 Final"
    elif buscado in numero:
        return "🧩 Parcial"
    else:
        return "—"

if numero_usuario:
    resultados = df[df["numero"].str.contains(numero_usuario)].copy()

    if len(resultados) > 0:
        resultados["Tipo de jugada"] = resultados["numero"].apply(
            lambda x: clasificar(x, numero_usuario)
        )

        st.success(f"Coincidencias encontradas: {len(resultados)}")
        st.dataframe(
            resultados[["numero", "Tipo de jugada"]],
            use_container_width=True
        )
    else:
        st.warning("No se encontraron coincidencias")

# =====================
# CALCULADORA
# =====================
st.divider()
st.subheader("💰 Calculadora de premios")

monto = st.number_input(
    "Monto apostado ($)",
    min_value=1,
    value=10,
    step=1
)

tipo = st.selectbox(
    "Tipo de jugada",
    [
        "🎯 Directa exacta",
        "🔢 Inicial",
        "🔢 Final",
        "🧩 Parcial"
    ]
)

multiplicadores = {
    "🎯 Directa exacta": 500,
    "🔢 Inicial": 50,
    "🔢 Final": 50,
    "🧩 Parcial": 10
}

ganancia = monto * multiplicadores[tipo]

st.info(f"💵 Ganancia potencial: **${ganancia}**")

# =====================
# MOSTRAR HISTÓRICO
# =====================
st.divider()
st.subheader("📊 Historial TRIS (últimos registros)")
st.dataframe(df.tail(20), use_container_width=True)
