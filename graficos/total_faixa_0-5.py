import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Carrega o CSV
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Filtra só faixa etária 0-5
df_0_5 = df[df['faixa_etaria'] == '0-5'].copy()

# Garante que a coluna 'ano' é numérica
df_0_5['ano'] = df_0_5['ano'].astype(int)

# Agrupa por ano e soma a quantidade de vacinas aplicadas
aplicacoes_0_5_por_ano = df_0_5.groupby('ano')['quantidade'].sum().reset_index()
aplicacoes_0_5_por_ano = aplicacoes_0_5_por_ano.sort_values(by='ano')

# Gráfico de colunas
plt.figure(figsize=(10, 6))
ax = plt.gca()

# Desenha o grid no eixo Y com zorder baixo (atrás)
ax.grid(axis='y', zorder=0, alpha=0.7)

# Desenha as barras com zorder maior (na frente do grid)
ax.bar(aplicacoes_0_5_por_ano['ano'], aplicacoes_0_5_por_ano['quantidade'], color='coral', zorder=3)

plt.title("Total de vacinas aplicadas por ano na faixa etária 0-5 no Brasil")
plt.xlabel("Ano")
plt.ylabel("Quantidade de doses aplicadas")
plt.xticks(aplicacoes_0_5_por_ano['ano'])

# Formatação do eixo Y para evitar notação científica
ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
plt.ticklabel_format(style='plain', axis='y')

plt.tight_layout()
plt.show()