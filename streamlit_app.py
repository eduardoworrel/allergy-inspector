# main.py

import streamlit as st
from ui.sidebar import sidebar_setup
from ui.media_input import media_input
from streamlit_chat import message

st.set_page_config(page_title= "Your Allergy Detector", page_icon="🔍")

sidebar_setup()

if st.session_state["allergies_selected"]:
    message("Hello there. What are you about to eat? Is it something you chose... or was it chosen for you? Perhaps there's a pattern, a clue hidden in the ingredients, the flavors, the texture that you don't know. So, hold on buddy. Let us investigate for you.")
    media_input()
else:
    st.markdown("# Well, well... what’s on the menu? Just the usual, or something... intriguing?🍽️")
