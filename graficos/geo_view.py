import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geobr import read_region

# Carrega os dados de vacinação
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Mapeia cada UF para sua região
regioes = {
    'RO': 'Norte', 'AC': 'Norte', 'AM': 'Norte', 'RR': 'Norte', 'PA': 'Norte', 'AP': 'Norte', 'TO': 'Norte',
    'MA': 'Nordeste', 'PI': 'Nordeste', 'CE': 'Nordeste', 'RN': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste',
    'AL': 'Nordeste', 'SE': 'Nordeste', 'BA': 'Nordeste',
    'MG': 'Sudeste', 'SP': 'Sudeste', 'RJ': 'Sudeste', 'ES': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste'
}

# Adiciona coluna de região
df['regiao'] = df['uf'].map(regioes)

# Soma total de vacinas aplicadas por região
vacinas_por_regiao = df.groupby('regiao')['quantidade'].sum()

# População fornecida
populacao = {
    'Norte': 18669345,
    'Nordeste': 57112091,
    'Sudeste': 88617693,
    'Sul': 31113021,
    'Centro-Oeste': 17071595
}

# DataFrame com vacinação per capita
df_vac = pd.DataFrame(vacinas_por_regiao)
df_vac.columns = ['total_vacinas']
df_vac['populacao'] = df_vac.index.map(populacao)
df_vac['vacinas_per_capita'] = df_vac['total_vacinas'] / df_vac['populacao']
df_vac = df_vac.reset_index()

# Corrige nome da região para casar com o shapefile do geobr
df_vac['regiao'] = df_vac['regiao'].replace({'Centro-Oeste': 'Centro Oeste'})

# Lê o shapefile de regiões brasileiras
mapa_regioes = read_region(year=2020)

# Junta com os dados de vacinação
mapa_completo = mapa_regioes.merge(df_vac, left_on='name_region', right_on='regiao')

# Plot do mapa
fig, ax = plt.subplots(figsize=(10, 8))
mapa_completo.plot(
    column='vacinas_per_capita',
    cmap='Reds',
    linewidth=0.8,
    edgecolor='0.8',
    legend=True,
    legend_kwds={'label': "Vacinação per capita", 'shrink': 0.7},
    ax=ax
)

plt.title("Vacinação per capita por Região", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()
