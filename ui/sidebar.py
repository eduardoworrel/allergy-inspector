# ui/sidebar.py

import streamlit as st
from utils.session_state import init_session_state

# Lista predefinida de categorias de alergias
allergy_options = ["Nuts", "Dairy", "Gluten", "Seafood", "Soy", "Eggs"]

def sidebar_setup():
    init_session_state()
    
    st.sidebar.markdown("# Allergy Detector 🤧")
    user_allergies = st.sidebar.multiselect(
        "Select your allergies:",
        options=allergy_options,
        help="Choose from common allergy categories."
    )
    if st.sidebar.button("Confirm Allergies"):
        if user_allergies:
            st.session_state["allergies_selected"] = True
            st.session_state["user_allergies"] = user_allergies
            st.sidebar.success("Allergies recorded.")
        else:
            st.sidebar.warning("Please select at least one allergy.")
