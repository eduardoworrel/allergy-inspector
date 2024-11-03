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
st.sidebar.markdown("We are one of the famous allergy detectors that keep people from getting sick.")

# New section for reasons to choose the service
st.sidebar.markdown("## Why you should choose us?")

# Adding the bullet points without extra space
st.sidebar.markdown("✅ We don't ask you for any fee. You can use us freely anytime!")
st.sidebar.markdown("✅ We are really accurate!*")
st.sidebar.markdown("✅ We are fun to interact with!")  # This line now has no additional spacing below it

# Directly adding the fun fact section with reduced space
st.sidebar.markdown("## Fun fact*")  # Same font size as previous headings

# Adding radio buttons for user options with an exclamation mark emoji
option = st.sidebar.radio("Do you want to know why we are so accurate?", 
                            ("Select an option ❗", "Yes, tell me!", "No, I don't want to know this!"))

# Display the additional information only if the user clicks "Yes, tell me!"
if option == "Yes, tell me!":
    st.sidebar.markdown("Well, we use the powerful Aria model 💪.")
    st.sidebar.markdown("The Aria model helps us analyze ingredients efficiently, providing you with accurate allergy information in real-time!")
elif option == "No, I don't want to know this!":
    st.sidebar.markdown("No issues, your loss :)")
if st.session_state["allergies_selected"]:
    text = (
        f"Hello {st.session_state['user_name']}. What are you about to eat? "
        "Is it something you chose... or was it chosen for you? Perhaps there's a "
        "pattern, a clue hidden in the ingredients, the flavors, the texture that you "
        "don't know. So, hold on buddy. Let us investigate for you."
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
