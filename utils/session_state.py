import streamlit as st

def init_session_state():
    if "allergies_selected" not in st.session_state:
        st.session_state["allergies_selected"] = False
        st.session_state["user_allergies"] = []
        st.session_state["user_name"] = ""
        st.session_state["user_avatar"] = ""
        st.session_state["user_description"] = ""
        st.session_state["uploaded_file"] = None
        st.session_state["active"] = False
        st.session_state["selected"] = ""
        