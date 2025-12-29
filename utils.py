import pandas as pd

# ---------- CARGA DE DATOS ----------
def load_data():
    df = pd.read_csv("data/tris.csv")
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["numero"] = df["numero"].astype(str).str.zfill(5)
    return df


# ---------- ÚLTIMOS N SORTEOS ----------
def ultimos_juegos(df, n=150):
    return df.sort_values("fecha", ascending=False).head(n)


# ---------- FRECUENCIAS ----------
def conteo_numeros(df):
    return df["numero"].value_counts()


# ---------- NÚMERO FUERTE POR SORTEO ----------
def numero_fuerte(df, sorteo):
    d = df[df["sorteo"] == sorteo]
    conteo = d["numero"].value_counts()
    if conteo.empty:
        return None, 0
    return conteo.idxmax(), conteo.max()


# ---------- CALIENTES Y FRÍOS ----------
def calientes_frios(df, top=7):
    conteo = df["numero"].value_counts()
    calientes = conteo.head(top)
    frios = conteo.tail(top)
    return calientes, frios


# ---------- CONSULTA POR NÚMERO ----------
def consulta_numero(df, numero):
    numero = str(numero).zfill(5)
    d = df[df["numero"] == numero]

    if d.empty:
        return None

    return {
        "total": len(d),
        "ultima_fecha": d["fecha"].max().date(),
        "por_sorteo": d["sorteo"].value_counts()
    }


# ---------- TABLA DE PREMIOS OFICIAL ----------
PAGOS = {
    "Directa 5": 50000,
    "Directa 4": 5000,
    "Directa 3": 500,
    "Par Inicial": 50,
    "Par Final": 50,
    "Número Inicial": 5,
    "Número Final": 5,
}


def calcular_ganancia(tipo, monto, multiplicador):
    premio_base = PAGOS.get(tipo, 0) * monto
    premio_multi = multiplicador * PAGOS.get(tipo, 0) if multiplicador > 0 else 0
    return premio_base + premio_multi
