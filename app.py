#pylint: disable=missing-module-docstring

import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
bev,price
orange juice, 2.5
Expresso, 2
Tea,3
"""

CSV2 = """
food_item,food_price
cookie juice, 2.5
Chocolatine, 2
muffin, 3
"""

# Charger les DataFrames
beverage = pd.read_csv(io.StringIO(CSV))
food_items = pd.read_csv(io.StringIO(CSV2))

# Enregistrer les DataFrames dans DuckDB
duckdb.register("beverage", beverage)
duckdb.register("food_items", food_items)

# solution_df attendue
ANSWER_STR = """
SELECT * FROM beverage
CROSS JOIN food_items
"""
solution_df = duckdb.sql(ANSWER_STR).df()

# Sidebar
with st.sidebar:
    option = st.selectbox(
        "What would you like to review ?",
        ["Join", "GroupBy", "Window Functions"],
        index=None,
        placeholder="Select option",
    )
    st.write("You selected ", option)

# Zone pour requête utilisateur
st.write("Enter your code")
query = st.text_area(label="Enter your code", key="user_input")

if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    if len(result.columns) != len(solution_df.columns):  # replace with result
        st.write("Your code does not have the right columns")

        try:
            result = result[solution_df.columns]
            st.dataframe(result.compare(solution_df))
        except KeyError as e:
            st.write("Your code does not have the right columns")

        n_lines_difference = result.shape[0] - solution_df.shape[0]
        if n_lines_difference != 0:
            st.write(
                f"result has a {n_lines_difference} lines difference with the solution_df"
            )

# Onglets
tab2, tab3 = st.tabs(["Tables", "solution_df"])

with tab2:
    st.write("Table : Beverage")
    st.dataframe(beverage)
    st.write("Table : Food Items")
    st.dataframe(food_items)
    st.write("Expected result")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
