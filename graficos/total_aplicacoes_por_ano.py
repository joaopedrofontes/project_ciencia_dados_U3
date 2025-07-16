import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Carrega o CSV
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Garante que a coluna 'ano' é numérica
df['ano'] = df['ano'].astype(int)

# Agrupa por ano e soma a quantidade de vacinas aplicadas
aplicacoes_por_ano = df.groupby('ano')['quantidade'].sum().reset_index()
aplicacoes_por_ano = aplicacoes_por_ano.sort_values(by='ano')

# Gráfico de colunas
plt.figure(figsize=(10, 6))
ax = plt.gca()

# Desenha o grid no eixo Y com zorder baixo (atrás das barras)
ax.grid(axis='y', zorder=0)

# Desenha as barras com zorder maior (na frente do grid)
ax.bar(aplicacoes_por_ano['ano'], aplicacoes_por_ano['quantidade'], color='mediumseagreen', zorder=3)

ax.set_title("Total de vacinas aplicadas por ano no Brasil")
ax.set_xlabel("Ano")
ax.set_ylabel("Quantidade de doses aplicadas")
ax.set_xticks(aplicacoes_por_ano['ano'])

# Desativa notação científica no eixo Y
ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
plt.ticklabel_format(style='plain', axis='y')

plt.tight_layout()
plt.show()
