import streamlit as st

def init_session_state():
    if "allergies_selected" not in st.session_state:
        st.session_state["allergies_selected"] = False
        st.session_state["user_allergies"] = []