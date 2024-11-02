import streamlit as st
from ui.sidebar import sidebar_setup
from ui.media_input import media_input
from streamlit_chat import message

st.set_page_config(page_title="Allergy Detector", page_icon="🔍")

sidebar_setup()

if st.session_state["allergies_selected"]:
    st.markdown(
        "<h2 style='text-align: center; color: #FF5733; font-weight: bold; font-family: monospace;'>"
        "What’s on Your Plate? A Curious Investigation!</h2>",
        unsafe_allow_html=True
    )
    media_input()
else:
    st.markdown("# Well, well... what’s on the menu? Just the usual, or something... intriguing? 🍽️")
