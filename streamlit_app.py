# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

from cryptography.hazmat.primitives import serialization

private_key_pem = st.secrets["connections"]["snowflake"]["private_key_pem"].encode()
p_key = serialization.load_pem_private_key(private_key_pem, password=None)
pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

conn = st.connection(
    "snowflake",
    account=st.secrets["connections"]["snowflake"]["account"],
    user=st.secrets["connections"]["snowflake"]["user"],
    private_key=pkb,
    role=st.secrets["connections"]["snowflake"]["role"],
    warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
    database=st.secrets["connections"]["snowflake"]["database"],
    schema=st.secrets["connections"]["snowflake"]["schema"],
)
session = conn.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# adding multi-select
# selections are stored in a var called `ingredients`, it's an object called LIST
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 6
)

# new section to display smoothiefroot nutrition info


# notice the ugly brackets if no ingredients are chosen, we can fix with an IF block
if ingredients_list:

    ingredients_string = '' # convert LIST to STRING

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '# += means add this to what's already in the var
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon") 
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(f'Your smoothie is ordered, {name_on_order}!', icon="✅")




