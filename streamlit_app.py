# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True), can be re-added to inspect DF

# adding multi-select
# selections are stored in a var called `ingredients`, it's an object called LIST
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 6
)

# display the list
# st.write(ingredients_list)
# st.text(ingredients_list)

# notice the ugly brackets if no ingredients are chosen, we can fix with an IF block
if ingredients_list:

    ingredients_string = '' # convert LIST to STRING

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '# += means add this to what's already in the var

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(f'Your smoothie is ordered, {name_on_order}!', icon="✅")




