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

# Filtra apenas faixa etária 0-5 nos meses de maio, junho e julho de 2024
df_filtrado = df[
    (df['faixa_etaria'] == '0-5') &
    (df['ano'] == 2024) &
    (df['mes_num'].isin([5, 6, 7]))
].copy()

# Cria rótulo tipo "Maio/2024"
meses_nome = {5: 'Maio', 6: 'Junho', 7: 'Julho'}
df_filtrado['mes_ano'] = df_filtrado['mes_num'].map(meses_nome) + '/2024'

# Agrupa por mês/ano e soma as quantidades
agrupado = df_filtrado.groupby('mes_ano')['quantidade'].sum().reindex(['Maio/2024', 'Junho/2024', 'Julho/2024'])

# Gráfico de colunas
plt.figure(figsize=(8, 6))
ax = plt.gca()

ax.bar(agrupado.index, agrupado.values, color='darkorange', zorder=3)

plt.title("Vacinas aplicadas na faixa etária 0-5 (maio a julho de 2024)")
plt.xlabel("Mês")
plt.ylabel("Quantidade de doses aplicadas")
plt.grid(axis='y', zorder=0)

# Formatação do eixo Y
ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
plt.ticklabel_format(style='plain', axis='y')

plt.tight_layout()
plt.show()
