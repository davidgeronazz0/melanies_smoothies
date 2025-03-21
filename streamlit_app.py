# Import python packages
import streamlit as st
import requests
import pandas as pd
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(" :cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your Smoothie!")

name_on_order = st.text_input('Name on smoothie')
st.write('The name on the Smoothie will be: ', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect('Choose up to 5 ingredients', 
                                 my_dataframe, 
                                 max_selections = 5)
if ingredient_list:
    ingredients_string = ''
    for fruit in ingredient_list:
        ingredients_string += fruit + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit,' is ', search_on, '.')
        
        st.subheader(fruit + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    # st.write(ingredients_srting)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """' )"""
    
    time_to_submit = st.button('Submit Order')

    #st.write(my_insert_stmt)
    #st.stop()

    if time_to_submit:
        session.sql(my_insert_stmt).collect()   
        st.success('Your Smoothie is ordered!', icon="✅")
        
        


