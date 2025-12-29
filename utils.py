import pandas as pd

def cargar_tris():
    df = pd.read_csv("data/tris.csv")

    # Asegurar 5 cifras
    df["numero"] = df["numero"].astype(str).str.zfill(5)

    # Directas
    df["directa_5"] = df["numero"]
    df["directa_4"] = df["numero"].str[-4:]
    df["directa_3"] = df["numero"].str[-3:]

    # Iniciales y finales
    df["par_inicial"] = df["numero"].str[:2]
    df["par_final"] = df["numero"].str[-2:]
    df["num_inicial"] = df["numero"].str[0]
    df["num_final"] = df["numero"].str[-1]

    return df
