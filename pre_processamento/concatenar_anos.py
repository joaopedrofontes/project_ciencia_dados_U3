import pandas as pd
import glob

ano = 2024

padrao_arquivos = f"vacinacao_resumo_anual_*.csv"

arquivo_anual = f"vacinacao_final.csv"

chunk_size = 100000


arquivos_mensais = glob.glob(padrao_arquivos)

dfs = []

for arquivo in arquivos_mensais:
    print(f"Processando arquivo: {arquivo}")

    for chunk in pd.read_csv(arquivo, sep=";", chunksize=chunk_size):
        dfs.append(chunk)

df_anual = pd.concat(dfs, ignore_index=True)

df_anual.sort_values(
    by=["no_municipio_paciente", "uf", "ds_vacina", "faixa_etaria"],
    inplace=True
)

df_anual.to_csv(arquivo_anual, sep=";", index=False, encoding="utf-8")

print("\nArquivo anual gerado com sucesso:", arquivo_anual)
print(f"Total de registros: {len(df_anual):,}")
print(f"Arquivos combinados: {len(arquivos_mensais)}")