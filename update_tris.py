
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os

URL = "https://trisresultados.com/"

def obtener_resultados():
    response = requests.get(URL, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")

    sorteos = {
        "Medio Día": "Tris Medio Día",
        "De las 3": "Tris de las 3",
        "Extra": "Tris Extra",
        "De las 7": "Tris de las 7",
        "Clásico": "Tris Clásico"
    }

    resultados = []
    fecha = datetime.now().strftime("%Y-%m-%d")

    for nombre, texto in sorteos.items():
        seccion = soup.find("h3", string=lambda t: t and texto in t)
        if not seccion:
            continue

        numeros = seccion.find_next("div").text.strip().replace(" ", "")
        if len(numeros) != 5:
            continue

        resultados.append({
            "fecha": fecha,
            "sorteo": nombre,
            "numero": numeros
        })

    return resultados

def guardar_csv(nuevos):
    os.makedirs("data", exist_ok=True)
    archivo = "data/tris.csv"

    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
    else:
        df = pd.DataFrame(columns=["fecha", "sorteo", "numero"])

    df_nuevo = pd.DataFrame(nuevos)
    df_final = pd.concat([df, df_nuevo]).drop_duplicates()
    df_final.to_csv(archivo, index=False)

if __name__ == "__main__":
    datos = obtener_resultados()
    if datos:
        guardar_csv(datos)
