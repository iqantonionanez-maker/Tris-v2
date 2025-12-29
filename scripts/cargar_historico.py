import pandas as pd

# Cargar el CSV crudo
df = pd.read_csv("data/tris.csv", header=None)

registros = []

fecha = None

for i in range(len(df)):
    fila = df.iloc[i].astype(str).tolist()

    if "Fecha" in fila[0]:
        fecha = fila[0].replace("Fecha", "").strip()
        continue

    if fila[0].isdigit() and len(fila[0]) >= 4:
        sorteo = fila[0]
        tipo = fila[1]
        numero = fila[2]

        registros.append({
            "fecha": fecha,
            "sorteo": sorteo,
            "tipo": tipo,
            "numero": numero
        })

# DataFrame limpio
df_limpio = pd.DataFrame(registros)

# Guardar CSV limpio
df_limpio.to_csv("data/tris_limpio.csv", index=False)

print("✅ CSV limpio generado correctamente")
print(df_limpio.head())
