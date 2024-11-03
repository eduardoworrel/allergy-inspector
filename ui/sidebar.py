# ui/sidebar.py

import streamlit as st
from utils.session_state import init_session_state
from utils.media_handler import image_to_base64
from services.multi_modal import get_infers_allergy_model_response
 
is_editing = False

def sidebar_setup():
    init_session_state()
    st.sidebar.markdown("# Allergy inspector 🕵️‍♀️")
    
    @st.dialog("Create your account")
    def setup():
        with st.container():
            # Input para o nome do usuário
            st.session_state["user_name"] = st.text_input(
                "Enter your name (optional):", 
                value=st.session_state.get("user_name", "Guest")
            )
            
            # Input para o avatar do usuário
            avatar = st.file_uploader(
                "Upload your picture (optional):", 
                type=["jpg", "jpeg", "png"]
            )
            if avatar:
                avatar = image_to_base64(avatar.getvalue())
                base64avatar = f"data:image/png;base64,{avatar}"
                st.session_state["user_avatar"] = base64avatar
            # Input para a descrição do usuário
            description = st.text_area(
                "Describe your food allergies naturally (optional):", 
                value=st.session_state.get("user_description", "")
            )
            process = st.button("Find out")
            if process and description:
                with st.spinner("processing"):
                    response = "".join(get_infers_allergy_model_response(description))
                    if response != "[noone]":
                        response = response.split(",")
                        for item in response:
                            st.session_state["allergy_options"].append(item)
                            st.session_state["user_allergies"].append(item)
                            st.session_state["allergy_options"] = list(dict.fromkeys(st.session_state["allergy_options"]))
                            st.session_state["user_allergies"] = list(dict.fromkeys(st.session_state["user_allergies"]))
                    else : 
                        st.write("no allergies identified")

            user_allergies = st.multiselect(
                "Select your allergies:", 
                options=st.session_state["allergy_options"],
                default=st.session_state["user_allergies"],
                help="Choose from common allergy categories."
            )
            
            if st.button("Confirm Your Choice"):
                if user_allergies:
                    st.session_state["allergies_selected"] = True
                    st.session_state["user_allergies"] = user_allergies
                    st.rerun()
                else:
                    st.warning("Please select at least one allergy.")
    if not st.session_state["allergies_selected"]:
        
        setup()
    else:
        st.sidebar.markdown("---")
        if st.sidebar.button("Edit preferences"):
            setup() 
        if st.session_state["user_avatar"] != "":
            st.sidebar.image(st.session_state["user_avatar"],width=120)
        else:
            st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Unknown_person.jpg/434px-Unknown_person.jpg",width=120)
        st.sidebar.markdown("## "+st.session_state["user_name"] or "Guest")
        st.sidebar.markdown("⚠️ :gray["+", ".join(st.session_state.get("user_allergies")) + "]")


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
