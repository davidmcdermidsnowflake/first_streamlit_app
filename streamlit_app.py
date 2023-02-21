import streamlit as st
import pandas as p
import requests as r
import snowflake.connector
from urllib.error import URLError

def normalize(fruit_choice):
    fruityvice_response = r.get("https://fruityvice.com/api/fruit/" + choice)
    fvr_json = fruityvice_response.json()
    return p.json_normalize(fvr_json)
 
def insert_row_snowflake(new_fruit):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])   
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit "')")
        my_cnx.close()
        return "Thanks for adding " + new_fruit
    
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
try:
  choice = st.text_input("what fruit would you like information about")
  if not choice:
    st.error("please select a fruit to get more information.")
  else:
    st.dataframe(normalize(choice))
except URLError as e:
  st.error()

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

if(st.button("Get Fruit List")):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])   
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    st.dataframe(my_data_rows)
    

addchoice = st.text_input("what fruit would you like to add")
res = insert_row_snowflake(addchoice)
st.write(res)
