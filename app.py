import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Análise do Dataset de Atletas das Olimpíadas 2024",
    layout="wide",
)

st.title("Análise de Variáveis Quantitativas — Atletas das Olimpíadas 2024")

df = load_data()

# Código é identificador, não uma medida quantitativa.
VARS_QUANT = ["height", "weight", "age"]

with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis para a correlação",
        options=VARS_QUANT,
        default=VARS_QUANT,
        help="Escolha as variáveis quantitativas que entrarão na análise de correlação.",
    )

    variavel_filtro = st.selectbox(
        "Variável para filtrar",
        options=VARS_QUANT,
        help="O intervalo selecionado remove atletas fora dessa faixa das análises.",
    )

    valores = df[variavel_filtro]
    if pd.api.types.is_integer_dtype(valores):
        minimo, maximo, passo = int(valores.min()), int(valores.max()), 1
    else:
        minimo, maximo, passo = float(valores.min()), float(valores.max()), 0.1

    intervalo = st.slider(
        f"Intervalo de {variavel_filtro}",
        min_value=minimo,
        max_value=maximo,
        value=(minimo, maximo),
        step=passo,
    )

df_filtrado = df[df[variavel_filtro].between(*intervalo)]
st.caption(
    f"{len(df_filtrado)} de {len(df)} atletas incluídos após o filtro de {variavel_filtro}."
)

col_correlacao, col_distribuicao = st.columns(2)

with col_correlacao:
    st.subheader("Correlação")
    if len(variaveis) < 2:
        st.info("Selecione pelo menos duas variáveis na barra lateral.")
    else:
        st.info("O mapa de calor da correlação será incluído na próxima aula.")

with col_distribuicao:
    st.subheader("Distribuição")
    st.info("O histograma da distribuição será incluído na próxima aula.")
