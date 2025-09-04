import streamlit as st
import pandas as pd
import duckdb
import io


csv = '''
beverage,price
orange juice, 2.5
Expresso, 2
Tea,3
'''

csv2 = '''
food_item,food_price
cookie juice, 2.5
Chocolatine, 2
muffin, 3
'''

# Charger les DataFrames
beverage = pd.read_csv(io.StringIO(csv))
food_items = pd.read_csv(io.StringIO(csv2))

# Enregistrer les DataFrames dans DuckDB
duckdb.register("beverage", beverage)
duckdb.register("food_items", food_items)

# Solution attendue
answer = '''
SELECT * FROM beverage
CROSS JOIN food_items
'''
solution = duckdb.sql(answer).df()

# Sidebar
with st.sidebar:
    option = st.selectbox(
        "What would you like to review ?",
        ["Join", "GroupBy", "Window Functions"],
        index=None,
        placeholder="Select option",
    )
    st.write('You selected ', option)

# Zone pour requête utilisateur
st.write("Enter your code")
query = st.text_area(label="Enter your code", key="user_input")

if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

# Onglets
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("Table : Beverage")
    st.dataframe(beverage)
    st.write("Table : Food Items")
    st.dataframe(food_items)
    st.write("Expected result")
    st.dataframe(solution)

with tab3:
    st.write(answer)
