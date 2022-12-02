
# IMPORTACIÓN DE LAS LIBRERÍAS
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import math
from datetime import datetime

#------------------------------------------------------------------------------------------------#
# IMPORTACIÓN DE LA BASE DE DATOS
df = pd.read_csv("Base de datos_Proyecto final.csv")
df.head(5)
#------------------------------------------------------------------------------------------------#

# CONFIGURACIÓN DE LA PÁGINA Y EL SIDEBAR
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.title("Programas internacionales")

#------------------------------------------------------------------------------------------------#
# SIDEBAR
sidebar = st.sidebar
sidebar.header('Dashboard \n `Programas internacionales`')

# LISTA DESPLEGABLE
year_options = df["Año"].unique().tolist()
year_options.append("Todos los registros")
year = st.sidebar.selectbox("Año:", year_options, 0) 

sidebar.subheader('Parámetros del mapa mundial')

# LISTA DESPLEGABLE MÚLTIPLE (MAPA MUNDIAL)
df_continents_non_nan = df.dropna()
continent_options = df_continents_non_nan["Continente"].unique().tolist()
continents = st.sidebar.multiselect("Continente:", continent_options, default=["Europa"])

#------------------------------------------------------------------------------------------------#
# OUTPUTS

# MÉTRICAS
if year == "Todos los registros":
    df1 = df.copy()
else:
    df1 = df[df['Año'] == year]
# GENERAL
est = df.groupby(['Estatus de asignacion'])['Estatus de asignacion'].count().to_dict()
df_est = pd.DataFrame([key for key in est.keys()], columns=['Estatus de asignacion'])
df_est['Conteo'] = [value for value in est.values()]
df_est = df_est.sort_values(by="Conteo", ascending=False)
df_est.reset_index(drop=True, inplace=True)
df_est['Porcentaje'] = round(df_est['Conteo']/(df_est['Conteo'].sum())*100,2)
porc_1era_opcion = df_est[df_est["Estatus de asignacion"] == "Asignación a la primera opción"]["Porcentaje"].reset_index(drop=True)
porc_2da_opcion = df_est[df_est["Estatus de asignacion"] == "Asignación a la segunda opción"]["Porcentaje"].reset_index(drop=True)
porc_3era_opcion = df_est[df_est["Estatus de asignacion"] == "Asignación a la tercera opción"]["Porcentaje"].reset_index(drop=True)

# AÑO SELECCIONADO
est_año = df1.groupby(['Estatus de asignacion'])['Estatus de asignacion'].count().to_dict()
df_est_año = pd.DataFrame([key for key in est_año.keys()], columns=['Estatus de asignacion'])
df_est_año['Conteo'] = [value for value in est_año.values()]
df_est_año = df_est_año.sort_values(by="Conteo", ascending=False)
df_est_año.reset_index(drop=True, inplace=True)
df_est_año['Porcentaje'] = round(df_est_año['Conteo']/(df_est_año['Conteo'].sum())*100,2)
porc_1era_opcion_año = df_est_año[df_est_año["Estatus de asignacion"] == "Asignación a la primera opción"]["Porcentaje"].reset_index(drop=True)
porc_2da_opcion_año = df_est_año[df_est_año["Estatus de asignacion"] == "Asignación a la segunda opción"]["Porcentaje"].reset_index(drop=True)
porc_3era_opcion_año = df_est_año[df_est_año["Estatus de asignacion"] == "Asignación a la tercera opción"]["Porcentaje"].reset_index(drop=True)

# MAPA MUNDIAL
df2 = df1[df1['Continente'].isin(continents)]
df2 = df2.dropna()
conteo_paises = df2.groupby(['País destino','Nombre del país', 'Continente'])['País destino'].count().to_dict()
df_conteo_paises = pd.DataFrame([key for key in conteo_paises.keys()], columns=['País destino','Nombre del país', 'Continente'])
df_conteo_paises['Número de intercambios'] = [value for value in conteo_paises.values()]
df_conteo_paises = df_conteo_paises.sort_values(by="Número de intercambios", ascending=False)
df_conteo_paises.reset_index(drop=True, inplace=True)
df_conteo_paises_2 = df_conteo_paises[["Nombre del país","Número de intercambios"]]


