import streamlit as st
from ui.sidebar import sidebar_setup
from ui.media_input import media_input
from streamlit_chat import message

st.set_page_config(page_title="Allergy Detector", page_icon="🔍")
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
    text = (
        f"Hello!{st.session_state['user_name']} What are you about to eat? "
        "Let us investigate for you. "
    )
    message(text, logo="https://i.ibb.co/py1Kdv4/image.png")
   
    media_input()
else:
    st.markdown(
        "<h2 style='font-weight: bold;'>I am an allergy detective. Ask me whether the food is "
        "<span style='color: green;'>safe</span> or "
        "<span style='color: red;'>unsafe</span> for you!</h2>",
        unsafe_allow_html=True
    )

    if st.button("Let us analyze for you"):
        st.rerun()
