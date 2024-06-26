import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

#image_path = 'D:/Users/FTC_analisando_dados_python/'
image = Image.open( 'logo.png.jpg' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Curry Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """___""" )

st.write( '# Curry Company Growth Dashboard' )

st.markdown(
    """
    Growth Dashboard foi construido para acompanhar métricas de crescimento dos entregadores e Restaurantes.
    ### Como utilizar o Growth Dashboard
    - Visão Empresa
        - Visão Gerencial: Métricas  gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Distribuição das entregas por Cidade.
    - Visão Entregador
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante
        - Indicadores semanais de crescimento dos Restaurantes 

    ### Ask for help
    - Time de Data Science no Discord
    @Hugo
"""
)