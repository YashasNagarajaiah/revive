import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import FILE_PATH, EMISSION_FACTORS, SECONDARY_COLOR, PRIMARY_COLOR

def calculate_co2_emission(df):
    """Calculate CO2 emissions for each waste stream"""
    df['CO2 Emission'] = df.apply(lambda x: (x['Weight (Kg)'] / 1000) * EMISSION_FACTORS.get(x['Waste Streams'], 0), axis=1)
    return df

def calculate_monthly_changes(df):
    """Calculate month-over-month changes"""
    df['Month'] = pd.to_datetime(df['Incoming Date']).dt.strftime('%Y-%m')
    current_month = df['Month'].max()
    prev_month = df[df['Month'] != current_month]['Month'].max()
    
    current_metrics = {
        'co2': df[df['Month'] == current_month]['CO2 Emission'].sum(),
        'carbon': df[df['Month'] == current_month]['CO2 Emission'].sum() / 3.67,
        'trees': 0.0164 * df[df['Month'] == current_month]['CO2 Emission'].sum(),
        'diesel': 0.372 * df[df['Month'] == current_month]['CO2 Emission'].sum(),
        'lamps': 0.04 * df[df['Month'] == current_month]['CO2 Emission'].sum(),
        'coal': 0.5 * df[df['Month'] == current_month]['CO2 Emission'].sum()
    }
    
    prev_metrics = {
        'co2': df[df['Month'] == prev_month]['CO2 Emission'].sum(),
        'carbon': df[df['Month'] == prev_month]['CO2 Emission'].sum() / 3.67,
        'trees': 0.0164 * df[df['Month'] == prev_month]['CO2 Emission'].sum(),
        'diesel': 0.372 * df[df['Month'] == prev_month]['CO2 Emission'].sum(),
        'lamps': 0.04 * df[df['Month'] == prev_month]['CO2 Emission'].sum(),
        'coal': 0.5 * df[df['Month'] == prev_month]['CO2 Emission'].sum()
    }
    
    changes = {
        'co2': ((current_metrics['co2'] - prev_metrics['co2']) / prev_metrics['co2'] * 100) if prev_metrics['co2'] else 0,
        'carbon': ((current_metrics['carbon'] - prev_metrics['carbon']) / prev_metrics['carbon'] * 100) if prev_metrics['carbon'] else 0,
        'trees': current_metrics['trees'] - prev_metrics['trees'],
        'diesel': current_metrics['diesel'] - prev_metrics['diesel'],
        'lamps': current_metrics['lamps'] - prev_metrics['lamps'],
        'coal': current_metrics['coal'] - prev_metrics['coal']
    }
    
    return changes

