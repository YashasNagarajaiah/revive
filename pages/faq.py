import streamlit as st

def display_faq_page():
    st.title("Frequently Asked Questions")
    comment = st.text_area("Have a question? Submit it here:")
    if st.button("Submit Question"):
        st.success("Thank you for your question! We'll get back to you soon.")
