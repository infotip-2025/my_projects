import pandas as pd
import os
# import streamlit as st
# import plotly.express as px


def read():
    df = pd.read_csv('data_pokemon/pokemon (4).csv')
    return df
