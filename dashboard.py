import streamlit as st
import pandas as pd
import plotly.express as px
from millify import prettify

st.set_page_config(page_title='Population Dashboard', layout="wide")
st.subheader('Word\'s Population Dashboard until 2022')

@st.cache_data
def load_data():
    df = pd.read_csv('world_population.csv')
    return df

df = load_data()

year_list = ['2022', '2020', '2015', '2010', '2000', '1990', '1980', '1970']

col1_row1, col2_row1, col3_row1 = st.columns(3)

continent = col1_row1.selectbox("Continent", df['Continent'].unique())
country = col2_row1.selectbox("Country", df.loc[df['Continent'] == continent, 'Country'])
year = col3_row1.selectbox("Year", year_list)

df_filtered_country = df[df['Country'] == country]
df_filtered_continent = df[df['Continent'] == continent]

col1_row2, col2_row2= st.columns(2, gap = "large")
col2_1, col2_2 = col2_row2.columns(2)
col1_row3, col2_row3 = st.columns(2)

df_filtered_country_pop = df_filtered_country[['1970 Population', '1980 Population', '1990 Population', '2000 Population', '2010 Population', '2015 Population', '2020 Population', '2022 Population']].T

fig_date = px.line(df_filtered_country_pop, title = country + ' Population ' , markers = True,
                    color_discrete_sequence=px.colors.sequential.Inferno)
fig_date.update_traces(name='')
fig_date.update_xaxes(title_text='Year')
fig_date.update_yaxes(title_text='Population')

x_labels = ['1970', '1980', '1990', '2000', '2010', '2015', '2020', '2022']
x_values = ['1970 Population', '1980 Population', '1990 Population', '2000 Population',
             '2010 Population','2015 Population', '2020 Population', '2022 Population']

fig_date.update_xaxes(ticktext=x_labels, tickvals=x_values)
col1_row2.plotly_chart(fig_date, use_container_width=True)

col2_1.metric(label=' ', value=' ')
col2_2.metric(label=' ', value=' ')

metric_col2_1 = ['Country', 'Capital', 'Continent', 'CCA3']

for metric in metric_col2_1:
    col2_1.metric(label=metric, value=str(df[df['Country'] == country][metric].iloc[0]))

metric_col2_2 = ['Area (km²)', 'Density (per km²)', 'Growth Rate' ]

for metric in metric_col2_2:
    col2_2.metric(label=metric, value=prettify(str(df[df['Country'] == country][metric].iloc[0])))

col2_2.metric(label='World Population Percentage', value=((str(df[df['Country'] == country]['World Population Percentage'].iloc[0])))+"%")

col2_row2.metric(label=year + ' Population', value=prettify(str(df[df['Country'] == country][ year + ' Population'].iloc[0])))

df_filtered_continent = df_filtered_continent.sort_values(by = '2022 Population', ascending = False)

fig_date = px.pie(df_filtered_continent.iloc[:10], names = 'Country', values= year + ' Population',
                   title = ('Population Share Across ' + continent + '\'s Countries in ' + year),
                   color_discrete_sequence=px.colors.sequential.Inferno)
col1_row3.plotly_chart(fig_date, use_container_width=True)

fig_date = px.bar(df_filtered_continent, y = 'Area (km²)', x ='Country',
                   title = (continent + '\'s Country: Contemporary Area Distribution'),
                   color_discrete_sequence=px.colors.sequential.Inferno)
col2_row3.plotly_chart(fig_date, use_container_width=True)

fig_date = px.scatter_geo(df_filtered_continent, locations='CCA3', color="Country", hover_name="Country",
                           size = '2022 Population', title = ('Population Across ' + continent + '\'s Countries in 2022'),
                           color_discrete_sequence=px.colors.sequential.Inferno,  projection = 'equirectangular')
fig_date.update_geos(
    projection_scale=1,
    showcountries=True,
    showcoastlines = True,
    showocean = True,
    showland = True,
    showsubunits = True,
    bgcolor = '#0e1117',
    landcolor = '#dbab3b',
    oceancolor = '#0e1117'

)
st.plotly_chart(fig_date, use_container_width=True)

