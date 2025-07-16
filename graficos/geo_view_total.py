import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geobr import read_state

# Carrega os dados de vacinação
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Soma vacinação total por UF
vacinas_por_estado = df.groupby('uf')['quantidade'].sum()

# População por estado (fonte: IBGE 2023 - valores aproximados)
populacao_estado = {
    'RO': 1746227, 'AC': 880631, 'AM': 4281209, 'RR': 716793,
    'PA': 8664306, 'AP': 802837, 'TO': 1577342,
    'MA': 7010960, 'PI': 3375646, 'CE': 9233656, 'RN': 3446071,
    'PB': 4145040, 'PE': 9539029, 'AL': 3220104, 'SE': 2291077, 'BA': 14850513,
    'MG': 21322691, 'ES': 4102129, 'RJ': 17219679, 'SP': 45973194,
    'PR': 11824665, 'SC': 8058441, 'RS': 11229915,
    'MS': 2901895, 'MT': 3836399, 'GO': 7350483, 'DF': 2982818
}


# Cria DataFrame com vacinação e população
df_estado = pd.DataFrame(vacinas_por_estado)
df_estado.columns = ['total_vacinas']
df_estado['populacao'] = df_estado.index.map(populacao_estado)
df_estado['vacinas_per_capita'] = df_estado['total_vacinas'] / df_estado['populacao']
df_estado = df_estado.reset_index()

# Lê shapefile dos estados
mapa_estados = read_state(year=2020)

# Merge shapefile com dados de vacinação
mapa_completo = mapa_estados.merge(df_estado, left_on='abbrev_state', right_on='uf')

# Plot do mapa
# Plot do mapa com total de vacinas (absoluto)
fig, ax = plt.subplots(figsize=(12, 10))
mapa_completo.plot(
    column='total_vacinas',
    cmap='Reds',
    linewidth=0.8,
    edgecolor='0.8',
    legend=True,
    legend_kwds={'label': "Total de vacinas aplicadas", 'shrink': 0.7},
    ax=ax
)

plt.title("Total de vacinas aplicadas por Estado", fontsize=15)
plt.axis('off')
plt.tight_layout()
plt.show()

