import streamlit as st
import pandas as pd
import plotly.express as px
from pandas import DataFrame


def filtrar_base(df: DataFrame, produto: str):
    df_filtrado = df[df["Produto"] == produto.upper()]

    df_filtrado["Ano-Mes"] = (
        df_filtrado["Ano"].astype(str) + "-" + df_filtrado["Mes"].astype(str)
    )
    return df_filtrado


st.title("Médias mensais")

tab1, tab2, tab3 = st.tabs(["País", "Estado", "Cidade"])

produtos = ["Gasolina", "Etanol", "Diesel", "Diesel S10"]

estados = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]

with tab1:
    st.subheader("País")

    df = pd.read_csv("src/data/med_mensais/media_BRASIL_mes_a_mes.csv", sep=";")

    produto_selecionado = st.selectbox(
        "Selecione um produto:", produtos, key="produtos select pais"
    )

    df_filtrado = filtrar_base(df, produto_selecionado)

    fig = px.line(df_filtrado, x="Ano-Mes", y="Valor de Venda", title="Médias mensais")
    st.plotly_chart(fig)


with tab2:
    st.subheader("Estados")

    estado_selecionado = st.selectbox(
        "Selecione um estado:", estados, key="estados select estados"
    )

    df = pd.read_csv(
        f"src/data/med_mensais/estados/media_{estado_selecionado}_mes_a_mes.csv",
        sep=";",
    )

    produto_selecionado = st.selectbox(
        "Selecione um produto:", produtos, key="produtos select estados"
    )

    df_filtrado = filtrar_base(df, produto_selecionado)

    fig = px.line(df_filtrado, x="Ano-Mes", y="Valor de Venda", title="Médias mensais")
    st.plotly_chart(fig)


with tab3:
    st.subheader("Cidades")

    estado_selecionado = st.selectbox(
        "Selecione um estado:", estados, key="estados select cidades"
    )

    df_estados_cidades_overview = pd.read_csv(
        "src\data\overview\coletas_por_estado_cidade_tratado.csv"
    )

    cidades = df_estados_cidades_overview[
        df_estados_cidades_overview["Estado"] == estado_selecionado
    ]["Cidade"].unique()

    cidade_selecionada = st.selectbox("Selecione uma cidade:", cidades)

    cidade_selecionada = cidade_selecionada.replace(" ", "_")

    df = pd.read_csv(
        f"src\data\med_mensais\cidades\mes_{estado_selecionado}_{cidade_selecionada}_mes_a_mes.csv"
    )

    produto_selecionado = st.selectbox(
        "Selecione um produto:", produtos, key="produtos select cidades"
    )

    df_filtrado = filtrar_base(df, produto_selecionado)

    fig = px.line(df_filtrado, x="Ano-Mes", y="Valor de Venda", title="Médias mensais")
    st.plotly_chart(fig)
