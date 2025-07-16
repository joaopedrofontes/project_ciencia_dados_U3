import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Carrega o CSV
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Mapeia os nomes dos meses para números
meses_ordem = {
    'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
    'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
}

# Converte o mês para número
df['mes_num'] = df['mes'].str.lower().map(meses_ordem)
df['ano'] = df['ano'].astype(int)

# Filtra apenas o ano de 2023 e meses março, abril e maio (sem filtrar faixa etária)
df_filtrado = df[
    (df['ano'] == 2023) &
    (df['mes_num'].isin([3, 4, 5]))
].copy()

# Cria rótulo tipo "Março/2023"
meses_nome = {3: 'Março', 4: 'Abril', 5: 'Maio'}
df_filtrado['mes_ano'] = df_filtrado['mes_num'].map(meses_nome) + '/2023'

# Agrupa por mês/ano e soma as quantidades
agrupado = df_filtrado.groupby('mes_ano')['quantidade'].sum().reindex(['Março/2023', 'Abril/2023', 'Maio/2023'])

# Gráfico de colunas
plt.figure(figsize=(8, 6))
ax = plt.gca()

ax.bar(agrupado.index, agrupado.values, color='teal', zorder=3)

plt.title("Vacinas aplicadas (março a maio de 2023)")
plt.xlabel("Mês")
plt.ylabel("Quantidade de doses aplicadas")
plt.grid(axis='y', zorder=0)

# Formatação eixo Y
ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
plt.ticklabel_format(style='plain', axis='y')

plt.tight_layout()
plt.show()
