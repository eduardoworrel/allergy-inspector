from io import BytesIO
import streamlit as st
from streamlit_chat import message
from PIL import Image
from utils.media_handler import image_to_base64
from services.multi_modal import get_crossing_data_model_response, get_ingredients_model_response

# Emoji constants
SAFE_EMOJI = "✅"  # Safe emoji
DANGER_EMOJI = "⚠️"  # Danger emoji

# Generate ingredient and allergy labels
def generate_labels(items, label_type="ingredient"):
    labels_html = ""
    css_class = "ingredient-label" if label_type == "ingredient" else "allergy-label"
    for item in items:
        labels_html += f'<span class="{css_class}">{item}</span>'
    return labels_html

# Check for known allergies in ingredients
def check_allergies(ingredients, known_allergies):
    dangerous_items = [ingredient for ingredient in ingredients if ingredient in known_allergies]
    if dangerous_items:
        return DANGER_EMOJI + " Potential allergens detected: " + ", ".join(dangerous_items)
    return SAFE_EMOJI + " No allergens detected."

# Main media input function
def media_input():
    # Apply a single light theme
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
                padding: 5px 10px;
                border-radius: 5px;
                margin: 0 4px 4px 0;
                font-weight: bold;
            }
            .allergy-label {
                background-color: #ff9999;
                color: white;
            }
            .ingredients-block, .allergy-block {
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    file_type = st.radio("Choose the type of media:", ["Image", "Video", "Text", "Camera"])

    if file_type == "Image":
        uploaded_file = st.file_uploader("Upload an image of the food", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            users_image = image_to_base64(uploaded_file.getvalue())
            message(f'<img width="100%" src="data:image/png;base64,{users_image}"/>', is_user=True, allow_html=True)
            message("Analyzing the evidence...")

            try:
                img = Image.open(BytesIO(uploaded_file.getvalue()))
                image = img.resize((80, 80), Image.LANCZOS)
                output = BytesIO()
                image.save(output, format="JPEG", optimize=True, quality=30)
                output.seek(0)

                encoded_image = image_to_base64(output.read())
                response_generator = get_ingredients_model_response(encoded_image)

                ingredients_text = "".join(response_generator).split(",")  # Assuming ingredients are comma-separated
                message(f"<div class='ingredients-block'><strong>Clues (Ingredients):</strong><br>{generate_labels(ingredients_text)}</div>", allow_html=True)

                # Check for allergies
                known_allergies = st.session_state.get("user_allergies", [])
                allergy_message = check_allergies(ingredients_text, known_allergies)
                message(allergy_message, is_user=True)

                response_generator = get_crossing_data_model_response(ingredients_text, ",".join(known_allergies))
                advice = "".join(response_generator)
                message(advice)

            except Exception as e:
                message("Something went wrong while analyzing the image.", is_user=True, allow_html=True)

    elif file_type == "Text":
        ingredients_text = st.text_area("Enter or paste the list of ingredients")
        if ingredients_text:
            ingredients_list = [ingredient.strip() for ingredient in ingredients_text.split(",")]
            labels_html = generate_labels(ingredients_list)
            message(f'<div class="ingredients-block"><strong>Clues (Ingredients):</strong><br>{labels_html}</div>', allow_html=True)

            # Check for allergies
            known_allergies = st.session_state.get("user_allergies", [])
            allergy_message = check_allergies(ingredients_list, known_allergies)
            message(allergy_message, is_user=True)

            response_generator = get_crossing_data_model_response(ingredients_text, ",".join(known_allergies))
            advice = "".join(response_generator)
            message(advice)

    # Other file types remain the same...

# Call the main function
if __name__ == "__main__":
    media_input()