def display_sustainability_report(username):
    st.title(f"Environmental Impact Report for {username}")
    
    # Load and prepare data
    try:
        df_outgoing = pd.read_excel(FILE_PATH, sheet_name='Outgoing')
        user_df = df_outgoing[df_outgoing['Source'] == username].copy()
        user_df = calculate_co2_emission(user_df)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    if not user_df.empty:
        # Calculate metrics
        total_co2_emission = user_df['CO2 Emission'].sum()
        total_carbon_emission = total_co2_emission / 3.67
        trees = 0.0164 * total_co2_emission
        diesel = 0.372 * total_co2_emission
        lamps = 0.04 * total_co2_emission
        coal = 0.5 * total_co2_emission

        # Calculate month-over-month changes
        changes = calculate_monthly_changes(user_df)

        # Display metrics with deltas
        st.subheader("Overall Environmental Impact")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("CO2 Emissions Prevented", 
                   f"{total_co2_emission:,.2f} Kg",
                   f"{changes['co2']:+.1f}% from last month")
        col2.metric("Carbon Footprint Reduced", 
                   f"{total_carbon_emission:,.2f} Kg", 
                   f"{changes['carbon']:+.1f}% from last month")
        col3.metric("Equivalent Trees Planted", 
                   f"{trees:,.0f}",
                   f"{changes['trees']:+.0f} trees from last month")

        col1, col2, col3 = st.columns(3)
        col1.metric("Diesel Saved", 
                   f"{diesel:,.2f} Liters",
                   f"{changes['diesel']:+.0f} liters from last month")
        col2.metric("Energy Conserved", 
                   f"{lamps:,.0f} Lamp Hours",
                   f"{changes['lamps']:+.0f} hours from last month")
        col3.metric("Coal Consumption Avoided", 
                   f"{coal:,.2f} Kg",
                   f"{changes['coal']:+.0f} kg from last month")

        # CO2 Emission by Waste Stream
        st.subheader("CO2 Emission Analysis")
        
        waste_stream_emissions = user_df.groupby('Waste Streams')['CO2 Emission'].sum().reset_index().sort_values('CO2 Emission', ascending=False)
        
        fig_emissions = px.bar(
            waste_stream_emissions,
            x='Waste Streams',
            y='CO2 Emission',
            title='CO2 Emissions Prevented by Waste Stream',
            color='CO2 Emission',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_emissions, use_container_width=True)

        # Environmental Impact Over Time
        st.subheader("Impact Trends")
        fig_impact = px.area(
            user_df.groupby('Incoming Date')[['CO2 Emission', 'Weight (Kg)']].sum().reset_index(),
            x='Incoming Date',
            y=['CO2 Emission', 'Weight (Kg)'],
            title='Environmental Impact Over Time',
            color_discrete_sequence=[SECONDARY_COLOR, PRIMARY_COLOR]
        )
        st.plotly_chart(fig_impact, use_container_width=True)

        # Waste Stream Composition Heatmap
        st.subheader("Waste Stream Analysis")
        pivot_df = user_df.pivot_table(
            values='Weight (Kg)',
            index='Incoming Date',
            columns='Waste Streams',
            aggfunc='sum'
        ).fillna(0)
        
        fig_heatmap = px.imshow(
            pivot_df,
            labels=dict(x="Waste Streams", y="Date", color="Weight (Kg)"),
            title="Waste Stream Composition Over Time",
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Cumulative Impact Analysis
        st.subheader("Cumulative Impact")
        user_df['Cumulative_CO2'] = user_df['CO2 Emission'].cumsum()
        
        fig_cumulative = px.line(
            user_df.groupby('Incoming Date')['Cumulative_CO2'].last().reset_index(),
            x='Incoming Date',
            y='Cumulative_CO2',
            title='Cumulative CO2 Emissions Prevented',
            line_shape='spline'
        )
        st.plotly_chart(fig_cumulative, use_container_width=True)

        # Monthly Performance Analysis
        st.subheader("Monthly Performance")
        monthly_impact = user_df.groupby('Month').agg({
            'CO2 Emission': 'sum',
            'Weight (Kg)': 'sum'
        }).reset_index()
        
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Bar(
            name='CO2 Emission',
            x=monthly_impact['Month'],
            y=monthly_impact['CO2 Emission'],
            marker_color=SECONDARY_COLOR
        ))
        fig_monthly.add_trace(go.Bar(
            name='Weight',
            x=monthly_impact['Month'],
            y=monthly_impact['Weight (Kg)'],
            marker_color=PRIMARY_COLOR
        ))
        fig_monthly.update_layout(
            title='Monthly Environmental Impact Comparison',
            barmode='group',
            bargap=0.2
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

        # Detailed Impact Analysis
        st.subheader("Waste Stream Impact Analysis")
        
        # Calculate impact metrics by waste stream
        stream_impact = user_df.groupby('Waste Streams').agg({
            'CO2 Emission': 'sum',
            'Weight (Kg)': 'sum'
        }).reset_index()
        
        # Calculate additional metrics
        stream_impact['Carbon_Footprint'] = stream_impact['CO2 Emission'] / 3.67
        stream_impact['Trees_Equivalent'] = stream_impact['CO2 Emission'] * 0.0164
        stream_impact['Diesel_Saved'] = stream_impact['CO2 Emission'] * 0.372
        stream_impact['Energy_Saved'] = stream_impact['CO2 Emission'] * 0.04
        stream_impact['Coal_Avoided'] = stream_impact['CO2 Emission'] * 0.5

        # Impact Distribution (Fixed version)
        stream_impact_filtered = stream_impact[stream_impact['CO2 Emission'] > 0].copy()
        if not stream_impact_filtered.empty:
            fig_stream_impact = px.treemap(
                stream_impact_filtered,
                path=['Waste Streams'],
                values='CO2 Emission',
                color='Trees_Equivalent',
                title='Environmental Impact Distribution by Waste Stream',
                color_continuous_scale='Viridis',
                custom_data=['Carbon_Footprint', 'Trees_Equivalent', 'Diesel_Saved']
            )
            fig_stream_impact.update_traces(
                hovertemplate="""
                Waste Stream: %{label}<br>
                CO2 Emission: %{value:.2f} Kg<br>
                Trees Equivalent: %{customdata[1]:.1f}<br>
                Diesel Saved: %{customdata[2]:.2f} L
                """
            )
            st.plotly_chart(fig_stream_impact, use_container_width=True)

        # Efficiency Analysis
        st.subheader("Waste Stream Efficiency")
        efficiency_df = pd.DataFrame({
            'Waste Stream': stream_impact['Waste Streams'],
            'CO2 per Kg': stream_impact['CO2 Emission'] / stream_impact['Weight (Kg)'],
            'Trees per Tonne': stream_impact['Trees_Equivalent'] / (stream_impact['Weight (Kg)'] / 1000),
            'Energy Saved per Kg': stream_impact['Energy_Saved'] / stream_impact['Weight (Kg)']
        }).fillna(0)
        
        fig_efficiency = px.scatter(
            efficiency_df,
            x='CO2 per Kg',
            y='Trees per Tonne',
            size='Energy Saved per Kg',
            color='Waste Stream',
            title='Waste Stream Efficiency Matrix',
            labels={
                'CO2 per Kg': 'CO2 Emissions Prevented per Kg',
                'Trees per Tonne': 'Trees Equivalent per Tonne'
            }
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)

        # Summary Table
        st.subheader("Detailed Impact Summary")
        summary_df = stream_impact.copy()
        summary_df['CO2_per_Kg'] = summary_df['CO2 Emission'] / summary_df['Weight (Kg)']
        summary_df['Impact_Score'] = (summary_df['CO2_per_Kg'] / summary_df['CO2_per_Kg'].max() * 100)
        
        st.dataframe(
            summary_df.style.format({
                'CO2 Emission': '{:,.2f} Kg',
                'Weight (Kg)': '{:,.2f} Kg',
                'Carbon_Footprint': '{:,.2f} Kg',
                'Trees_Equivalent': '{:,.1f}',
                'Diesel_Saved': '{:,.2f} L',
                'Energy_Saved': '{:,.0f} hrs',
                'Coal_Avoided': '{:,.2f} Kg',
                'CO2_per_Kg': '{:,.3f}',
                'Impact_Score': '{:,.1f}%'
            }),
            hide_index=True
        )

    else:
        st.info("No data available for sustainability reporting.")