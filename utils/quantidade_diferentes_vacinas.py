import pandas as pd

arquivo_origem = "../datasets/vacinacao_final.csv"

chunk_size = 100000

valores_unicos = set()

# Lendo em partes
for chunk in pd.read_csv(arquivo_origem, sep=";", encoding="UTF-8", usecols=["ds_vacina"], chunksize=chunk_size):

    valores_unicos.update(chunk["ds_vacina"].dropna().unique())

print("Quantidade de valores únicos em 'sg_vacina':", len(valores_unicos))
print(valores_unicos)