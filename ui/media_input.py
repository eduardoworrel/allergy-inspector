from io import BytesIO
import streamlit as st
from streamlit_chat import message
from PIL import Image
from utils.media_handler import image_to_base64
from services.multi_modal import get_crossing_data_model_response, get_ingredients_model_response

# Custom CSS for detective theme
def add_detective_theme():
    st.markdown("""
        <style>
            /* Background and font styles for a detective feel */
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
            /* Style for the ingredient and allergy labels */
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
            /* Detective icon styling */
            .detective-icon {
                content: url('https://example.com/magnifying-glass-icon.png'); /* Replace with actual detective icon URL */
                margin-right: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

def generate_labels(items, label_type="ingredient"):
    labels_html = ""
    css_class = "ingredient-label" if label_type == "ingredient" else "allergy-label"
    for item in items:
        labels_html += f'<span class="{css_class}">{item}</span>'
    return labels_html

def media_input():
    add_detective_theme()  # Apply detective theme

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

                # Display ingredients as text block
                ingredients_text = "".join(response_generator)  # Joining response to create a single block of text
                message(f"<div><strong>🔎 Clues (Ingredients):</strong><br>{ingredients_text}</div>", allow_html=True)

                # Display user allergies
                labels_html = generate_labels(st.session_state["user_allergies"], label_type="allergy")
                message(f'<div>🕵️ Known Allergies: {labels_html}</div>', is_user=True, allow_html=True)

                # Check for cross-reactions
                response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state["user_allergies"]))
                advice = "".join(response_generator)  # Joining response to display without line spaces
                message(advice)

            except Exception as e:
                inner_exception = e.__context__
                message(f"<div>🔍 Something went wrong while analyzing the image.</div>", is_user=True, allow_html=True)

    elif file_type == "Text":
        ingredients_text = st.text_area("Enter or paste the list of ingredients")
        if ingredients_text:
            # Display ingredients in block format with detective theme
            ingredients_list = ingredients_text.split(",")  # Assuming ingredients are comma-separated
            labels_html = generate_labels(ingredients_list)
            message(f'<div><strong>🔎 Clues (Ingredients):</strong><br>{labels_html}</div>', allow_html=True)

            # Display user allergies
            labels_html_allergies = generate_labels(st.session_state["user_allergies"], label_type="allergy")
            message(f'<div>🕵️ Known Allergies: {labels_html_allergies}</div>', is_user=True, allow_html=True)

            # Check for potential cross-reactions
            response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state["user_allergies"]))
            advice = "".join(response_generator)  # Joining response to display without line spaces
            message(advice)

    # Other file types remain the same...

