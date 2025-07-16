import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import geopandas as gpd

output_dir = 'output_vacinacao'
os.makedirs(output_dir, exist_ok=True)

# 1. Carregar e pré-processar os dados
try:
    df = pd.read_csv('../vacinacao_final.csv', sep=';')
except FileNotFoundError:
    print("Erro: Arquivo '../vacinacao_final.csv' não encontrado. Verifique o caminho.")
    exit()

# Definir faixa etária
faixa_etaria_escolhida = '19-59'
df_faixa = df[df['faixa_etaria'] == faixa_etaria_escolhida]

# Agrupar por estado e somar as quantidades
df_estados = df_faixa.groupby('uf')['quantidade'].sum().reset_index()

# Carregar o shapefile do Brasil:  https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html
try:
    brasil = gpd.read_file('BR_UF_2024.shp')
except FileNotFoundError:
    print("Erro: Arquivo 'BR_UF_2024.shp' não encontrado. Verifique o caminho.")
    exit()

# Padronizar os dados para o K-means
scaler = StandardScaler()
X = scaler.fit_transform(df_estados[['quantidade']])

# Método do cotovelo para determinar o número ideal de clusters
inertias = []
possible_k_values = range(1, 10)

for k in possible_k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Plot do método do cotovelo
plt.figure(figsize=(10, 6))
plt.plot(possible_k_values, inertias, '-o')
plt.xlabel('Número de clusters (k)')
plt.ylabel('Inércia')
plt.title('Método do Cotovelo')
plt.xticks(possible_k_values)
plt.savefig(os.path.join(output_dir, 'elbow_method.png'))
plt.close()

# Definir número de clusters (baseado no método do cotovelo)
# A análise revelou que o valor ideal é de 3 clusters
n_clusters = 3

# Aplicar K-means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df_estados['cluster'] = kmeans.fit_predict(X)

# Ordenar clusters pela média da quantidade (para garantir ordem crescente)
cluster_order = df_estados.groupby('cluster')['quantidade'].mean().sort_values().index
cluster_mapping = {cluster_order[i]: i for i in range(len(cluster_order))}
df_estados['cluster_ordered'] = df_estados['cluster'].map(cluster_mapping)

# Mapear nomes dos clusters baseado na ordem
cobertura_labels = ['Baixa cobertura', 'Média cobertura', 'Alta cobertura'][:n_clusters]
df_estados['cobertura'] = pd.cut(df_estados['cluster_ordered'],
                                bins=n_clusters,
                                labels=cobertura_labels)

# Juntar com os dados geográficos
brasil['uf'] = brasil['SIGLA_UF']  # Assumindo que a coluna de sigla é SIGLA_UF
df_map = brasil.merge(df_estados, on='uf', how='left')

# Criar mapa
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# Definir cores - gradiente do vermelho ao verde
colors = plt.cm.RdYlGn(np.linspace(0, 1, n_clusters))  # Inverter para vermelho=baixo, verde=alto

# Plotar os estados com cores baseadas no cluster
for cluster, color in zip(sorted(df_estados['cluster_ordered'].unique()), colors):
    df_map[df_map['cluster_ordered'] == cluster].plot(
        color=color,
        edgecolor='black',
        linewidth=0.5,
        ax=ax,
        label=f'{cobertura_labels[cluster]}'
    )

# Adicionar rótulos dos estados
for idx, row in df_map.iterrows():
    if not pd.isna(row['cluster_ordered']):
        ax.annotate(
            text=row['uf'],
            xy=(row['geometry'].centroid.x, row['geometry'].centroid.y),
            ha='center',
            fontsize=8,
            color='black'
        )

# Configurações do mapa
ax.set_title(f'Cobertura Vacinal para Faixa Etária: {faixa_etaria_escolhida}', fontsize=16)
ax.set_axis_off()

# Criar elementos da legenda com cores explícitas
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors[i],
                         edgecolor='black',
                         label=cobertura_labels[i]) for i in range(n_clusters)]

# Adicionar legenda
leg = ax.legend(
    handles=legend_elements,
    title='Cobertura Vacinal',
    loc='upper right',
    fontsize=10,
    frameon=True,
    framealpha=1
)
leg.get_frame().set_edgecolor('black')

# Salvar o mapa
plt.savefig(
    os.path.join(output_dir, f'mapa_cobertura_{faixa_etaria_escolhida.replace("+", "plus")}.png'),
    dpi=300,
    bbox_inches='tight'
)
plt.close()

print(f"Análise concluída para faixa etária {faixa_etaria_escolhida}. Resultados salvos em {output_dir}")