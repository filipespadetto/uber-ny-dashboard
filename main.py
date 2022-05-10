import pandas as pd
import numpy as np
import streamlit as st

DATA_URL = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"

@st.cache
def load_data(nrows=2000):
    # columns map
    columns = {"Date/Time": "date",
               "Lat": "lat",
               "Lon": "lon"}

    # import dataframe and clean data
    df = pd.read_csv(DATA_URL, compression="gzip", nrows=nrows)
    df = df.rename(columns=columns)
    df.date = pd.to_datetime(df.date)
    df = df[list(columns.values())]

    return df

# load data
df = load_data()

# MAIN APPLICATION
st.title("Uber for NYC")
st.markdown(
    """
    Dashboard para análise de passageiros Uber na cidade de **Nova York**
    """
)

# SIDEBAR RAW DATA
st.sidebar.header("Configurações")
if st.sidebar.checkbox("Mostrar Raw Data"):
    st.markdown(
        f"""
        ##### Raw Data
        Carregando {df.shape[0]} linhas de entrada.
        """
    )
    st.write(df)

# MAP
st.subheader("Mapa")
select_entries = st.empty()
st.sidebar.subheader("Horário")
hour = st.sidebar.slider("Selecione a hora desejada", 0, 23, 12)
df_filtered = df[df.date.dt.hour == hour]
select_entries.text(df_filtered.shape[0])
st.map(df_filtered)

# HISTOGRAM
st.subheader("Quantidade de pedidos por hora")
hist = np.histogram(df.date.dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist)
