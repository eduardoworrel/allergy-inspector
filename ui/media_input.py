from io import BytesIO
import streamlit as st
from streamlit_chat import message
from PIL import Image
from utils.media_handler import image_to_base64
from services.multi_modal import get_crossing_data_model_response, get_ingredients_model_response

# Function to generate ingredient and allergy labels
def generate_labels(items, label_type="ingredient"):
    labels_html = ""
    css_class = "ingredient-label" if label_type == "ingredient" else "allergy-label"
    for item in items:
        labels_html += f'<span class="{css_class}">{item}</span> '  # Add a space after each label
    return labels_html

# Main media input function
def media_input():
    # Set the light mode theme with aesthetics
    st.markdown("""
        <style>
            .reportview-container {
                background-color: #f9f9f9;  /* Light background */
                color: #333333;  /* Dark text color */
                font-family: Arial, sans-serif;
            }
            .stButton>button {
                color: #fff;
                background-color: #007BFF;  /* Button color */
                border-radius: 5px;
                font-weight: bold;
            }
            .stTextInput>div>div>input {
                color: #333333;
                background-color: #ffffff;
            }
            .ingredient-label, .allergy-label {
                background-color: #d9d9d9;  /* Ingredient label color */
                color: #333333;  /* Dark text for labels */
                padding: 5px 8px;
                border-radius: 3px;
                display: inline-block;
                margin: 0 4px 4px 0;
                font-weight: bold;
            }
            .allergy-label {
                background-color: #ff9999;  /* Allergy label color */
                color: white;
            }
            .ingredient-container {
                line-height: 1.5;  /* Adjusted line spacing for readability */
                margin-bottom: 20px;  /* Space between ingredient sections */
                padding: 15px;  /* Padding inside the container */
                border: 1px solid #ddd;  /* Border around the ingredient block */
                border-radius: 5px;  /* Rounded corners */
                background-color: #ffffff;  /* White background for the block */
                text-align: left;  /* Left-align text for consistency */
            }
            .explanation {
                font-style: italic;  /* Italic style for explanation */
                color: #555555;  /* Lighter text for explanation */
                margin-top: 8px;  /* Space above explanation */
                line-height: 1.4;  /* Line spacing for explanation */
            }
        </style>
    """, unsafe_allow_html=True)

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
                message(f"<div class='ingredient-container'><strong>🔎 Clues (Ingredients):</strong><br>{ingredients_text}</div>", allow_html=True)

                labels_html = generate_labels(st.session_state.get("user_allergies", []), label_type="allergy")
                message(f'<div class="ingredient-container">🕵️ Known Allergies: {labels_html}</div>', is_user=True, allow_html=True)

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
            message(f'<div class="ingredient-container"><strong>🔎 Clues (Ingredients):</strong><br>{labels_html}</div>', allow_html=True)

            labels_html_allergies = generate_labels(st.session_state.get("user_allergies", []), label_type="allergy")
            message(f'<div class="ingredient-container">🕵️ Known Allergies: {labels_html_allergies}</div>', is_user=True, allow_html=True)

            # Example explanation (customize this part as needed)
            explanation_text = "These ingredients are commonly found in various dishes. Ensure to check if they trigger any allergies."
            message(f'<div class="explanation">{explanation_text}</div>', allow_html=True)

            response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state.get("user_allergies", [])))
            advice = "".join(response_generator)
            message(advice)

    # Other file types remain the same...
