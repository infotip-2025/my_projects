import pandas as pd
# import os
# import streamlit as st
# import plotly.express as px


def read(file_to_read):
    df = pd.read_csv(file_to_read)
    return df
