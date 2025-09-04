import streamlit as st
import pandas as pd
import duckdb

st.write("Hello World")

data = {"a" : [1, 2, 3], "b" : [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    input_text = st.text_area (label="Input text")
    st.write(duckdb.sql(input_text))
    st.dataframe(df)

