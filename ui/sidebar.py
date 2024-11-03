# ui/sidebar.py

from io import BytesIO
import streamlit as st
from PIL import Image
from utils.session_state import init_session_state
from utils.media_handler import image_to_base64

# Lista predefinida de categorias de alergias
allergy_options = ["Nuts", "Dairy", "Gluten", "Seafood", "Soy", "Eggs"]

is_editing = False

def sidebar_setup():
    init_session_state()
    st.sidebar.markdown("# Allergy inspector 🕵️‍♀️")
    @st.dialog("Setting up")
    def setup():
        with st.container():
            st.write("Prepare your enviroment")
            # Input para o nome do usuário
            st.session_state["user_name"] = st.text_input(
                "Enter your name (optional):", 
                value=st.session_state.get("user_name", "Guest")
            )
            
            # Input para o avatar do usuário
            avatar = st.file_uploader(
                "Upload your avatar image (optional):", 
                type=["jpg", "jpeg", "png"]
            )
            if avatar :
                avatar = image_to_base64(avatar.getvalue())
                base64avatar = f"data:image/png;base64,{avatar}"
                st.session_state["user_avatar"] = base64avatar
            # Input para a descrição do usuário
            st.session_state["user_description"] = st.text_area(
                "Describe your food allergies naturally (optional):", 
                value=st.session_state.get("user_description", "")
            )
            
            # Seletor de alergias
            user_allergies = st.multiselect(
                "Select your allergies:",
                options=allergy_options,
                default=st.session_state["user_allergies"],
                help="Choose from common allergy categories."
            )
            
            if st.button("Confirm Allergies"):
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
        if st.sidebar.button("✏️ Edit preferences"):
            setup() 
        if st.session_state["user_avatar"] != "":
            st.sidebar.image(st.session_state["user_avatar"],width=120)
        else:
            st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Unknown_person.jpg/434px-Unknown_person.jpg",width=120)
        st.sidebar.markdown("## "+st.session_state["user_name"] or "Guest")
        st.sidebar.markdown("⚠️ :gray["+", ".join(st.session_state.get("user_allergies")) + "]")

