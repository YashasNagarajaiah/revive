import streamlit as st
import pandas as pd
from config import FILE_PATH

def user_login():
    st.title("Revive Platform - Login")
    try:
        df_password = pd.read_excel(FILE_PATH, sheet_name='Password')
        credentials = dict(zip(df_password['Source'], df_password['Password']))

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in credentials and credentials[username] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Logged in as {username}")
                st.rerun()
            else:
                st.error("Invalid credentials")
    except Exception as e:
        st.error(f"Error loading credentials: {str(e)}")