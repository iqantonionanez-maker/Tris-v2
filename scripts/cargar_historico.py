import csv
import requests
from datetime import datetime, timedelta

URL = "https://www.pronosticos.gob.mx/Documentos/Historicos/Tris.csv"
OUTPUT = "data/tris.csv"

def main():
    r = requests.get(URL)
    r.raise_for_status()

    lines = r.text.splitlines()

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["fecha", "hora", "sorteo", "numero"])

        for line in lines[1:]:
            cols = line.split(",")
            if len(cols) >= 4:
                writer.writerow(cols[:4])

    print("Histórico TRIS cargado correctamente")

if __name__ == "__main__":
    main()
