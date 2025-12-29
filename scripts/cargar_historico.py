import pandas as pd
import requests
from datetime import datetime

# FUENTE PÚBLICA (no gubernamental)
URL = "https://api.allorigins.win/raw?url=https://www.pronosticos.gob.mx/Resultados/Tris"

def obtener_datos():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data

def procesar(data, limite=1000):
    filas = []

    for item in data[:limite]:
        filas.append({
            "fecha": item.get("fecha"),
            "hora": item.get("hora"),
            "sorteo": item.get("sorteo"),
            "numero": str(item.get("resultado")).zfill(5)
        })

    return pd.DataFrame(filas)

def main():
    data = obtener_datos()
    df = procesar(data)

    df.to_csv("data/tris.csv", index=False)
    print(f"✔ {len(df)} sorteos guardados")

if __name__ == "__main__":
    main()
