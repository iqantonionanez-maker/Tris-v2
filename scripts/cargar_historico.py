import pandas as pd
import requests

URL = "https://api.allorigins.win/raw?url=https://www.lotterycorner.com/mx/tris/results"

def main():
    tablas = pd.read_html(URL)
    df = tablas[0]

    df.columns = ["fecha", "hora", "sorteo", "numero"]

    df["numero"] = df["numero"].astype(str).str.zfill(5)

    df = df.head(1000)

    df.to_csv("data/tris.csv", index=False)
    print(f"✔ {len(df)} sorteos guardados")

if __name__ == "__main__":
    main()
