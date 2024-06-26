#Libraries
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from haversine import haversine
import streamlit as st
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa', page_icon=':bar_chart:', layout='wide' )

#---------------------------------------------------------------------------
#Funções
#---------------------------------------------------------------------------

def country_maps( df1 ):
    df_aux = ( df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                    .groupby( ['City', 'Road_traffic_density'])
                    .median()
                    .reset_index() )

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'], 
                        location_info['Delivery_location_longitude']] ).add_to( map )
            
    folium_static( map, width=1024, height=600 )

def order_share_by_week( df1 ):
    #Criar uma coluna de semana
    df['week_of_year'] = df1['Order_Date'].dt.strftime( '%U')

    #Calcular o numero de pedidos por semana
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year').count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()

    #Calcular a media de pedidos por semana
    df_aux = pd.merge( df_aux01, df_aux02, how='inner' )
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line( df_aux, x='week_of_year', y='order_by_deliver' )
            
            
    return fig

def order_by_week( df1 ):
    #Criar uma coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
    df1_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year').count().reset_index()
    #Desenhar um Mapa
    fig = px.line( df1_aux, x='week_of_year', y='ID')

    return fig
def traffic_order_city( df1 ):
    df1_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby( ['City', 'Road_traffic_density'] ).count().reset_index()

    fig = px.scatter(df1_aux, x='City', y='Road_traffic_density', size='ID', color='City')
                
    return fig
def traffic_order_share( df1 ):
    df1_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby( 'Road_traffic_density').count().reset_index()
    df1_aux['entregas_perc'] = df1_aux['ID'] / df1_aux['ID'].sum()

    #Criando um grafico de pizza
    fig = px.pie( df1_aux, values='entregas_perc', names='Road_traffic_density' )
                
    return fig

def order_metric( df1 ):
    cols = ['ID', 'Order_Date']
    #selecionando as linhas
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()

    #desenhar o grafico de linhas=
    fig = px.bar( df_aux, x='Order_Date', y='ID' )

    return fig

def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe 
        
        Tipos de limpeza:
        1. Removendo os dados NaN
        2. Convertendo a coluna de dados de texto para numero Inteiro (int)
        3. Convertendo a coluna de dados de texto para numero Decimal (float)
        4. Convertendo a coluna de dados de texto para data (date)
        5. Removendo os espaços dentro de Strings/Object

        Input: Dataframe
        Output: Dataframe
    """

    #1. Removendo os dados NaN
    linhas_selecionadas = (df1['Delivery_person_Age'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['City'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Festival'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    #2. Convertendo a coluna de dados de texto para numero Inteiro (int)
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

    #3.Convertendo a coluna Ratings de texto para numero Decimal (Float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    #4.Convertendo a coluna Order_date de texto( str ) para Data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format= '%d-%m-%Y' )

    #5.Convertendo a coluna multiple_deliveries de texto para numero inteiro ( int )
    linhas_selecionas = ( df1['multiple_deliveries'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    #6. Removendo os espaços dentro de Strings/Object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    #Limpando a coluna Time_taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    return df1

#---------------------------------------- Inicio da Estrutura lógica do código ----------------------------------------
#Importing Dataset
df = pd.read_csv( 'D:/Users/FTC_analisando_dados_python/dataset/train.csv' )


#Limpando o dataframe
df1 = clean_code( df )

#====================================================================
#Barra Lateral
#====================================================================

st.header( 'Marketplace - Visão Cliente' )

#image_path = 'D:/Users/FTC_analisando_dados_python/logo.png.jpg'
image = Image.open( 'logo.png.jpg' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown(  '# Cury Company' )
st.sidebar.markdown(  '## Fastest Delivery in Town' )
st.sidebar.markdown(  """___""")

st.sidebar.markdown(  '## Selecione uma Data limite' )

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime( 2022, 4, 13 ),
    min_value=datetime( 2022, 2, 11 ),
    max_value=datetime( 2022, 4, 6),
    format='DD/MM/YYYY'
)

st.header( date_slider )
st.sidebar.markdown(  """___""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)
st.sidebar.markdown(  """___""")
st.sidebar.markdown(  '## Powered by Comunidade DS' )

#Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de trânsito
linhas_selecionadas = df1[ 'Road_traffic_density' ].isin ( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]

#====================================================================
#Layout Streamlit
#====================================================================

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Trafego', 'Visão Detalhada'] )

with tab1:

    with st.container():
        #Order metric
        fig = order_metric( df1 )
        st.markdown( 'Order By Day' )
        st.plotly_chart( fig, use_container_width=True )

    with st.container():
        col1, col2 = st.columns( 2 )
        with col1:
            fig = traffic_order_share( df1 )
            st.header( 'Traffic Order Share' )
            st.plotly_chart( fig, use_container_width=True )

        with col2:
            
            st.header( 'Traffic Order City' )
            fig = traffic_order_city( df1 )
            st.plotly_chart( fig, use_container_width=True )

with tab2:
    with st.container():
        st.header( 'Order by Week' )
        fig = order_by_week( df1 )
        st.plotly_chart( fig, use_container_width=True )

    with st.container():
        st.header( 'Order Share by Week' )
        fig = order_share_by_week( df1 )
        st.plotly_chart( fig, use_container_width=True )

with tab3:
    st.header( 'Country Maps')
    country_maps( df1 )
    