# TREEMAP
val_treemap_1 = df.groupby(['Escuela', 'Tipo de intercambio', 'Estatus de asignacion'])['Promedio'].mean().to_dict()
val_treemap_2 = df.groupby(['Escuela', 'Tipo de intercambio', 'Estatus de asignacion'])['Estatus de asignacion'].count().to_dict()
df_treemap = pd.DataFrame([key for key in val_treemap_1.keys()], columns=['Escuela','Tipo de intercambio', 'Estatus de asignacion'])
df_treemap['Promedio medio'] = [value for value in val_treemap_1.values()]
df_treemap['Número de estudiantes'] = [value for value in val_treemap_2.values()]
df_treemap = df_treemap.sort_values(by='Número de estudiantes', ascending=False)
df_treemap.reset_index(drop=True, inplace=True)
df_treemap = df_treemap.dropna(subset=['Escuela', 'Tipo de intercambio', 'Estatus de asignacion','Promedio medio', 'Número de estudiantes'])

# SANKEY
df_sankey = df[['Escuela', 'Tipo de intercambio', 'Estatus de asignacion']]
df_sankey = df_sankey.dropna()
df_sankey['Escuela'] = df_sankey['Escuela'].astype('category').cat.codes
num_escuela = list(df_sankey['Escuela'].unique())
tipo_escuela = list(df['Escuela'].unique())
escuela_dim = go.parcats.Dimension(values = df_sankey['Escuela'], label = 'Escuela', categoryarray = num_escuela, ticktext = tipo_escuela)
df_sankey['Tipo de intercambio'] = df_sankey['Tipo de intercambio'].astype('category').cat.codes
num_tipo = list(df_sankey['Tipo de intercambio'].unique())
tipo_tipo = list(df['Tipo de intercambio'].unique())
tipo_dim = go.parcats.Dimension(values =df_sankey['Tipo de intercambio'], label = 'Tipo de intercambio', categoryarray = num_tipo, ticktext = tipo_tipo)
df_sankey['Estatus de asignacion'] = df_sankey['Estatus de asignacion'].astype('category').cat.codes
num_estatus = list(df_sankey['Estatus de asignacion'].unique())
tipo_estatus = list(df['Estatus de asignacion'].unique())
estatus_dim = go.parcats.Dimension(values = df_sankey['Estatus de asignacion'], label = 'Estatus de asignación', categoryarray = num_estatus, ticktext = tipo_estatus)

# PIE
df_pie = df1.dropna()
val_pie = df_pie.groupby(['Tipo de intercambio'])['Tipo de intercambio'].count().to_dict()
df_pie = pd.DataFrame([key for key in val_pie.keys()], columns=['Tipo de intercambio'])
df_pie['Número de estudiantes'] = [value for value in val_pie.values()]
df_pie = df_pie.sort_values(by='Número de estudiantes', ascending=False)
df_pie.reset_index(drop=True, inplace=True)

#------------------------------------------------------------------------------------------------#
# GRÁFICOS
# MAPA 1
fig = go.Figure(data=go.Choropleth( 
                     locations=df_conteo_paises["País destino"],
                    z=df_conteo_paises["Número de intercambios"],
                    colorscale="Viridis",
                    colorbar=dict(thickness=10,
                           ticklen=10, tickcolor='rgb(255, 255, 255)',
                           tickfont=dict(size=10, color='rgb(255, 255, 255)')),
                    marker_line_color='darkgray',
                    marker_line_width=0.5,
                    #colorbar_title = 'Número de alumnos <br> en programas de <br> internacionalización',
                    hovertemplate = "%{Número de intercambios}: <br>Popularity: %{percent} </br> %{text}"
                 ))

fig.update_layout(
    autosize = True,
    #width=750,
    paper_bgcolor = 'rgb(54, 54, 54)',
    title_text='Alumnos en programas de internacionalización alrededor del mundo',
    title_font_color = 'rgb(255, 255, 255)',
    geo=dict(
        scope='world', resolution=110, projection_type='equirectangular',
        showcoastlines=True, showocean=True, showcountries=True,
        countrycolor='#829199', oceancolor='#343434', lakecolor='#132630',
        coastlinecolor='#829199',landcolor='#224354'))

# GRÁFICO 2: MAPA
fig2 = go.Figure(data=go.Choropleth( 
                    locations=df_conteo_paises["País destino"],
                    z=df_conteo_paises["Número de intercambios"],
                    colorscale="Viridis",
                    colorbar=dict(thickness=10,
                        ticklen=10, tickcolor='rgb(54, 54, 54)',
                        tickfont=dict(size=10, color='rgb(54, 54, 54)')),
                        marker_line_color='darkgray',
                    marker_line_width=0.5,
                    colorbar_title = 'Número de alumnos <br> en programas de <br> internacionalización',
                    #hovertemplate = "%{Número de intercambios}: <br>Popularity: %{percent} </br> %{text}"
                ))

