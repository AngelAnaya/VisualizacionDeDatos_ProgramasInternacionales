import pandas as pd
import streamlit as st
import plotly.express as px

df = px.data.gapminder()

st.title("Streamlit - Search names")
st.dataframe(df)

year_options = df["year"].unique().tolist()
year = st.selectbox("Which year would you like to see?", year_options, 0)

continent_options = df["continent"].unique().tolist()
continent = st.selectbox("Which year would you like to see?", continent_options, 0)

df = df[(df['year'] == year) | (df['continent'] == continent)]

fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                hover_name="continent", log_x=True, size_max=55, 
                range_x = [100,100000], range_y = [25, 50])

fig.update_layout(width=400)
st.write(fig)