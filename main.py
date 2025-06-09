import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import matplotlib.pyplot as plt
import seaborn as sns

# Baixar o dataset
url = "https://www.kaggle.com/datasets/joaoassaoka/taxas-de-rendimento-escolar-inep?select=Taxas_de_Rendimento_Escolar_2013_2023.csv"
df = pd.read_csv("Taxas_de_Rendimento_Escolar_2013_2023.csv")

# Filtrar apenas os dados do ano de 2023
df_2023 = df[df["Ano"] == 2023]

# Verificar as primeiras linhas
print(df_2023.head())

#  Gráficos Interativos para Análise
# 📌 Gráfico 1 – Mapa Coroplético (Visualização Geográfica)
# Esse mapa mostrará a distribuição das taxas de abandono escolar por estado.

import plotly.express as px

fig = px.choropleth(df_2023, 
                    locations="Unidade_Geografica", 
                    locationmode="country names",
                    color="Taxa_Abandono_3_Ano_EM",
                    title="Taxa de Abandono Escolar por Estado - 2023",
                    color_continuous_scale="Reds")

fig.show()

# 📌 Gráfico 2 – Gráfico de Linhas (Visualização Temporal)
# Este gráfico mostrará a evolução das taxas de abandono ao longo dos anos (2013-2023), destacando tendências.

df_temporal = df[df["Unidade_Geografica"].isin(["Minas Gerais", "São Paulo", "Rio de Janeiro"])]

fig = px.line(df_temporal, x="Ano", y="Taxa_Abandono_Total_EF", color="Unidade_Geografica",
              title="Evolução da Taxa de Abandono Escolar (2013-2023)")

fig.show()


# 📌 Gráfico 3 – Diagrama de Cordas (Visualização de Redes)
# Esse diagrama destacará a relação entre estados e etapas de ensino.

import plotly.graph_objects as go

df_chord = df_2023.groupby(["Regiao", "Dependencia_Administrativa"])["Taxa_Abandono_Total_EF"].sum().reset_index()

fig = go.Figure(data=[go.Sankey(
    node=dict(label=df_chord["Dependencia_Administrativa"].tolist() + df_chord["Regiao"].tolist()),
    link=dict(source=df_chord.index, target=df_chord.index + len(df_chord), value=df_chord["Taxa_Abandono_Total_EF"])
)])

fig.update_layout(title="Relação entre Estados e Etapas de Ensino no Abandono Escolar")
fig.show()


