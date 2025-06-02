import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from config import FILE_PATH, PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR_1
from styles import load_css


def calculate_kpis(df):
    """Calculate KPIs for month-over-month comparison."""
    df['Month'] = pd.to_datetime(df['Incoming Date']).dt.strftime('%Y-%m')
    current_month = pd.Timestamp.now().strftime('%Y-%m')
    prev_month = df[df['Month'] != current_month]['Month'].max()

    # Metrics for the current month
    current_metrics = {
        'weight': df[df['Month'] == current_month]['Weight (Kg)'].sum(),
        'collections': df[df['Month'] == current_month]['IS Number'].nunique()
    }

    # Metrics for the previous month
    prev_metrics = {
        'weight': df[df['Month'] == prev_month]['Weight (Kg)'].sum() if prev_month else 0,
        'collections': df[df['Month'] == prev_month]['IS Number'].nunique() if prev_month else 0
    }

    # Month-over-month growth
    mom_growth = ((current_metrics['weight'] - prev_metrics['weight']) / prev_metrics['weight'] * 100) if prev_metrics['weight'] else 0

    return {
        'total_weight': df['Weight (Kg)'].sum(),
        'total_collections': df['IS Number'].nunique(),
        'current_month_weight': current_metrics['weight'],
        'current_month_collections': current_metrics['collections'],
        'prev_month_weight': prev_metrics['weight'],
        'prev_month_collections': prev_metrics['collections'],
        'mom_growth': mom_growth
    }


def calculate_best_month(df):
    """Calculate the best month based on total weight collected."""
    monthly_weights = df.groupby('Month')['Weight (Kg)'].sum()
    best_month_raw = monthly_weights.idxmax() if not monthly_weights.empty else None
    best_month_weight = monthly_weights.max() if not monthly_weights.empty else 0
    
    # Format best month
    best_month = pd.to_datetime(best_month_raw).strftime('%B %Y') if best_month_raw else "N/A"
    return best_month, best_month_weight


def display_overview(username):
    """Display the overview dashboard."""
    st.markdown(load_css(), unsafe_allow_html=True)
    st.title(f"Overview for {username}")

    # Load data
    df_outgoing = pd.read_excel(FILE_PATH, sheet_name='Outgoing')
    user_df = df_outgoing[df_outgoing['Source'] == username]

    if not user_df.empty:
        # Calculate KPIs
        kpis = calculate_kpis(user_df)
        best_month, best_month_weight = calculate_best_month(user_df)

        # Display KPI Rows (2 rows, 4 columns each)
        st.subheader("Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Weight Collected", f"{kpis['total_weight']:,.2f} Kg")
        col2.metric("Total Collections", f"{kpis['total_collections']}")
        col3.metric("This Month's Weight", f"{kpis['current_month_weight']:,.2f} Kg")
        col4.metric("This Month's Collections", f"{kpis['current_month_collections']}")

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Previous Month's Weight", f"{kpis['prev_month_weight']:,.2f} Kg")
        col6.metric("Previous Month's Collections", f"{kpis['prev_month_collections']}")
        col7.metric("Best Month", best_month, f"{best_month_weight:,.2f} Kg")
        col8.metric("Month-over-Month Growth", f"{kpis['mom_growth']:+.1f}%")

        # Colorful Bar Chart for Waste Streams Distribution using Altair
        st.subheader("Waste Streams Distribution")
        waste_stream_data = user_df.groupby('Waste Streams')['Weight (Kg)'].sum().reset_index()
        chart = alt.Chart(waste_stream_data).mark_bar().encode(
            x=alt.X('Waste Streams', sort='-y', title='Waste Streams'),
            y=alt.Y('Weight (Kg)', title='Weight (Kg)'),
            color=alt.Color('Waste Streams', scale=alt.Scale(scheme='category20')),
            tooltip=['Waste Streams', 'Weight (Kg)']
        ).properties(
            title='Waste Streams Contribution',
            width='container',
            height=400
        )
        st.altair_chart(chart, use_container_width=True)

        # Time Series Visualization for Daily Trends using Altair
        st.subheader("Daily Waste Collection Trend")
        user_df['Incoming Date'] = pd.to_datetime(user_df['Incoming Date'])
        daily_data = user_df.groupby('Incoming Date').agg({
            'Weight (Kg)': 'sum',
            'IS Number': pd.Series.nunique
        }).reset_index()
        line_chart = alt.Chart(daily_data).mark_line(point=True).encode(
            x=alt.X('Incoming Date', title='Date'),
            y=alt.Y('Weight (Kg)', title='Weight (Kg)'),
            tooltip=['Incoming Date', 'Weight (Kg)']
        ).properties(
            title='Daily Waste Collection Trend',
            width='container',
            height=400
        )
        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.warning("No data available for this user.")




