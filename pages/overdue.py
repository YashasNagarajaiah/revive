import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import INVOICE_PATH, SECONDARY_COLOR, LIGHT_COLOR

def display_overdue_page(username):
    st.title("Outstanding Invoices")
    try:
        df = pd.read_excel(INVOICE_PATH)
        user_specific_data = df[(df['Source'] == username) & (df['Invoice Status'] == 'Overdue')]

        if not user_specific_data.empty:
            fig = go.Figure(data=[go.Table(
                header=dict(values=['Invoice Status', 'Balance'],
                            fill_color=SECONDARY_COLOR,
                            align='left',
                            font=dict(color=LIGHT_COLOR, size=12)),
                cells=dict(values=[user_specific_data['Invoice Status'], user_specific_data['Balance']],
                           fill_color=LIGHT_COLOR,
                           align='left'))
            ])
            fig.update_layout(title='Outstanding Invoices')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("Great job! You have no outstanding invoices.")
    except Exception as e:
        st.error(f"Error loading invoice data: {str(e)}")
