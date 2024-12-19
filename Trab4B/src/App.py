import streamlit as st
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier

# dados
# https://www.kaggle.com/datasets/mujtabamatin/air-quality-and-pollution-assessment

colunas = [
    "Temperature",
    "Humidity",
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "Proximity_to_Industrial_Areas",
    "Population_Density",
    "Air Quality",
]


def treinar_random_forest(dfWork: DataFrame, target: DataFrame):
    rf = RandomForestClassifier(n_estimators=500, random_state=42)
    rf.fit(dfWork.values, target.values)
    return rf


def preparar_dados_treinamento():
    df = pd.read_csv("data/updated_pollution_dataset.csv")
    var_quanti = [
        "Temperature",  # float °C
        "Humidity",  # float %
        "PM2.5",  # float ug/m³
        "PM10",  # float ug/m³
        "NO2",  # float ppb
        "SO2",  # float ppb
        "CO",  # float ppm
        "Proximity_to_Industrial_Areas",  # float km
        "Population_Density",  # int people/km²
    ]
    dfWork = df[var_quanti]
    target = df["Air Quality"]
    return dfWork, target


dfWork, target = preparar_dados_treinamento()
rf = treinar_random_forest(dfWork, target)


vals_predict = {
    "Temperature": "**Temperatura (°C)**",
    "Humidity": "**Umidade (%)**",
    "PM2.5": "**Concentração de partículas inaláveis finas PM2.5 (µg/m³)**",
    "PM10": "**Concentração de partículas inaláveis PM10 (µg/m³)**",
    "NO2": "**Concentração de dióxido de nitrogênio (ppb)**",
    "SO2": "**Concetração de dióxido de enxofre (ppb)**",
    "CO": "**Concentração de monóxido de carbono (ppm)**",
    "Proximity_to_Industrial_Areas": "**Distância até a área industrial mais próxima (km)**",
    "Population_Density": "**Densidade populacional (pessoas/km²)**",
}

ranges = {}
for val in vals_predict.keys():
    ranges[val] = {"min": dfWork[val].min(), "max": dfWork[val].max()}

selected_values = {}
for val in vals_predict.keys():
    if val != "Population_Density":
        selected_values[val] = st.sidebar.slider(
            label=vals_predict[val],
            min_value=ranges[val]["min"],
            max_value=ranges[val]["max"],
            step=0.1,
            value=(ranges[val]["min"] + ranges[val]["max"]) / 2,
        )
    else:
        selected_values[val] = st.sidebar.slider(
            label=vals_predict[val],
            min_value=ranges[val]["min"],
            max_value=ranges[val]["max"],
            step=1,
            value=int((ranges[val]["min"] + ranges[val]["max"]) / 2),
        )

res = rf.predict([list(selected_values.values())])

map_resposta = {
    "Good": "Boa",
    "Moderate": "Moderada",
    "Poor": "Ruim",
    "Hazardous": "Perigosa",
}

cor_texto = {
    "Good": "green",
    "Moderate": "gray",
    "Poor": "orange",
    "Hazardous": "red",
}

st.title("Previsão de qualidade do ar")
st.subheader(
    f"Resultado de acordo com o modelo: **:{cor_texto[res[0]]}[{map_resposta[res[0]]}]**"
)

st.divider()

st.write("Valores utilizados para a previsão:")

for val in vals_predict.keys():
    if val == "Temperature":
        unidade = "°C"
    elif val == "Humidity":
        unidade = "%"
    elif val in ["PM2.5", "PM10"]:
        unidade = "µg/m³"
    elif val in ["NO2", "SO2"]:
        unidade = "ppb"
    elif val == "CO":
        unidade = "ppm"
    elif val == "Proximity_to_Industrial_Areas":
        unidade = "km"
    elif val == "Population_Density":
        unidade = "pessoas/km²"
    else:
        unidade = ""

    st.write(f"{vals_predict[val]}: {selected_values[val]:.2f} {unidade}")
