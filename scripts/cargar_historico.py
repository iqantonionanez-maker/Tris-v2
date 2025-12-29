
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

URL = "https://www.loterianacional.gob.mx/Tris/resultados"

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if table is None:
        raise Exception("No se encontró la tabla de resultados")

    df = pd.read_html(StringIO(str(table)))[0]

    df.to_csv("data/tris.csv", index=False)
    print("CSV actualizado correctamente")

if __name__ == "__main__":
    main()
