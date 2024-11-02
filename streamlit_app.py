import streamlit as st
from ui.sidebar import sidebar_setup
from ui.media_input import media_input
from streamlit_chat import message

st.set_page_config(page_title="Allergy Detector", page_icon="🔍")

sidebar_setup()

if st.session_state["allergies_selected"]:
    # Display the styled detective-themed message using the streamlit_chat message function
    message(
        "<h3 style='color: #333333; font-family: monospace;'>What’s on Your Plate? A Curious Investigation!</h3>",
        unsafe_allow_html=True
    )
    media_input()
else:
    st.markdown("# Well, well... what’s on the menu? Just the usual, or something... intriguing? 🍽️")
