import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv("../datasets/vacinacao_final.csv", sep=';')

# Dicionário para converter nomes de meses em português para número
meses_pt = {
    'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06',
    'jul': '07', 'ago': '08', 'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
}

meses_nome = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun',
              'jul', 'ago', 'set', 'out', 'nov', 'dez']

# Substituir os nomes dos meses pelos números correspondentes
df['mes_num'] = df['mes'].str.lower().map(meses_pt)
df['mes_nome'] = df['mes'].str.lower()

# Criar a coluna de data com formato 'YYYY-MM'
df['data'] = pd.to_datetime(df['ano'].astype(str) + '-' + df['mes_num'], format='%Y-%m')

# Converter a coluna 'quantidade' para numérico
df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')

# Agrupar por mês e somar
vacinas_por_mes = df.groupby('data')['quantidade'].sum().sort_index()

# Preparar rótulos curtos para o eixo x: "jan/20", "fev/20", ...
labels_x = [f"{meses_nome[d.month - 1]}/{str(d.year)[-2:]}" for d in vacinas_por_mes.index]

# Plotar gráfico de barras
plt.figure(figsize=(14, 6))
plt.bar(labels_x, vacinas_por_mes.values, color='darkblue')
plt.title('Quantidade Total de Vacinas Aplicadas por Mês (2020-2024)')
plt.xlabel('Mês/Ano')
plt.ylabel('Total de Vacinas Aplicadas')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y')
plt.show()
