import streamlit as st
from PIL import Image
import pandas as pd
import math
import numpy as np
import folium
from streamlit_folium import folium_static
from datetime import datetime
import plotly.express as px
import os

image = Image.open('ft-logo.png')
st.image(image, use_column_width=False)

#load data
@st.cache_data
def get_data():
    csv = "nyc_2019_airbnb_data.csv"
    try:
        st.write("loading data ... success!")
        return pd.read_csv(csv)
    except pd.errors.ParserError as e:
        st.write(f"loading error: {e}")
        return None

df = get_data()

#title and important information


st.header('Final Project CIS 102')
st.subheader('Mingjia "Jacky" Guan - 14/12/2023')

st.markdown("""

This is my final project in Prof. Qu Zheng's Introduction to Computing (CIS 102) class. In this project, 
a dashboard was created to manipulate Airbnb data from NYC from 2019. 


This project has used various python packages such as `pandas`, `folium`, `datetime`, and `plotly` to visualize the data presented.


The data we are using contains several attributes which all serve to characterize each individual Airbnb location in NYC. 
""")
st.write("These columns are:", df.columns)

st.write(f"Overall, the dataframe has {len(df)} entries, making it quite a substantial dataset. The first few rows in the dataset looks something like this: ")

st.dataframe(df.head())

# Set default values for the slider
default_values = (50, 300)

# min and max values
min_price = st.number_input("Min Price",  df.price.min(), df.price.max(), default_values[0], step=1)
max_price = st.number_input("Max Price", df.price.min(), df.price.max(), default_values[1], step=1)

# Set default values for the slider based on user input
values = st.slider(
    "Price range",
    df.price.min(),
    df.price.max(),
    (min_price, max_price),
    step=1
)

min_price, max_price = values


boroughs = st.sidebar.multiselect("Borough selection", df['neighbourhood_group'].unique())

filtered_neighborhoods = df[df['neighbourhood_group'].isin(boroughs)]['neighbourhood'].unique()

selected_neighborhoods = st.sidebar.multiselect("Neighborhood selection", sorted(filtered_neighborhoods))



def string_b(large, small):
    ret_str = str()
    if not large and not small:
        ret_str = "You have not selected any boroghs/neighborhoods to visualize. "
    elif large or small: 
        ret_str += "You have selected: "
        if large:
            ret_str += ", ".join(large)
            ret_str += " as your borough(s); "
        if small:
            ret_str += ", ".join(small)
            ret_str += " as your neighborhood(s). "
    return ret_str


boroughs_sentence = string_b(boroughs, selected_neighborhoods)

st.write(f"Now, onto the dashboarding part. Currently, the selected price range is from `{min_price}` to `{max_price}`. {boroughs_sentence}You can change this at any time in the sidebar")

filtered_data = df.query(f"price>={min_price}").query(f"price<={max_price}").query(f"neighbourhood_group == {boroughs}").query(f"neighbourhood == {selected_neighborhoods}")

if len(filtered_data) == 0:
    st.markdown(f"""

    There currently {len(filtered_data)} Airbnb units available in your given price range of \${min_price} to \${max_price}. 
    Perhaps you would like to change your price range or location filters?

    """)
else: 
        st.markdown(f"""

    There currently {len(filtered_data)} Airbnb units available in {" - ".join(boroughs)} in the neighborhoods 
    {", ".join(selected_neighborhoods)} in your given price range of \${min_price} to \${max_price}.
    

    """)

st.dataframe(filtered_data)


st.header("Let's see where these units are")

listings = filtered_data[["name", "neighbourhood", "latitude", "longitude", "host_name", 'room_type', 'price']].dropna(how="any")

m = folium.Map(location=(40.748065, -73.734173), zoom_start=10)


for index, row in listings.iterrows():
    name = row["name"]
    hood = row["neighbourhood"]
    lat = row["latitude"]
    lon = row["longitude"]
    host = row["host_name"]
    room = row["room_type"]
    price = row["price"]

    folium.Marker(
        (lat, lon), popup=f"NAME: {name} \n\nNEIGHBORHOOD: {hood} \n\nHOST NAME: {host} \n\nROOM TYPE: {room}", tooltip=f"Price: \${price}"
    ).add_to(m)

folium_static(m)
