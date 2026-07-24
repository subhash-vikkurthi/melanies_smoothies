# Import python packages
import streamlit as st
import os
import requests
# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)


name_on_order = st.text_input("Name of the smoothie:")
st.write("name of the smoothie will be", name_on_order)

from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),(col("SEARCH_ON")))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingrediants_list = st.multiselect(
    'choose_upto 5 fruits:',
    my_dataframe,
    max_selections=5)

if ingrediants_list:
    ingredients_string = ""
    for fruits_choosen in ingrediants_list:
        ingredients_string += fruits_choosen +' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
      
        st.subheader(fruits_choosen + " Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruits_choosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('submit_order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


# New section to display smoothiefroot nutrition information

import requests

#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

#st.text(smoothiefroot_response.json())

#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