fig2.update_layout(
    paper_bgcolor = 'rgb(255, 255, 255)',
    plot_bgcolor = 'rgb(255, 255, 255)',
    title_text='Alumnos en programas de internacionalización <br>alrededor del mundo',
    title_font_color = 'rgb(54, 54, 54)',
    geo=dict(
        scope='world', resolution=110, projection_type='natural earth',
        showcoastlines=True, showocean=True, showcountries=True,
        countrycolor='#829199', oceancolor='#343434', lakecolor='#132630',
        coastlinecolor='#829199',landcolor='#224354'))

# GRÁFICO 3: TREEMAP
fig3 = px.treemap(df_treemap, path=[px.Constant("Todos los estudiantes"), 'Escuela', 'Tipo de intercambio', 'Estatus de asignacion'], 
                     values = 'Promedio medio',
                     #hover_data=['iso_alpha'],
                     color='Número de estudiantes',
                     color_continuous_scale='RdBu',
                     #color_continuous_midpoint=np.average(df_not_nan['Promedio medio'], weights=df_not_nan['Número de estudiantes'])
                     )
fig3.update_traces(root_color="lightgrey")
fig3.update_layout(margin = dict(t=50, l=25, r=25, b=25))

# GRÁFICO 4: GRÁFICO DE SANKEY
fig4 = go.Figure(data = [go.Parcats(dimensions = [escuela_dim, tipo_dim, estatus_dim],
                                    line={'color': df_sankey["Escuela"],'colorscale':'RdBu'},
                                    labelfont={'size': 11, 'color':'#FFFFFF'},
                                    tickfont={'size': 10,'color':'#FFFFFF'})])

fig4.update_layout(hoverlabel_font_family = 'Arial', hoverlabel_font_size = 15,
                  margin = dict(t=30, l=120, r=180, b=30)) # paper_bgcolor = '#000000', #Color del background,

# GRÁFICO 5: PIE
fig5 = go.Figure(data=[go.Pie(labels=df_pie['Tipo de intercambio'], values=df_pie['Número de estudiantes'], textinfo='label+percent',
                             insidetextorientation='radial',
                             marker_colors = ['rgb(93, 109, 126)', 'rgb(247, 220, 111)']
                            )])
fig5.update_traces(hole=.4, hoverinfo="label+percent+name")
fig5.update_layout(hoverlabel_font_family = 'Arial', hoverlabel_font_size = 15,
                  annotations=[dict(text='Internacionalización', x=0.5, y=0.5, font_size=12, showarrow=False)],
                  margin = dict(t=30, l=120, r=180, b=30))

#------------------------------------------------------------------------------------------------#
# Row A
st.markdown('### Métricas sobre la opción en la que fueron seleccionados los estudiantes')

col1, col2, col3 = st.columns(3)
col1.metric("Primera opción", f"{porc_1era_opcion[0]}%", f"Año {year}: {porc_1era_opcion_año[0]}%")
col2.metric("Segunda opción", f"{porc_2da_opcion[0]}%", f"Año {year}: {porc_2da_opcion_año[0]}%")
col3.metric("Tercera opción", f"{porc_3era_opcion[0]}%", f"Año {year}: {porc_3era_opcion_año[0]}%")

# MAPA MUNDIAL
with st.container():
    st.write("---")
    col_1, col_2 = st.columns([2, 3])
    with col_1:
        st.subheader('Mapa del mundo')
        st.write('##')
        st.write(f'Países preferidos para programas de internacionalización en el año {year}:')
        st.write(df_conteo_paises_2.head(5))
    with col_2:
        st.plotly_chart(fig2, use_container_width=True)

#st.write(df)
st.write("---")
st.markdown('### Análisis por escuela, tipo de intercambio y opción en la que fueron asignados')

# RADIO (TREEMAP/SANKEY)
tipo_de_grafico = st.radio(
    "Selecciona el gráfico a visualizar: ",
    ('Gráfico de Sankey', 'Treemap'), index = 1)

if tipo_de_grafico == 'Gráfico de Sankey':
    st.write(fig4)
else:
    st.write(fig3)

#PIE
with st.container():
    st.write("---")
    col_1, col_2 = st.columns([3, 2])
    with col_1:
            st.plotly_chart(fig5, use_container_width=True) 
    with col_2:
        st.subheader(f'Tipo de internacionalización')
        st.write('##')
        st.write(f'Programas de internacionalización preferidos por estudiantes en el año {year}:')
        st.write(df_pie.head(5))
        