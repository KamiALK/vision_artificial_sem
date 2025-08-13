# Install dependencies as needed:
# kagle_phone_model.py
# pip install kagglehub[pandas-datasets]

import pandas as pd

df = pd.read_csv(
    "/home/kami/proyectos/vision_artificial_sem/app/in_model/smartphones_data.csv.csv"
)

# Mostrar solo la columna 'name'
# obtencion de los nombres de los celulares
df_name = df[["Name"]]
print(df_name.head())
# print(df)

# Guardar como CSV
df_name.to_csv("smartphones_names.csv.csv", index=False)
