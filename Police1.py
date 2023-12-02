import streamlit as st
import pandas as pd 
import numpy as np
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt 
import plotly.express as px


#   1er cambio: Darle una nueva configuración a la página
st.set_page_config(
    page_title="Police Incident Reports",
    page_icon=":policeman:",
    layout="wide"
)

st.title('Police Incident Reports from 2018 to 2020 in San Francisco')

data = pd.read_csv(r"/Users/gonzalo/Downloads/Police_Department_Incident_Reports__2018_to_Present.csv")
df = data.fillna(method='bfill')

st.markdown("The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, which details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location, and resolution")

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Date']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']

#2 cambio mostrar solo las primeros 5 filas con un cambio de colores
st.dataframe(mapa.head().style.set_properties(**{'background-color': 'white', 'color': 'black'}))
subset_data2 = mapa


police_district_input = st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist())


if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

subset_data

st.markdown("It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.")
st.markdown("Crime location in San Francisco")

#3er cambio : mapa interactivo con el mapa
st.subheader('Interactive Crime Map')
fig_map = px.scatter_mapbox(subset_data, lat='lat', lon='lon', color='Incident Category', zoom=10)
fig_map.update_layout(mapbox_style="carto-positron")  
st.plotly_chart(fig_map)



#4to cambio gráfico de linea interactivo con la fecha
st.subheader('Interactive Line Chart - Incidents over Time')
fig_line = px.line(subset_data['Date'].value_counts(), title='Incidents over Time', labels={'value': 'Number of Incidents'})
st.plotly_chart(fig_line)


#5to cambio gráfico de barras interactivas
st.subheader('Type of crimes committed (Interactive)')
fig = px.bar(x=subset_data['Incident Category'].value_counts().index,
             y=subset_data['Incident Category'].value_counts().values,
             labels={'y': 'Number of Incidents', 'x': 'Incident Category'},
             title='Type of crimes committed (Interactive)')
st.plotly_chart(fig)

agree = st.button('Click to see Incident Subcategories')
if agree:
    st.subheader('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())


#6to cambio, cambio de formato el el grafico de pastel
resolution_counts = subset_data['Resolution'].value_counts()
fig, ax1 = plt.subplots()
colors = plt.cm.Paired(range(len(resolution_counts)))
ax1.pie(resolution_counts, labels=resolution_counts.index, autopct='%1.1f%%', startangle=20, colors=colors)
ax1.set_title('Resolution status')
ax1.legend(resolution_counts.index, title='Resolution', bbox_to_anchor=(1, 0.8))
ax1.axis('equal')
plt.tight_layout()
st.markdown('### Resolution Status (Matplotlib)')
st.pyplot(fig)