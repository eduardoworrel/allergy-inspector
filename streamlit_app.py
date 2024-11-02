# main.py

import streamlit as st
from ui.sidebar import sidebar_setup
from ui.media_input import media_input
from streamlit_chat import message

st.set_page_config(page_title="Allergy Assistant", page_icon="🤧")

sidebar_setup()

if st.session_state["allergies_selected"]:
    message("Hello, what are you about to eat?")
    media_input()
else:
    st.markdown("# Please select your allergies in the sidebar.")