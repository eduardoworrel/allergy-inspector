from io import BytesIO
import streamlit as st
from streamlit_chat import message
from PIL import Image
from utils.media_handler import image_to_base64
from services.multi_modal import get_crossing_data_model_response, get_ingredients_model_response

# Function to apply the detective theme
def add_theme(dark_mode):
    if dark_mode:
        # Dark (Detective) Theme CSS
        st.markdown("""
            <style>
                .reportview-container {
                    background-color: #2b2b2b;
                    color: #d1c7b7;
                    font-family: 'Courier New', Courier, monospace;
                }
                .stButton>button {
                    color: #ffffff;
                    background-color: #6c757d;
                    border-radius: 5px;
                    font-weight: bold;
                }
                .stTextInput>div>div>input {
                    color: #d1c7b7;
                    background-color: #3b3b3b;
                }
                .ingredient-label, .allergy-label {
                    background-color: #3b3b3b;
                    color: #ffcc00;
                    padding: 5px 8px;
                    border-radius: 3px;
                    display: inline-block;
                    margin: 0 4px 4px 0;
                    font-weight: bold;
                }
                .allergy-label {
                    background-color: #ff4d4d;
                    color: white;
                }
                /* Reduce line spacing and margin */
                .message-content, .ingredient-label, .allergy-label {
                    line-height: 1.2;
                    margin: 0;
                    padding: 0;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Light Mode CSS
        st.markdown("""
            <style>
                .reportview-container {
                    background-color: #f0f0f5;
                    color: #333333;
                    font-family: Arial, sans-serif;
                }
                .stButton>button {
                    color: #333333;
                    background-color: #e7e7e7;
                    border-radius: 5px;
                    font-weight: bold;
                }
                .stTextInput>div>div>input {
                    color: #333333;
                    background-color: #ffffff;
                }
                .ingredient-label, .allergy-label {
                    background-color: #d9d9d9;
                    color: #333333;
                    padding: 5px 8px;
                    border-radius: 3px;
                    display: inline-block;
                    margin: 0 4px 4px 0;
                    font-weight: bold;
                }
                .allergy-label {
                    background-color: #ff9999;
                    color: white;
                }
                /* Reduce line spacing and margin */
                .message-content, .ingredient-label, .allergy-label {
                    line-height: 1.2;
                    margin: 0;
                    padding: 0;
                }
            </style>
        """, unsafe_allow_html=True)

# Generate ingredient and allergy labels
def generate_labels(items, label_type="ingredient"):
    labels_html = ""
    css_class = "ingredient-label" if label_type == "ingredient" else "allergy-label"
    for item in items:
        labels_html += f'<span class="{css_class}">{item}</span>'
    return labels_html

# Main media input function
def media_input():
    # Light/Dark mode toggle
    st.sidebar.markdown("### Theme")
    dark_mode = st.sidebar.checkbox("Enable Detective (Dark) Mode", value=True)
    
    # Apply the chosen theme
    add_theme(dark_mode)

    file_type = st.radio("Choose the type of media:", ["Image", "Video", "Text", "Camera"])

    if file_type == "Image":
        uploaded_file = st.file_uploader("Upload an image of the food", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            users_image = image_to_base64(uploaded_file.getvalue())
            message(f'<img width="100%" src="data:image/png;base64,{users_image}"/>', is_user=True, allow_html=True)
            message("🕵️ Analyzing the evidence...")

            try:
                img = Image.open(BytesIO(uploaded_file.getvalue()))
                image = img.resize((80, 80), Image.LANCZOS)
                output = BytesIO()
                image.save(output, format="JPEG", optimize=True, quality=30)
                output.seek(0)
                
                encoded_image = image_to_base64(output.read())
                response_generator = get_ingredients_model_response(encoded_image)

                ingredients_text = "".join(response_generator)
                message(f"<div><strong>🔎 Clues (Ingredients):</strong><br>{ingredients_text}</div>", allow_html=True)

                labels_html = generate_labels(st.session_state.get("user_allergies", []), label_type="allergy")
                message(f'<div>🕵️ Known Allergies: {labels_html}</div>', is_user=True, allow_html=True)

                response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state.get("user_allergies", [])))
                advice = "".join(response_generator)
                message(advice)

            except Exception as e:
                message("🔍 Something went wrong while analyzing the image.", is_user=True, allow_html=True)

    elif file_type == "Text":
        ingredients_text = st.text_area("Enter or paste the list of ingredients")
        if ingredients_text:
            ingredients_list = ingredients_text.split(",")
            labels_html = generate_labels(ingredients_list)
            message(f'<div><strong>🔎 Clues (Ingredients):</strong><br>{labels_html}</div>', allow_html=True)

            labels_html_allergies = generate_labels(st.session_state.get("user_allergies", []), label_type="allergy")
            message(f'<div>🕵️ Known Allergies: {labels_html_allergies}</div>', is_user=True, allow_html=True)

            response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state.get("user_allergies", [])))
            advice = "".join(response_generator)
            message(advice)

    # Other file types remain the same...
