import streamlit as st
from ui.sidebar import sidebar_setup
from ui.media_input import media_input
from streamlit_chat import message

st.set_page_config(page_title= "Allergy Detector", page_icon="🔍")
st.html(
    '''
        <style>
            div[aria-label="dialog"]>button[aria-label="Close"] {
                display: none;
            }
        </style>
    '''
)

sidebar_setup()

if st.session_state["allergies_selected"]:
    text = f"Hello {st.session_state['user_name']}. What are you about to eat? Is it something you chose... or was it chosen for you? Perhaps there's a pattern, a clue hidden in the ingredients, the flavors, the texture that you don't know. So, hold on buddy. Let us investigate for you.";
    message(text, logo="https://i.ibb.co/py1Kdv4/image.png")
   
    media_input()
else:
    st.markdown("# Please select your allergies.")
    if st.button("Start again"):
        st.rerun()

