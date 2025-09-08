# pylint: disable=missing-module-docstring
import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    print("Creating data...")
    logging.error(os.listdir())
    logging.error("creating data")
    os.mkdir("data")

if "exercices_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# Sidebar
# Récupérer les thèmes distincts depuis memory_state
themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
themes = themes_df["theme"].tolist()

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        themes,                # 👈 prend les thèmes depuis la DB
        index=None,
        placeholder="Select theme",
    )
    st.write("You selected ", theme)


# with st.sidebar:
#     theme = st.selectbox(
#         "What would you like to review ?",
#         ["cross_joins", "GroupBy", "window_functions"],
#         index=None,
#         placeholder="Select theme",
#     )
#     st.write("You selected ", theme)
#
    exercice = con.execute(f"SELECT * FROM memory_state WHERE theme ='{theme}'").df().sort_values("last_reviewed").reset_index()
    st.write(exercice)

    # ... après avoir défini `exercice` ...
    try:
        # évite KeyError si l'index ne contient pas 0
        exercice_name = exercice.iloc[0]["exercise_name"]

        with open(f"answers/{exercice_name}.sql", "r") as f:
            answer = f.read()

        solution_df = con.execute(answer).df()

    except (IndexError, KeyError):
        # IndexError: dataframe vide -> pas de ligne 0
        # KeyError: colonne absente
        st.warning("Aucun exercice trouvé (sélectionne un thème dans la sidebar).")
        exercice_name = None
        answer = None
        solution_df = None

# Zone pour requête utilisateur
st.write("Enter your code")
query = st.text_area(label="Enter your code", key="user_input")
#
if query:
    result = con.execute(query).df()
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

# # Onglets
tab2, tab3 = st.tabs(["Tables", "solution_df"])

with tab2:
    try:
        exercice_table = exercice.iloc[0]["tables"]
    except (IndexError, KeyError, SyntaxError, ValueError):
        st.info("Aucune table à afficher pour le moment.")
    else:
        for table in exercice_table:
            st.write(f"Table : {table}")
            df_table = con.execute(f'SELECT * FROM "{table}"').df()
            st.dataframe(df_table)

#
with tab3:
    st.write(answer)
