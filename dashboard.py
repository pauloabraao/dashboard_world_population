import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
df = pd.read_csv('world_population.csv')

continent = st.sidebar.selectbox("Continent", df['Continent'].unique())
country = st.sidebar.selectbox("Country", df.loc[df['Continent'] == continent, 'Country'])

df_filtered_country = df[df['Country'] == country]
df_filtered_continent = df[df['Continent'] == continent]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

fig_date = px.line(df_filtered_country[['1970 Population', '1980 Population', '1990 Population', '2000 Population', '2010 Population', '2015 Population', '2020 Population', '2022 Population']].T, title = country + ' Population ' , markers = True)
fig_date.update_traces(name='')
fig_date.update_xaxes(title_text='Year')
fig_date.update_yaxes(title_text='Population')

x_labels = ['1970', '1980', '1990', '2000', '2010', '2015', '2020', '2022']
x_values = ['1970 Population', '1980 Population', '1990 Population', '2000 Population', '2010 Population','2015 Population', '2020 Population', '2022 Population']

fig_date.update_xaxes(ticktext=x_labels, tickvals=x_values)
col1.plotly_chart(fig_date, use_container_width=True)

df_filtered_continent = df_filtered_continent.sort_values(by = '2022 Population', ascending = False)

fig_date = px.pie(df_filtered_continent.iloc[:10], names = 'Country', values='2022 Population', title = 'Population Share Across ' + continent + '\'s Countries in 2022')
col2.plotly_chart(fig_date, use_container_width=True)

fig_date = px.scatter_geo(df_filtered_continent, locations='CCA3', color="Country", hover_name="Country" , size = '2022 Population', title = 'Population Across ' + continent + '\'s Countries in 2022')
col3.plotly_chart(fig_date, use_container_width=True)

fig_date = px.bar(df_filtered_continent, y = 'Area (km²)', x ='Country', title = continent + '\'s Country: Contemporary Area Distribution')
col4.plotly_chart(fig_date, use_container_width=True)

