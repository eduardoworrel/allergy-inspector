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
    text = f"Hello {st.session_state['user_name']}. I'm your allergy detective! What are you about to eat? Is it a meal you chose... or was it mysteriously chosen for you? Let's uncover the clues hidden in the ingredients, flavors, and textures. Stay sharp, my friend! Together, we will determine if it's safe or unsafe for you!"
    message(text, logo="https://i.ibb.co/py1Kdv4/image.png")

    # The input and button for food description have been removed
else:
    st.markdown("# I am an allergy detective. Ask me whether the food is <span style='color:green'>safe</span> or <span style='color:red'>unsafe</span> for you!", unsafe_allow_html=True)

    if st.button("Let us analyze the evidence for you"):
        st.rerun()
