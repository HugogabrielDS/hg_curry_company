import pandas as pd
import numpy  as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine
import streamlit as st
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Restaurante', page_icon=':bar_chart:', layout='wide' )

#---------------------------------------------------------------------------
#Funções
#---------------------------------------------------------------------------

def avg_std_time_graph_bar( df1 ):
    df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby( 'City' ).agg( {'Time_taken(min)': ['mean', 'std']} )
    
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict( type= 'data', array=df_aux['std_time'] ) ) )

    fig.update_layout( barmode='group' )

    return fig

def avg_std_time_graph( df1 ):
    df_aux = ( df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density'])
                                                                                    .agg( {'Time_taken(min)': ['mean', 'std'] } ) )

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = px.sunburst( df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                            color='std_time', color_continuous_scale='RdBu',
                            color_continuous_midpoint=np.average(df_aux['std_time'] ) )
                
    return fig

def avg_distance_graph( df1 ):
    cols = [ 'Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude' ]
    df1['distance'] = df1.loc[:, cols].apply( lambda x:  
                                        haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                   (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1 )

    avg_distance = df1.loc[:,[ 'City', 'distance']].groupby( 'City' ).mean().reset_index()

    fig = go.Figure( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, .1, 0] )] )

    return fig

def avg_std_time_delivery(df1, festival, op):
    """
        Esta função calcula a media e o desvio padrão de tempo de entrega.
        Parâmetros:
            imput:
                - df: Dataframe com os dados necessários para o calculo
                - op: Tipo de operação que serão realizadas (media ou desvio padrão)
            output:
                - df: Dataframe com 2 colunas e 1 linha com os valores calculados

    """
    df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival',)
                                                         .agg( {'Time_taken(min)': ['mean', 'std']} ) )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round( df_aux.loc[df_aux['Festival'] == festival, op], 2)

    return df_aux

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
df = pd.read_csv( 'D:/Users/FTC_analisando_dados_python/dataset/train.csv.zip' )

df1 = clean_code( df )

#====================================================================
#Barra Lateral
#====================================================================

st.header( 'Marketplace - Visão Restaurante' )

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
        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        with col1:
            delivery_unique = len( df1.loc[:, 'Delivery_person_ID'].unique() )
            col1.metric( 'Entregadores', delivery_unique )

        with col2:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']

            df1['distance'] = df1.loc[:, cols].apply( lambda x: haversine( 
                                (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 )

            avg_distance = np.round( df1.loc[:, 'distance'].mean(), 2)
            col2.metric( 'A Distância média', avg_distance )

        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')         
            col3.metric( 'Tempo médio Festival', df_aux)

        with col4:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time')
            col4.metric( 'STD Entrega Festival', df_aux)

        with col5:
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
            col5.metric( 'Tempo médio', df_aux)

        with col6:
            df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
            col6.metric( 'STD Entrega', df_aux)

    with st.container():    
        st.title( 'Tempo médio de entrega por cidade' )
        col1, col2 = st.columns( 2 )
        with col1:
        
            fig = avg_distance_graph( df1 )
            st.plotly_chart( fig )

        with col2:
            fig = avg_std_time_graph( df1 )
            st.plotly_chart( fig )

    with st.container():
        st.title( 'Distribuição de tempo' )
        fig = avg_std_time_graph_bar( df1 )
        st.plotly_chart( fig )