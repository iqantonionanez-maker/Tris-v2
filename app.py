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
    [150, 500, 1000, "Todos"],
    index=2
)

if ventana != "Todos":
    df_analisis = df.head(int(ventana))
else:
    df_analisis = df.copy()

# ----------------------------------
# MÉTRICAS GENERALES
# ----------------------------------
st.subheader("📊 Resumen general")

col1, col2, col3 = st.columns(3)
col1.metric("Total sorteos históricos", len(df))
col2.metric("Sorteos analizados", len(df_analisis))

sorteos_anuales = df["fecha"].dt.year.value_counts().mean()
col3.metric("Promedio sorteos por año", int(sorteos_anuales))

# ----------------------------------
# NÚMEROS CALIENTES Y FRÍOS
# ----------------------------------
st.subheader("🔥❄️ Números calientes y fríos")

conteo = df_analisis["numero"].value_counts()

calientes = conteo.head(7)
frios = conteo.tail(7)

col1, col2 = st.columns(2)
col1.markdown("### 🔥 Calientes")
col1.dataframe(calientes)

col2.markdown("### ❄️ Fríos")
col2.dataframe(frios)

st.caption(f"Basado en los últimos {len(df_analisis)} sorteos")

# ----------------------------------
# ANÁLISIS POR SORTEO
# ----------------------------------
st.subheader("🎯 Frecuencia por sorteo")

por_sorteo = (
    df_analisis
    .groupby(["sorteo", "numero"])
    .size()
    .reset_index(name="veces")
)

st.dataframe(
    por_sorteo.sort_values("veces", ascending=False).head(20)
)

# ----------------------------------
# CONSULTA POR NÚMERO
# ----------------------------------
st.subheader("🔎 Consulta por número")

numero_consulta = st.text_input("Número (1 a 5 cifras)")

if numero_consulta:
    numero_consulta = numero_consulta.zfill(5)
    sub = df[df["numero"] == numero_consulta]

    if sub.empty:
        st.warning("Este número no ha salido en el histórico")
    else:
        st.success(f"📌 El número {numero_consulta} ha salido {len(sub)} veces")
        st.write("Última vez:")
        st.write(sub.iloc[0][["fecha", "hora", "sorteo"]])

        st.write("Frecuencia por sorteo:")
        st.dataframe(sub["sorteo"].value_counts())

# ----------------------------------
# SIMULADOR DE APUESTA
# ----------------------------------
st.subheader("💰 Simulador de apuesta")

tipo_juego = st.selectbox(
    "Tipo de jugada",
    [
        "Número final / inicial",
        "Par inicial / final",
        "Directa 3",
        "Directa 4",
        "Directa 5"
    ]
)

apuesta = st.number_input("Monto apostado ($)", min_value=1, value=5)
multiplicador = st.number_input(
    "Monto al multiplicador (0 si no juega)",
    min_value=0,
    value=0
)

pagos = {
    "Número final / inicial": 5,
    "Par inicial / final": 50,
    "Directa 3": 500,
    "Directa 4": 5000,
    "Directa 5": 50000
}

if st.button("Calcular premio"):
    base = pagos[tipo_juego]
    premio = apuesta * base

    if multiplicador > 0:
        premio += multiplicador * base * 3

    st.success(f"💵 Premio posible: ${premio:,.0f}")
    st.caption("🍀 Pronósticos Lucky te desea mucha suerte")

# ----------------------------------
# HISTÓRICO
# ----------------------------------
st.subheader("📄 Vista del histórico")
st.dataframe(df_analisis.head(50))
