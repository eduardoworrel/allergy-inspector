from io import BytesIO
import streamlit as st
from streamlit_chat import message
from PIL import Image
from utils.media_handler import image_to_base64
from services.multi_modal import get_crossing_data_model_response, get_ingredients_model_response

# Generate ingredient and allergy labels
def generate_labels(items, label_type="ingredient"):
    labels_html = ""
    css_class = "ingredient-label" if label_type == "ingredient" else "allergy-label"
    for item in items:
        labels_html += f'<span class="{css_class}">{item.strip()}</span>'
    return labels_html

# Main media input function
def media_input():
    st.markdown("<h2 style='text-align: center;'>🕵️‍♂️ Ingredient Detective</h2>", unsafe_allow_html=True)
    
    file_type = st.radio("Choose the type of media:", ["Image", "Video", "Text", "Camera"])

    if file_type == "Image":
        uploaded_file = st.file_uploader("Upload an image of the food", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            users_image = image_to_base64(uploaded_file.getvalue())
            message(f'<img width="100%" src="data:image/png;base64,{users_image}"/>', is_user=True, allow_html=True)
            message("🕵️ Analyzing the evidence...")

            try:
                img = Image.open(BytesIO(uploaded_file.getvalue()))
                output = BytesIO()
                img.save(output, format="JPEG", optimize=True, quality=30)
                output.seek(0)
                
                encoded_image = image_to_base64(output.read())
                response_generator = get_ingredients_model_response(encoded_image)

                ingredients_text = "".join(response_generator)
                labels_html = generate_labels(ingredients_text.split(","))
                message(f"<div style='margin-bottom: 10px;'><strong>🔎 Clues (Ingredients):</strong><br>{labels_html}</div>", allow_html=True)

                labels_html_allergies = generate_labels(st.session_state.get("user_allergies", []), label_type="allergy")
                message(f'<div style="margin-bottom: 10px;">🕵️ Known Allergies: {labels_html_allergies}</div>', is_user=True, allow_html=True)

                response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state.get("user_allergies", [])))
                advice = "".join(response_generator)
                message(advice)

            except Exception as e:
                message("🔍 Something went wrong while analyzing the image.", is_user=True, allow_html=True)

    elif file_type == "Text":
        ingredients_text = st.text_area("Enter or paste the list of ingredients", height=150)
        if ingredients_text:
            ingredients_list = ingredients_text.split(",")
            labels_html = generate_labels(ingredients_list)
            message(f'<div style="margin-bottom: 10px;"><strong>🔎 Clues (Ingredients):</strong><br>{labels_html}</div>', allow_html=True)

            labels_html_allergies = generate_labels(st.session_state.get("user_allergies", []), label_type="allergy")
            message(f'<div style="margin-bottom: 10px;">🕵️ Known Allergies: {labels_html_allergies}</div>', is_user=True, allow_html=True)

            response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state.get("user_allergies", [])))
            advice = "".join(response_generator)
            message(advice)

    elif file_type == "Video":
        uploaded_file = st.file_uploader("Upload a video of the food", type=["mp4", "mov"])
        if uploaded_file:
            st.video(uploaded_file)
            ingredients_text = "Example OCR result text for video."  # Example OCR result text for simulation
            get_model_response(ingredients_text)

    elif file_type == "Camera":
        enable = st.checkbox("Enable camera")
        img_file_buffer = st.camera_input("Take a picture", disabled=not enable)
        if img_file_buffer:
            image = Image.open(img_file_buffer)
            st.image(image, caption="Captured Image", use_column_width=True)
            ingredients_text = "Example OCR result text for camera image."  # Example OCR result text for simulation
            get_model_response(ingredients_text)
