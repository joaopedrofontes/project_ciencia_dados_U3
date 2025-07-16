import pandas as pd


mes = "dez"
ano = 2024

arquivo_origem = f"vacinacao_{mes}_{ano}.csv"

arquivo_saida = f"vacinacao_resumo_{mes}_{ano}.csv"

chunk_size = 100000


resultados = []

for chunk in pd.read_csv(
    arquivo_origem,
    sep=";",
    encoding="iso-8859-1",
    usecols=["no_municipio_paciente", "sg_uf_paciente", "ds_vacina", "nu_idade_paciente"],
    chunksize=chunk_size
):
    chunk["faixa_etaria"] = pd.cut(
        chunk["nu_idade_paciente"],
        bins=[-1, 5, 18, 59, float("inf")],
        labels=["0-5", "6-18", "19-59", "60+"],
        right=True
    )

    agrupado = chunk.groupby(
        ["no_municipio_paciente", "sg_uf_paciente", "ds_vacina", "faixa_etaria"],
        observed=True
    ).size().reset_index(name="quantidade")

    resultados.append(agrupado)

df_final = pd.concat(resultados, ignore_index=True)

df_resumido = df_final.groupby(
    ["no_municipio_paciente", "sg_uf_paciente", "ds_vacina", "faixa_etaria"],
    as_index=False,
    observed=True
).sum()

df_resumido.rename(columns={"sg_uf_paciente": "uf"}, inplace=True)

df_resumido["mes"] = mes
df_resumido["ano"] = ano

df_resumido = df_resumido[
    ["no_municipio_paciente", "uf", "ds_vacina", "faixa_etaria", "quantidade", "mes", "ano"]
]

df_resumido.to_csv(arquivo_saida, sep=";", index=False, encoding="utf-8")

print("Arquivo de resumo gerado com sucesso:", arquivo_saida)
