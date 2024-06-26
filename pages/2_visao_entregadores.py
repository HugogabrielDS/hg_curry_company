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

st.set_page_config( page_title='Visão Entregadores', page_icon=':bar_chart:', layout='wide' )

#---------------------------------------------------------------------------
#Funções
#---------------------------------------------------------------------------

def top_delivers( df1, top_asc ):
    df2 = ( df1.loc[:,['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby( ['City','Delivery_person_ID'] )
                                                                        .mean().sort_values( ['City', 'Time_taken(min)'], ascending=top_asc ).reset_index() )

    df_aux01 = df2.loc[df2[ 'City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2[ 'City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2[ 'City'] == 'Semi-Urban', :].head(10)  

    df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )

    return df3
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
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format= '%d-%m-%Y')

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

#Importing Dataset
df = pd.read_csv( 'D:/Users/FTC_analisando_dados_python/dataset/train.csv' )

df1 = clean_code( df )

#====================================================================
#Barra Lateral
#====================================================================

st.header( 'Marketplace - Visão Entregadores' )

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

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'] )

with tab1:
    with st.container():
        st.title( 'Overall Metrics' )
        col1, col2, col3, col4 = st.columns( 4, gap='large' )
        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric( 'Maior de Idade', maior_idade )

        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric( 'Menor de Idade', menor_idade )

        with col3:
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric( 'Melhor condição de veículos', melhor_condicao )

        with col4:
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric( 'Pior condição de veículos', pior_condicao )

with st.container():
    st.markdown(  """___""" )
    st.title( 'Avaliações' )

    col1, col2, col3 = st.columns( 3 )
    with col1:
        st.markdown( 'Avaliação média por entregador' )
        df_avg_ratings_per_deliver = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby( 'Delivery_person_ID' ).mean().reset_index()
        st.dataframe( df_avg_ratings_per_deliver )
    
    with col2:
        st.markdown( 'Avaliação por trânsito' )
        df_avg_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby( 'Road_traffic_density' )
                                                                                                    .agg( {'Delivery_person_Ratings': ['mean', 'std'] } ) )
        #Mudança de nome das colunas
        df_avg_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']
        #Reseta o index
        df_avg_rating_by_traffic.reset_index()
        st.dataframe( df_avg_rating_by_traffic )

    with col3:
        st.markdown( 'Avaliação por clima' )
        df_std_avg_rating_by_conditions = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby( 'Weatherconditions' )
                                                                                                        .agg( {'Delivery_person_Ratings': ['mean', 'std'] } ) )

        #Mudança de nome das colunas
        df_std_avg_rating_by_conditions.columns = ['delivery_mean', 'delivery_std']

        #Reseta o index
        df_std_avg_rating_by_conditions.reset_index()
        st.dataframe( df_std_avg_rating_by_conditions )

with st.container():
    st.markdown( """___""" )
    st.title( 'Tempo de Entrega' )

    col1, col2 = st.columns( 2 )
    with col1: 
        st.markdown( 'Top Entregadores mais rápidos' )
        df3 = top_delivers( df1, top_asc=True )
        st.dataframe( df3 )

    with col2: 
        st.markdown( 'Top Entregadores mais lentos' )
        df3 = top_delivers( df1, top_asc=False )
        st.dataframe( df3 )