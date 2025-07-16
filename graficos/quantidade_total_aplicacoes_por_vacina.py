import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Carrega o CSV
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Agrupa por vacina e soma quantidade total aplicada
vacinas_totais = df.groupby('ds_vacina')['quantidade'].sum().reset_index()

# Ordena em ordem decrescente e seleciona top 10
top10_vacinas = vacinas_totais.sort_values(by='quantidade', ascending=False).head(10)

# Cria figura e eixo
plt.figure(figsize=(12, 7))
ax = plt.gca()

# Gráfico de colunas (barras verticais)
ax.bar(top10_vacinas['ds_vacina'], top10_vacinas['quantidade'], color='steelblue', zorder=3)

# Configurações visuais
ax.set_title("Top 10 vacinas mais aplicadas no Brasil (total de doses)")
ax.set_xlabel("Vacina")
ax.set_ylabel("Quantidade total de doses aplicadas")
ax.grid(axis='y', zorder=0)

# Evita notação científica no eixo Y
ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
plt.ticklabel_format(style='plain', axis='y')

# Rotaciona labels do eixo X para melhor leitura
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()
