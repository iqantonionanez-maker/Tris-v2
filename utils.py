import pandas as pd
from collections import Counter

# =========================
# TABLAS OFICIALES DE PAGOS
# =========================

PAGOS_BASE = {
    "Numero Inicial": 5,
    "Numero Final": 5,
    "Par Inicial": 50,
    "Par Final": 50,
    "Directa 3": 500,
    "Directa 4": 5000,
    "Directa 5": 50000,
}

PAGOS_MULTIPLICADOR = {
    "Numero Inicial": 20,
    "Numero Final": 20,
    "Par Inicial": 200,
    "Par Final": 200,
    "Directa 3": 2000,
    "Directa 4": 20000,
    "Directa 5": 200000,
}

# =========================
# CARGA DE DATOS
# =========================

def load_data():
    df = pd.read_csv("data/tris.csv", dtype={"numero": str})
    df["numero"] = df["numero"].str.zfill(5)
    return df

# =========================
# UTILIDADES DE ANALISIS
# =========================

def extraer_numero(numero, tipo):
    if tipo == "Numero Inicial":
        return numero[0]
    if tipo == "Numero Final":
        return numero[-1]
    if tipo == "Par Inicial":
        return numero[:2]
    if tipo == "Par Final":
        return numero[-2:]
    if tipo == "Directa 3":
        return numero[-3:]
    if tipo == "Directa 4":
        return numero[-4:]
    if tipo == "Directa 5":
        return numero

def analizar_numero(df, numero_usuario, tipo):
    df["comparado"] = df["numero"].apply(lambda x: extraer_numero(x, tipo))
    sub = df[df["comparado"] == numero_usuario]

    if sub.empty:
        return None

    return {
        "total": len(sub),
        "ultima_fecha": sub.iloc[-1]["fecha"],
        "ultima_hora": sub.iloc[-1]["hora"],
        "ultimo_sorteo": sub.iloc[-1]["sorteo"],
        "por_sorteo": sub["sorteo"].value_counts().to_dict()
    }

def numeros_calientes(df, tipo, top=7):
    df["comparado"] = df["numero"].apply(lambda x: extraer_numero(x, tipo))
    conteo = Counter(df["comparado"])
    calientes = conteo.most_common(top)
    frios = conteo.most_common()[:-top-1:-1]
    return calientes, frios

# =========================
# SIMULADOR DE APUESTAS
# =========================

def calcular_premio(tipo, apuesta_base, apuesta_multi):
    premio_base = apuesta_base * PAGOS_BASE[tipo]
    premio_multi = apuesta_multi * PAGOS_MULTIPLICADOR[tipo]
    total = premio_base + premio_multi
    return premio_base, premio_multi, total
