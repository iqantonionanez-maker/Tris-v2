import pandas as pd
from datetime import datetime

ARCHIVO_HISTORICO = "data/trishistorico.csv"

def main():
    print("Iniciando actualización TRIS...")

    # Leer histórico existente
    try:
        df = pd.read_csv(ARCHIVO_HISTORICO)
        print(f"Histórico cargado: {len(df)} sorteos")
    except FileNotFoundError:
        print("No existe histórico, creando uno nuevo")
        df = pd.DataFrame()

    # 🔒 POR AHORA: solo validamos que el workflow funcione
    # (más adelante conectamos la extracción web segura)

    df["ultima_actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df.to_csv(ARCHIVO_HISTORICO, index=False)
    print("Histórico guardado correctamente")

if __name__ == "__main__":
    main()
