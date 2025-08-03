import pandas as pd
# import streamlit as st
# import plotly.express as px


def read():
    df = pd.read_csv('./data/pokemon (4).csv')
    return df
