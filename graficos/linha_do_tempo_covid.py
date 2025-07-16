import pandas as pd
import matplotlib.pyplot as plt

# Carrega o CSV
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Filtra todas as vacinas que contêm 'covid' no nome (ignora maiúsculas/minúsculas)
df_covid = df[df['ds_vacina'].str.contains('covid', case=False, na=False)].copy()

# Mapeia nomes dos meses para números
meses_ordem = {
    'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
    'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
}
df_covid['mes'] = df_covid['mes'].str.lower().map(meses_ordem)
df_covid['ano'] = df_covid['ano'].astype(int)

# Cria coluna de data com ano e mês
df_covid['ano_mes'] = pd.to_datetime(dict(year=df_covid['ano'], month=df_covid['mes'], day=1))

# Agrupa por ano-mês e soma a quantidade
covid_mensal = df_covid.groupby('ano_mes')['quantidade'].sum().reset_index()

# Garante todos os meses desde jan/2020 até o último presente no dataset
inicio = pd.Timestamp('2020-01-01')
fim = df_covid['ano_mes'].max()
todos_os_meses = pd.date_range(start=inicio, end=fim, freq='MS')

# Preenche meses ausentes com 0
covid_mensal_completo = pd.DataFrame({'ano_mes': todos_os_meses})
covid_mensal_completo = covid_mensal_completo.merge(covid_mensal, on='ano_mes', how='left')
covid_mensal_completo['quantidade'] = covid_mensal_completo['quantidade'].fillna(0).astype(int)

# Gráfico de colunas
plt.figure(figsize=(14, 6))
plt.bar(covid_mensal_completo['ano_mes'], covid_mensal_completo['quantidade'], width=20, color='skyblue')
plt.title("Aplicações mensais de vacinas contra COVID-19 no Brasil")
plt.xlabel("Ano-Mês")
plt.ylabel("Quantidade de doses aplicadas")
plt.grid(axis='y')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
