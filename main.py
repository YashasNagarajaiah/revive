import streamlit as st
from config import *
from styles import load_css
from auth import user_login
from pages.overview import display_overview
from pages.sustainability import display_sustainability_report
from pages.analytics import display_analytics_page
from pages.calculator import display_calculation_page
from pages.overdue import display_overdue_page
from pages.downloads import display_downloads_page
from pages.faq import display_faq_page
from pages.live_stream import display_live_stream
from pages.chatbot import display_chatbot_page  # Import the chatbot page
from utils import load_data

def main():
    st.set_page_config(page_title="Revive Platform", page_icon="Ehfaaz", layout="wide", initial_sidebar_state="collapsed")
    
    # Load and display logo
    logo_path = "Images\Ehfaaz Logo.jpeg"  # Adjust the path if necessary
    st.image(logo_path, width=200)  # Display the logo
    st.markdown("<h1 style='text-align: center;'>Revive - Give your used resources a new life</h1>", unsafe_allow_html=True)

    st.markdown(load_css(), unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    try:
        df_outgoing, credentials = load_data()

        if not st.session_state['logged_in']:
            user_login()
        else:
            tab_overview, tab_sustain, tab_calc, tab_process, tab_analytics, tab_faq, tab_downloads, tab_invoices, tab_chatbot = st.tabs([
                "Overview", "Sustainability", "Calculator", "Process Monitoring",
                "Analytics", "FAQ", "Downloads", "Invoices", "Chatbot"  # Added Chatbot tab
            ])

            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state.pop('username', None)
                st.rerun()

            with tab_overview:
                display_overview(st.session_state['username'])
            with tab_sustain:
                display_sustainability_report(st.session_state['username'])
            with tab_calc:
                display_calculation_page()
            with tab_process:
                display_live_stream()
            with tab_analytics:
                display_analytics_page(st.session_state['username'])
            with tab_faq:
                display_faq_page()
            with tab_downloads:
                display_downloads_page(st.session_state['username'])
            with tab_invoices:
                display_overdue_page(st.session_state['username'])
            with tab_chatbot:  # Display the chatbot page
                display_chatbot_page()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.clear()

if __name__ == "__main__":
    main()
