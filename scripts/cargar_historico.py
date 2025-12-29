import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL de resultados históricos (no oficial, fácil de leer)
URL = "https://www.loteriasyapuestas.mx/resultados-tris-historicos"

def cargar_historico():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    filas = []

    tabla = soup.find("table")
    if not tabla:
        print("No se encontró la tabla")
        return

    for row in tabla.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        fecha = cols[0].text.strip()
        sorteo = cols[1].text.strip()
        hora = cols[2].text.strip()
        numero = cols[3].text.strip().zfill(5)

        filas.append([fecha, hora, sorteo, numero])

    df = pd.DataFrame(filas, columns=["fecha", "hora", "sorteo", "numero"])

    df.to_csv("data/tris.csv", index=False)
    print(f"Histórico cargado: {len(df)} sorteos")

if __name__ == "__main__":
    cargar_historico()
