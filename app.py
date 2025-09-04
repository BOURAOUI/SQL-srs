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
food_item, food price
cookie juice, 2.5
Chocolatine, 2
muffin, 3
'''

food_items = pd.read_csv(io.StringIO(csv2))

answer = '''
SELECT * FROM beverages
CROSS JOIN food_items
'''

solution = duckdb.sql(answer).df()

beverages = pd.read_csv(io.StringIO(csv))
with st.sidebar:
    option = st.selectbox(
        "What would you like to reveiw ?",
        ["Join", "GoupBy", "Windows Functions"],
        index=None,
        placeholder="Select option",
    )
    st.write('You selected ', option)





st.write("Enter you code")
query = st.text_area(label="Enter your code",key="user_input")

if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("Table : Beverages")
    st.dataframe(beverages)
    st.write("Table : Food Items")
    st.dataframe(food_items)
    st.write("expected")
    st.dataframe(solution)

with tab3:
    st.write(answer)

