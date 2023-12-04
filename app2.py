import streamlit as st
import math
from datetime import datetime

st.title("CIS102: My 2nd App")
st.markdown("Welcome to my App #2.")
st.header("Slider widget")

x = st.slider('Your number', help="Please choose a number by sliding through the bar")
st.write('$x^2$ = ', x * x)

st.write("---") # line separater

# note `r` before quotation mark below
# it means `\` in the string should be treated as is
# instead of an escape symbol
theta = st.slider(r'θ: Angle in degrees', min_value=-180, max_value=180, step=5)
st.write(r'$Cos( \theta )$ = ', math.cos(theta/180.*math.pi))

st.write("---")

beta = st.slider(r'β: Angle in degrees', value = 30, min_value=-180, max_value=180, step=5)
st.write(r'$Sin( \beta )$ = ', math.sin(beta/180.*math.pi))

st.write("---")
start_time = st.slider(
      "When do you start?",
     value=datetime(2020, 1, 1, 9, 30),
     format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)
