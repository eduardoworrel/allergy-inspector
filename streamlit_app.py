import streamlit as st
from ui.sidebar import sidebar_setup
from ui.media_input import media_input
from streamlit_chat import message

st.set_page_config(page_title="Allergy Detector", page_icon="🔍")
st.markdown(
    '''
        <style>
            div[aria-label="dialog"]>button[aria-label="Close"] {
                display: none;
            }
        </style>
    ''',
    unsafe_allow_html=True
)

sidebar_setup()

if st.session_state.get("allergies_selected"):
    # Initial message
    text = f"Hello {st.session_state.get('user_name', 'User')}. What are you about to eat? Is it something you chose... or was it chosen for you? Perhaps there's a pattern, a clue hidden in the ingredients, the flavors, the texture that you don't know. So, hold on buddy. Let us investigate for you."
    message(text, logo="https://i.ibb.co/py1Kdv4/image.png")
   
    # Interactive input for food description
    user_food_input = st.text_input("Tell us what you’re about to eat:")

    # Analyze button to trigger investigation
    if st.button("Analyze"):
        if user_food_input:
            # Placeholder logic for food safety (replace with actual check)
            food_safe = True  # Change this logic based on actual allergy checks

            # Display result with colored text based on safety
            if food_safe:
                result_text = f"Great news! The food '{user_food_input}' is <span style='color:green'>safe</span> for you to eat."
            else:
                result_text = f"Warning! The food '{user_food_input}' is <span style='color:red'>unsafe</span> for you to eat."

            st.markdown(result_text, unsafe_allow_html=True)
            media_input()  # Further processing, if necessary
        else:
            st.warning("Please describe what you are about to eat.")
else:
    # Message for user when allergies are not selected
    st.markdown("# Hey buddy! I am an allergy detective (yeah, that's my name). Let me tell you the food that you are about to eat is <span style='color:green'>safe</span> or <span style='color:red'>unsafe</span> for you!", unsafe_allow_html=True)
    
    if st.button("Start again"):
        st.rerun()
