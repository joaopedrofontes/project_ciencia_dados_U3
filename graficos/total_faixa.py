import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Carrega o CSV
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Garante tipos corretos
df['ano'] = df['ano'].astype(int)

# Agrupa por ano e faixa etária, somando as quantidades
grupo = df.groupby(['ano', 'faixa_etaria'])['quantidade'].sum().reset_index()

# Pivota o DataFrame para colocar as faixas etárias como colunas
pivot = grupo.pivot(index='ano', columns='faixa_etaria', values='quantidade').fillna(0)

# Estilos de linha e cor por faixa etária (ciclo automático se houver mais)
estilos = ['-', '--', '-.', ':']
cores = plt.get_cmap('tab10').colors  # até 10 cores distintas do matplotlib

# Gráfico
plt.figure(figsize=(12, 7))
ax = plt.gca()

for idx, faixa in enumerate(pivot.columns):
    estilo_linha = estilos[idx % len(estilos)]
    cor = cores[idx % len(cores)]
    ax.plot(
        pivot.index,
        pivot[faixa],
        label=faixa,
        linestyle=estilo_linha,
        color=cor,
        linewidth=2,
        marker='o'
    )

# Título e eixos
plt.title("Total de vacinas aplicadas por ano por faixa etária no Brasil")
plt.xlabel("Ano")
plt.ylabel("Quantidade de doses aplicadas")
plt.xticks(pivot.index)
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Legenda
plt.legend(title='Faixa Etária')

# Eixo Y sem notação científica
ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
plt.ticklabel_format(style='plain', axis='y')

plt.tight_layout()
plt.show()
