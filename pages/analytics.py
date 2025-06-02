import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import FILE_PATH
import plotly.figure_factory as ff

def display_analytics_page(username):
    st.title(f"Data Analytics for {username}")
    df_outgoing = pd.read_excel(FILE_PATH, sheet_name='Outgoing')
    user_df = df_outgoing[df_outgoing['Source'] == username]

    if not user_df.empty:
        st.subheader("Waste Collection Overview")
        total_weight = user_df['Weight (Kg)'].sum()
        avg_weight = user_df['Weight (Kg)'].mean()
        max_weight = user_df['Weight (Kg)'].max()
        num_collections = len(user_df)

        col1, col2 = st.columns(2)
        col1.metric("Total Waste Collected", f"{total_weight:.2f} Kg")
        col2.metric("Number of Collections", num_collections)
        col1.metric("Average Weight per Collection", f"{avg_weight:.2f} Kg")
        col2.metric("Maximum Weight in a Collection", f"{max_weight:.2f} Kg")

        st.subheader("Waste Composition Analysis")
        waste_composition = user_df.groupby('Waste Streams')['Weight (Kg)'].sum().sort_values(ascending=False)
        fig_composition = px.pie(values=waste_composition.values, names=waste_composition.index, title="Waste Composition by Weight")
        st.plotly_chart(fig_composition, use_container_width=True)

        st.subheader("Waste Collection Trend")
        user_df['Incoming Date'] = pd.to_datetime(user_df['Incoming Date'])
        daily_waste = user_df.groupby('Incoming Date')['Weight (Kg)'].sum().reset_index()

        if not daily_waste.empty:
            fig_trend = px.line(daily_waste, x='Incoming Date', y='Weight (Kg)', title='Daily Waste Collection Trend')
            st.plotly_chart(fig_trend, use_container_width=True)

        # Additional analytics start here
        
        # 1. Monthly Collection Heatmap
        st.subheader("Monthly Collection Heatmap")
        user_df['Month'] = user_df['Incoming Date'].dt.month
        user_df['Year'] = user_df['Incoming Date'].dt.year
        monthly_pivot = user_df.pivot_table(
            values='Weight (Kg)',
            index='Month',
            columns='Year',
            aggfunc='sum'
        ).fillna(0)
        
        fig_heatmap = px.imshow(
            monthly_pivot,
            labels=dict(x="Year", y="Month", color="Weight (Kg)"),
            title="Monthly Collection Heatmap",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # 2. Waste Stream Bar Chart
        st.subheader("Top Waste Streams")
        fig_bar = px.bar(
            waste_composition.reset_index(),
            x='Waste Streams',
            y='Weight (Kg)',
            title="Waste Streams by Weight",
            color='Weight (Kg)',
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # 3. Weight Distribution Histogram
        st.subheader("Weight Distribution Analysis")
        fig_hist = px.histogram(
            user_df,
            x='Weight (Kg)',
            nbins=30,
            title="Distribution of Collection Weights",
            color_discrete_sequence=['lightblue']
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        # 4. Day of Week Analysis
        st.subheader("Day of Week Analysis")
        user_df['Day'] = user_df['Incoming Date'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_avg = user_df.groupby('Day')['Weight (Kg)'].mean().reindex(day_order)
        
        fig_dow = px.bar(
            x=daily_avg.index,
            y=daily_avg.values,
            title="Average Collection by Day of Week",
            labels={'x': 'Day', 'y': 'Average Weight (Kg)'},
            color=daily_avg.values,
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_dow, use_container_width=True)

        # 5. Box Plot by Waste Stream
        st.subheader("Weight Distribution by Waste Stream")
        fig_box = px.box(
            user_df,
            x='Waste Streams',
            y='Weight (Kg)',
            title="Weight Distribution by Waste Stream"
        )
        st.plotly_chart(fig_box, use_container_width=True)

        # 6. Cumulative Weight Collection
        st.subheader("Cumulative Weight Collection")
        daily_waste['Cumulative_Weight'] = daily_waste['Weight (Kg)'].cumsum()
        fig_cumulative = px.line(
            daily_waste,
            x='Incoming Date',
            y='Cumulative_Weight',
            title="Cumulative Weight Collection Over Time"
        )
        st.plotly_chart(fig_cumulative, use_container_width=True)

        # 7. Monthly Totals
        st.subheader("Monthly Collection Totals")
        user_df['Month_Year'] = user_df['Incoming Date'].dt.strftime('%B %Y')
        monthly_totals = user_df.groupby('Month_Year')['Weight (Kg)'].sum().reset_index()
        fig_monthly = px.bar(
            monthly_totals,
            x='Month_Year',
            y='Weight (Kg)',
            title="Monthly Collection Totals",
            color='Weight (Kg)',
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

        # 8. Waste Stream Time Series
        st.subheader("Waste Stream Trends")
        waste_stream_time = user_df.pivot_table(
            values='Weight (Kg)',
            index='Incoming Date',
            columns='Waste Streams',
            aggfunc='sum'
        ).fillna(0)
        
        fig_streams = px.line(
            waste_stream_time,
            title="Waste Stream Collection Over Time",
            labels={'value': 'Weight (Kg)', 'variable': 'Waste Stream'}
        )
        st.plotly_chart(fig_streams, use_container_width=True)

        # 9. Collection Frequency Calendar
        st.subheader("Collection Frequency Calendar")
        user_df['Date'] = user_df['Incoming Date'].dt.date
        daily_counts = user_df.groupby('Date').size().reset_index()
        daily_counts.columns = ['Date', 'Collections']
        
        fig_calendar = px.scatter(
            daily_counts,
            x='Date',
            y='Collections',
            size='Collections',
            title="Collection Frequency Calendar",
            color='Collections',
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_calendar, use_container_width=True)

        # 10. Statistical Summary
        st.subheader("Statistical Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Weight Statistics by Waste Stream")
            stats_df = user_df.groupby('Waste Streams')['Weight (Kg)'].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(2)
            st.dataframe(stats_df)
        
        with col2:
            st.write("Recent Collections")
            recent = user_df.sort_values('Incoming Date', ascending=False).head()
            st.dataframe(recent[['Incoming Date', 'Waste Streams', 'Weight (Kg)']])

    else:
        st.info("No data available for analysis. Please ensure you have waste collection records.")
