import streamlit as st
import pandas as pd
from io import BytesIO
from config import DOWNLOADS_PATH

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output.getvalue()

def display_downloads_page(username):
    st.title("Download Your Reports")
    try:
        sheets = ['Images', 'Sustainability', 'Segregation']
        data_frames = {}
        for sheet in sheets:
            df = pd.read_excel(DOWNLOADS_PATH, sheet_name=sheet)
            user_specific_data = df[df['Source'] == username]
            if not user_specific_data.empty:
                data_frames[sheet] = to_excel(user_specific_data)

        for sheet, data in data_frames.items():
            if data:
                st.download_button(
                    label=f"Download {sheet} Report",
                    data=data,
                    file_name=f"{username}_{sheet.lower()}_report.xlsx",
                    mime="application/vnd.ms-excel"
                )
    except Exception as e:
        st.error(f"Error loading downloads data: {str(e)}")
