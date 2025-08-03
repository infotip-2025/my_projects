import pandas as pd
# import streamlit as st
# import plotly.express as px


def read():
    df = pd.read_csv('./pokemon.py')
    return df
