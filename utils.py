import streamlit as st
import pandas as pd
from config import *

def load_data():
    try:
        df_outgoing = pd.read_excel(FILE_PATH, sheet_name='Outgoing')
        df_password = pd.read_excel(FILE_PATH, sheet_name='Password')
        credentials = dict(zip(df_password['Source'], df_password['Password']))
        return df_outgoing, credentials
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None
