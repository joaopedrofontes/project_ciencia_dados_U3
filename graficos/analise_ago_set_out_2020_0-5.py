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

# Filtra faixa etária 0-5 e meses específicos de 2020
df_filtrado = df[
    (df['faixa_etaria'] == '0-5') &
    (df['ano'] == 2020) &
    (df['mes_num'].isin([8, 9, 10]))
].copy()

# Cria rótulo tipo "Ago/2020"
meses_nome = {8: 'Agosto', 9: 'Setembro', 10: 'Outubro'}
df_filtrado['mes_ano'] = df_filtrado['mes_num'].map(meses_nome) + '/2020'

# Agrupa por mês/ano e soma as quantidades
agrupado = df_filtrado.groupby('mes_ano')['quantidade'].sum().reindex(['Agosto/2020', 'Setembro/2020', 'Outubro/2020'])

# Gráfico de colunas
plt.figure(figsize=(8, 6))
ax = plt.gca()

ax.bar(agrupado.index, agrupado.values, color='darkblue', zorder=3)

plt.title("Vacinas aplicadas na faixa etária 0-5 (Ago-Out 2020)")
plt.xlabel("Mês")
plt.ylabel("Quantidade de doses aplicadas")
plt.grid(axis='y', zorder=0)

# Formatação eixo Y
ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
plt.ticklabel_format(style='plain', axis='y')

plt.tight_layout()
plt.show()
