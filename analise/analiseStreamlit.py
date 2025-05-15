import streamlit as st
import pandas as pd
import plotly.express as px 
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Dashboard de Despesas", page_icon='🏎️', layout='wide')

df = pd.read_excel("Despesas_Tratadas.xlsx")

st.sidebar.header("Selecione os Filtros")


tipos = st.sidebar.multiselect(
    "Tipos",
    options=df["tipo"].unique(),
    default=df["tipo"].unique(),
    key="tipo"
)

setores = st.sidebar.multiselect(
    "Setores",
    options=df["setor"].unique(),
    default=df["setor"].unique(),
    key="setor"
)


df_selection = df.query("tipo in @tipos and setor in @setores")

def Home():
    total_despesas = df["valor"].sum()
    media = df["valor"].mean()
    mediana = df["valor"].median()
        
    total1, total2, total3 = st.columns(3)
    with total1:
            # Apresentar indicadores rápidos
      st.metric("Total de Despesas", value=int(total_despesas))
    with total2:
            st.metric("Média por Produto", value=f"{media:.2f}")
    with total3:
            st.metric("Mediana", value=int(mediana))
            
    st.markdown("---")
    
    df_selection['data'] = pd.to_datetime(df_selection['data'], dayfirst=True)
    
    df_selection['mes_ano'] = df_selection['data'].dt.to_period('M').astype(str)
    df_grouped = (
        df_selection
        .groupby(['mes_ano', 'setor'])['valor']
        .sum()
        .reset_index())
    
    fig_barras = px.bar(
        df_grouped , 
        x='mes_ano',
        y='valor',
        color='setor',
        barmode='group',
        title="Quantidade de despesa por setor"
    )
    
    st.plotly_chart(fig_barras, use_container_width=True)
    
def sideBar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title="Menu",
            options=["Home", "Gráficos"],
            icons=["house", "bar-chart"],
            default_index=0
        )
    if selecionado == "Home":
        Home()

sideBar()
    