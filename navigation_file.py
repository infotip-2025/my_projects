import streamlit as st

pages = {
    "Weight page": [
        st.Page("/mount/src/my_projects/weight-checks-adoric-or-salter-mibody/adoric_health.py", title="Check body mass data"),
        # st.Page("manage_account.py", title="Manage your account"),
    ],
    "Pokemon page": [
        st.Page("/mount/src/my_projects/pokemon/pokemon.py", title="Pokemons"),
        # st.Page("trial.py", title="Try it out"),
    ],
}