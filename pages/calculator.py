import streamlit as st
from config import ACCENT_COLOR_2, SECONDARY_COLOR, PRIMARY_COLOR, EMISSION_FACTORS

def display_calculation_page():
    st.title("Sustainability Impact Calculator")

    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Enter Weight (Kg):", min_value=0.0, format="%.2f")
    with col2:
        waste_stream = st.selectbox("Select Waste Stream", list(EMISSION_FACTORS.keys()))

    if st.button("Calculate Environmental Impact"):
        co2_emission = (weight / 1000) * EMISSION_FACTORS[waste_stream]
        carbon_emission = co2_emission / 3.67
        trees = 0.0164 * co2_emission
        diesel = 0.372 * co2_emission
        lamps = 0.04 * co2_emission
        coal = 0.5 * co2_emission

        st.subheader("Your Environmental Impact")
        col1, col2, col3 = st.columns(3)
        col1.metric("CO2 Emissions Prevented", f"{co2_emission:.2f} Kg")
        col2.metric("Carbon Footprint Reduced", f"{carbon_emission:.2f} Kg")
        col3.metric("Equivalent Trees Planted", f"{trees:.2f}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Diesel Saved", f"{diesel:.2f} Liters")
        col2.metric("Energy Conserved", f"{lamps:.0f} Lamp Hours")
        col3.metric("Coal Consumption Avoided", f"{coal:.2f} Kg")
