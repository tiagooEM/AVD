import ast

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Painel de Análise Exploratória",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #fffaf0;
        color: #3d3d3d;
    }
    .stMainBlockContainer {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #ff6b0a;
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.18);
        padding: 1rem;
    }
    h1, h2, h3 {
        color: #3d3d3d;
    }
    div[data-testid="stWidgetLabel"] p {
        color: #444444;
        font-weight: 600;
    }
    div[data-baseweb="select"] > div {
        border-color: #ff6b0a;
        border-radius: 10px;
        background-color: #fffaf0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

df = load_data()
variaveis_quantitativas = ["height", "weight", "age"]
rotulos_variaveis = {
    "height": "Altura (cm)",
    "weight": "Peso (kg)",
    "age": "Idade (anos)",
}
colunas_necessarias = [
    *variaveis_quantitativas,
    "gender",
    "disciplines",
    "country",
    "faixa_etaria",
]
colunas_ausentes = [coluna for coluna in colunas_necessarias if coluna not in df.columns]
if colunas_ausentes:
    st.error(f"Colunas necessárias ausentes no dataset: {', '.join(colunas_ausentes)}.")
    st.stop()

for coluna in variaveis_quantitativas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

df["gender_label"] = df["gender"].map(
    {"Female": "Feminino", "Male": "Masculino"}
).fillna(df["gender"])

if "disciplines" in df.columns:
    def parse_disciplines(value):
        if pd.isna(value):
            return []
        parsed = ast.literal_eval(value) if isinstance(value, str) else value
        if isinstance(parsed, str):
            return [parsed]
        return [str(disciplina) for disciplina in parsed]

    df["_disciplines_list"] = df["disciplines"].map(parse_disciplines)
else:
    st.error("A coluna `disciplines` é necessária para os KPIs de modalidades.")
    st.stop()

df = df.dropna(subset=variaveis_quantitativas, how="all")
idades_validas = df["age"].dropna()
if df.empty or idades_validas.empty:
    st.error("Não há dados quantitativos e idades válidas para exibir.")
    st.stop()

idade_minima = int(idades_validas.min())
idade_maxima = int(idades_validas.max())

with st.sidebar:
    st.header("Filtros · Dashboard 1")
    st.caption("Os filtros abaixo afetam o laboratório de análise exploratória.")
    variaveis_selecionadas = st.multiselect(
        "Variáveis quantitativas",
        options=variaveis_quantitativas,
        default=variaveis_quantitativas,
        format_func=lambda variavel: rotulos_variaveis[variavel],
        help="Escolha as variáveis exibidas no mapa de calor e nos histogramas.",
        key="variaveis_dashboard1",
    )
    faixa_idade = st.slider(
        "Intervalo de idade (anos)",
        min_value=idade_minima,
        max_value=idade_maxima,
        value=(idade_minima, idade_maxima),
        step=1,
        help="Atletas fora deste intervalo são excluídos da análise.",
        key="faixa_idade_dashboard1",
    )

df_filtrado = df.loc[df["age"].between(faixa_idade[0], faixa_idade[1])]

with st.container(border=True):
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:14px; padding:2px 6px;">
            <span style="font-size:30px; color:#ff6b0a;">▮▮▮</span>
            <h1 style="font-size:30px; margin:0;">Painel de Análise Exploratória</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

aba_dashboard1, aba_dashboard2 = st.tabs(["Dashboard 1 · Análise exploratória", "Dashboard 2 · KPIs"])

with aba_dashboard1:
    with st.container(border=True):
        st.subheader("Relação entre variáveis")
        st.caption("Matriz de correlação")
        if len(variaveis_selecionadas) < 2:
            st.info("Selecione pelo menos duas variáveis para visualizar a correlação.")
        elif df_filtrado[variaveis_selecionadas].dropna(how="all").empty:
            st.info("Não há dados disponíveis para as variáveis e a faixa etária selecionadas.")
        else:
            correlacoes = df_filtrado[variaveis_selecionadas].corr()
            fig_correlacao = go.Figure(
                data=go.Heatmap(
                    z=correlacoes.values,
                    x=[rotulos_variaveis[coluna] for coluna in correlacoes.columns],
                    y=[rotulos_variaveis[coluna] for coluna in correlacoes.index],
                    zmin=-1,
                    zmax=1,
                    zmid=0,
                    colorscale=[
                        [0, "#a9a9a9"],
                        [0.5, "#fff3e5"],
                        [1, "#f97316"],
                    ],
                    text=[[f"{valor:.2f}" for valor in linha] for linha in correlacoes.values],
                    texttemplate="%{text}",
                    textfont={"size": 13, "color": "#444444"},
                    colorbar={"title": "Correlação"},
                    hovertemplate="%{y} × %{x}<br>Correlação: %{z:.2f}<extra></extra>",
                )
            )
            fig_correlacao.update_layout(
                height=450,
                margin={"l": 8, "r": 8, "t": 12, "b": 8},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis={"side": "top", "showgrid": False},
                yaxis={"autorange": "reversed", "showgrid": False},
                font={"color": "#444444"},
            )
            st.plotly_chart(fig_correlacao, width="stretch")

    with st.container(border=True):
        st.subheader("Altura e peso")
        st.caption("Relação entre medidas corporais por gênero")
        fig_perfil = px.scatter(
            df_filtrado,
            x="height",
            y="weight",
            color="gender_label",
            color_discrete_map={"Feminino": "#f97316", "Masculino": "#64748b"},
            opacity=0.62,
            hover_data=["age", "country"],
            labels={
                "height": "Altura (cm)",
                "weight": "Peso (kg)",
                "gender_label": "Gênero",
                "age": "Idade",
                "country": "País",
            },
        )
        fig_perfil.update_layout(
            height=430,
            margin={"l": 8, "r": 8, "t": 12, "b": 8},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#444444"},
            legend_title_text="Gênero",
        )
        fig_perfil.update_xaxes(showgrid=False)
        fig_perfil.update_yaxes(gridcolor="#e8dfd3")
        st.plotly_chart(fig_perfil, width="stretch")

    with st.container(border=True):
        st.subheader("Distribuição das variáveis quantitativas")
        st.caption("Um histograma para cada variável selecionada")
        if not variaveis_selecionadas:
            st.info("Selecione ao menos uma variável para visualizar seu histograma.")
        else:
            colunas_histogramas = st.columns(len(variaveis_selecionadas), gap="small")
            for coluna, variavel in zip(colunas_histogramas, variaveis_selecionadas):
                with coluna:
                    fig_histograma = px.histogram(
                        df_filtrado,
                        x=variavel,
                        color="gender_label",
                        nbins=25,
                        barmode="overlay",
                        opacity=0.72,
                        color_discrete_map={"Feminino": "#f97316", "Masculino": "#64748b"},
                        labels={
                            variavel: rotulos_variaveis[variavel],
                            "count": "Atletas",
                            "gender_label": "Gênero",
                        },
                    )
                    fig_histograma.update_layout(
                        title=rotulos_variaveis[variavel],
                        height=350,
                        margin={"l": 8, "r": 8, "t": 45, "b": 8},
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={"color": "#444444"},
                        legend_title_text="Gênero",
                    )
                    fig_histograma.update_xaxes(showgrid=False)
                    fig_histograma.update_yaxes(
                        title_text="Número de atletas",
                        gridcolor="#e8dfd3",
                    )
                    st.plotly_chart(fig_histograma, width="stretch")

    with st.container(border=True):
        st.subheader("Modalidades mais representadas")
        st.caption("Número de atletas nas 10 modalidades com maior participação")
        contagem_modalidades = (
            df_filtrado.explode("_disciplines_list")
            .groupby("_disciplines_list")
            .size()
            .nlargest(10)
            .sort_values()
        )
        fig_modalidades = px.bar(
            x=contagem_modalidades.values,
            y=contagem_modalidades.index,
            orientation="h",
            color_discrete_sequence=["#f97316"],
            labels={"x": "Atletas", "y": "Modalidade"},
        )
        fig_modalidades.update_layout(
            height=380,
            margin={"l": 8, "r": 8, "t": 12, "b": 8},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#444444"},
        )
        fig_modalidades.update_xaxes(showgrid=True, gridcolor="#e8dfd3")
        fig_modalidades.update_yaxes(showgrid=False)
        st.plotly_chart(fig_modalidades, width="stretch")

    st.caption(
        f"{len(df_filtrado):,} de {len(df):,} atletas na faixa etária selecionada.".replace(",", ".")
    )

with aba_dashboard2:
    st.subheader("Resumo dos atletas")
    st.caption(
        "Indicadores para gestores esportivos e comissões técnicas, com filtros opcionais por delegação e modalidade."
    )

    with st.container(border=True):
        col_filtro_pais, col_filtro_modalidade = st.columns(2)
        with col_filtro_pais:
            paises_selecionados = st.multiselect(
                "Países (opcional)",
                options=sorted(df["country"].dropna().unique()),
                help="Deixe vazio para incluir todos os países.",
                key="paises_dashboard2",
            )
        modalidades = sorted(
            {modalidade for lista in df["_disciplines_list"] for modalidade in lista}
        )
        with col_filtro_modalidade:
            modalidades_selecionadas = st.multiselect(
                "Modalidades (opcional)",
                options=modalidades,
                help="Deixe vazio para incluir todas as modalidades.",
                key="modalidades_dashboard2",
            )

    df_kpis = df.copy()
    if paises_selecionados:
        df_kpis = df_kpis[df_kpis["country"].isin(paises_selecionados)]
    if modalidades_selecionadas:
        df_kpis = df_kpis[
            df_kpis["_disciplines_list"].map(
                lambda lista: any(modalidade in lista for modalidade in modalidades_selecionadas)
            )
        ]

    if df_kpis.empty:
        st.info("Nenhum atleta encontrado com os filtros selecionados.")
    else:
        total_atletas = len(df_kpis)
        idades_validas = df_kpis["age"].dropna()
        generos_validos = df_kpis["gender"].dropna().str.casefold()
        total_generos_conhecidos = len(generos_validos)
        participacao_feminina = (
            generos_validos.eq("female").sum() / total_generos_conhecidos * 100
            if total_generos_conhecidos
            else None
        )
        modalidades_presentes = {
            modalidade for lista in df_kpis["_disciplines_list"] for modalidade in lista
        }

        metricas = st.columns(4)
        with metricas[0]:
            st.metric("Atletas", f"{total_atletas:,}".replace(",", "."))
        with metricas[1]:
            st.metric(
                "Idade mediana",
                f"{idades_validas.median():.0f} anos" if not idades_validas.empty else "Sem dados",
            )
        with metricas[2]:
            st.metric(
                "Participação feminina",
                f"{participacao_feminina:.1f}%".replace(".", ",")
                if participacao_feminina is not None
                else "Sem dados",
            )
        with metricas[3]:
            st.metric("Modalidades", f"{len(modalidades_presentes)}")

        st.caption(
            f"Indicadores calculados para {total_atletas:,} atletas nos filtros selecionados."
            .replace(",", ".")
        )

        col_faixa_etaria, col_paises = st.columns(2, gap="small")
        with col_faixa_etaria:
            with st.container(border=True):
                st.subheader("Faixas etárias")
                st.caption("Composição por idade e gênero")
                ordem_faixas = ["<20", "20-29", "30-39", "40+"]
                dados_faixas = (
                    df_kpis.groupby(["faixa_etaria", "gender_label"], observed=True)
                    .size()
                    .rename("Atletas")
                    .reset_index()
                )
                fig_faixas = px.bar(
                    dados_faixas,
                    x="faixa_etaria",
                    y="Atletas",
                    color="gender_label",
                    barmode="group",
                    category_orders={
                        "faixa_etaria": ordem_faixas,
                        "gender_label": ["Feminino", "Masculino"],
                    },
                    color_discrete_map={"Feminino": "#f97316", "Masculino": "#64748b"},
                    labels={
                        "faixa_etaria": "Faixa etária",
                        "gender_label": "Gênero",
                    },
                )
                fig_faixas.update_layout(
                    height=380,
                    margin={"l": 8, "r": 8, "t": 12, "b": 8},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#444444"},
                    legend_title_text="Gênero",
                )
                fig_faixas.update_xaxes(showgrid=False)
                fig_faixas.update_yaxes(title_text="Número de atletas", gridcolor="#e8dfd3")
                st.plotly_chart(fig_faixas, width="stretch")

        with col_paises:
            with st.container(border=True):
                st.subheader("Delegações com mais atletas")
                st.caption("As 10 maiores delegações no recorte atual")
                contagem_paises = (
                    df_kpis.groupby("country")
                    .size()
                    .nlargest(10)
                    .sort_values()
                )
                fig_paises = px.bar(
                    x=contagem_paises.values,
                    y=contagem_paises.index,
                    orientation="h",
                    color_discrete_sequence=["#f97316"],
                    labels={"x": "Atletas", "y": "País"},
                )
                fig_paises.update_layout(
                    height=380,
                    margin={"l": 8, "r": 8, "t": 12, "b": 8},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#444444"},
                )
                fig_paises.update_xaxes(showgrid=True, gridcolor="#e8dfd3")
                fig_paises.update_yaxes(showgrid=False)
                st.plotly_chart(fig_paises, width="stretch")

        with st.container(border=True):
            st.subheader("Modalidades com mais atletas")
            st.caption(
                "As 10 modalidades mais representadas; um atleta pode participar de mais de uma."
            )
            contagem_modalidades = (
                df_kpis.explode("_disciplines_list")
                .groupby("_disciplines_list")
                .size()
                .nlargest(10)
                .sort_values()
            )
            fig_modalidades = px.bar(
                x=contagem_modalidades.values,
                y=contagem_modalidades.index,
                orientation="h",
                color_discrete_sequence=["#f97316"],
                labels={"x": "Atletas", "y": "Modalidade"},
            )
            fig_modalidades.update_layout(
                height=420,
                margin={"l": 8, "r": 8, "t": 12, "b": 8},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#444444"},
            )
            fig_modalidades.update_xaxes(showgrid=True, gridcolor="#e8dfd3")
            fig_modalidades.update_yaxes(showgrid=False)
            st.plotly_chart(fig_modalidades, width="stretch")
