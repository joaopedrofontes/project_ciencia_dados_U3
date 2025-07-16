import pandas as pd

arquivo_csv = "../vacinacao_resumo_anual_final.csv"

chunk_size = 100000

total_linhas = 0

for chunk in pd.read_csv(arquivo_csv, sep=";", encoding="iso-8859-1", chunksize=chunk_size):
    total_linhas += len(chunk)

print(f"Total de linhas no arquivo '{arquivo_csv}': {total_linhas}")
