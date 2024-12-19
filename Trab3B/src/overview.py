import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Overview")

df_cnpj_unicos = pd.read_csv("src/data/overview/cnpjs_unicos_tratado.csv")
qntde_cnpj_unicos = len(df_cnpj_unicos)
qntde_cnpj_unicos_formatado = "{0:,}".format(qntde_cnpj_unicos).replace(",", ".")

df_estados = pd.read_csv("src/data/overview/coletas_por_estado_tratado.csv")
qntde_total_coletas = df_estados["Numero de Coletas"].sum()
qntde_total_coletas_formatado = "{0:,}".format(qntde_total_coletas).replace(",", ".")

df_cidades = pd.read_csv("src/data/overview/coletas_por_estado_cidade_tratado.csv")

texto = f"""
    Para a realização deste estudo, foram analisadas:
    
    ##### {qntde_total_coletas_formatado} entradas de dados

    Coletadas em:
    
    ##### {qntde_cnpj_unicos_formatado} empresas diferentes
"""

st.markdown(texto)

st.subheader("Distribuição por estado das coletas realizadas no Brasil")

fig = px.pie(
    df_estados,
    values="Numero de Coletas",
    names="Estado",
    title="Distribuição por estado",
    hole=0.3,
    width=700,
    height=700,
)

st.plotly_chart(fig)


st.subheader("Distribuição por cidade das coletas realizadas no estado")

estados = df_estados["Estado"].unique()
estado_selecionado = st.selectbox("Escolha o estado", estados)
df_cidades_estado_selecionado = df_cidades[df_cidades["Estado"] == estado_selecionado]

fig = px.pie(
    df_cidades_estado_selecionado,
    values="Numero de Coletas",
    names="Cidade",
    title=f"Distribuição por cidade no estado: {estado_selecionado}",
    hole=0.3,
    width=700,
    height=700,
)
st.plotly_chart(fig)

# Calcular o total de coletas do estado selecionado
total_coletas = df_cidades_estado_selecionado['Numero de Coletas'].sum()

# Adicionar a porcentagem de coletas para cada cidade
df_cidades_estado_selecionado['Porcentagem'] = (df_cidades_estado_selecionado['Numero de Coletas'] / total_coletas) * 100

# Exibir a tabela abaixo do gráfico com a cidade, quantidade de coletas e porcentagem
st.write("Tabela de coletas por cidade:")
st.dataframe(df_cidades_estado_selecionado[['Cidade', 'Numero de Coletas', 'Porcentagem']].sort_values(by='Numero de Coletas', ascending=False))