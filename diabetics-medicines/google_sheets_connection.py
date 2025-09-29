# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# url = "https://docs.google.com/spreadsheets/d/1Gc3Wi1vpTP4g5rnWuaRJDZWycZHvKO7F2xCv1ZGo0oU/edit?usp=sharing"
# url = 'https://docs.google.com/spreadsheets/d/1n3aDcsdgAMb17yXnmKZHUm4hK7P8exlkO6H0NdvLZZ8/edit?usp=edit'
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQnadO2nX23JArLFEhtOK60bmJ9JyHKqeqKL83KZn5gUCuZF-WXPyk-l9Mv-6E_VWzpatb9dbBpponf/pubhtml?gid=985363931&single=true'
id = '1n3aDcsdgAMb17yXnmKZHUm4hK7P8exlkO6H0NdvLZZ8'
conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(
    spreadsheet=id,
    # worksheet="Medicines_Diabetics",
    ttl="1m",
    usecols=[0, 1],
    nrows=3,
)
st.dataframe(data)


