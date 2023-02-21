import streamlit as st
import pandas as p
import requests as r
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = p.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)
st.header("Fruityvice Fruit Advice")
choice = st.text_input("what fruit would you like information about", "kiwi")
st.write("the user entered", choice)

fruityvice_response = r.get("https://fruityvice.com/api/fruit/" + choice)
fvr_json = fruityvice_response.json()


fvr_json_norm = p.json_normalize(fvr_json)
st.dataframe(fvr_json_norm)

st.stop()
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

addchoice = st.text_input("what fruit would you like information about", "kiwi")

st.write("the user entered", addchoice)
