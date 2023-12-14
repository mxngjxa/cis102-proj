import streamlit as st
from PIL import Image
import pandas as pd
import math
import numpy as np
import folium
from streamlit_folium import folium_static
from datetime import datetime
import plotly.express as px

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

#sideboarding 


with st.sidebar.expander("Price range"):
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

def string_b():
    nice_looking_string = ""
    if not boroughs:
        nice_looking_string = "You have not selected any boroghs to visualize. "
    else: 
        nice_looking_string += "You have selected: "
        for b in boroughs:
            nice_looking_string += b
            nice_looking_string += " - "
        nice_looking_string += "as your boroughs. "

    return nice_looking_string
boroughs_sentence = string_b()


st.write(f"Currently, the selected Price Range is from `{min_price}` to `{max_price}`. {boroughs_sentence}You can change this at any time in the sidebar")


#Dashboarding

