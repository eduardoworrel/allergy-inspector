from io import BytesIO

import streamlit as st
from streamlit_chat import message
from PIL import Image
from utils.media_handler import image_to_base64
from services.multi_modal import get_crossing_data_model_response, get_ingredients_model_response

def generate_labels(items):
    labels_html = ""
    colors = ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF"]  # Colors for the labels
    for index, item in enumerate(items):
        color = colors[index % len(colors)]  # Cycle through colors
        label = f'<span style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 5px; margin-right: 5px;">{item}</span>'
        labels_html += label
    return labels_html

def media_input():
    file_type = st.radio("Choose the type of media:", ["Image", "Video", "Text", "Camera"])
    if file_type == "Image":
        uploaded_file = st.file_uploader("Upload an image of the food", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            users_image = image_to_base64(uploaded_file.getvalue())
            message(f'<img width="100%" src="data:image/png;base64,{users_image}"/>', is_user=True, allow_html=True)

            image = Image.open(uploaded_file)
            message("working on that...")
            try:
                img = Image.open(BytesIO(uploaded_file.getvalue()))
                image = img.resize((80, 80), Image.LANCZOS)

                output = BytesIO()
                image.save(output, format="JPEG", optimize=True, quality=30)

                output.seek(0)
                encoded_image = image_to_base64(output.read())
                response_generator = get_ingredients_model_response(encoded_image)
                
                ingredients_text = ""
                for response_part in response_generator:
                    ingredients_text += response_part
                message(ingredients_text)

                # Display allergies
                labels_html = generate_labels(st.session_state["user_allergies"])
                message(f'<div>My allergies: {labels_html}</div>', is_user=True, allow_html=True)

                # Display ingredient warnings based on allergies
                response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state["user_allergies"]))
                adivices = ""
                for response_part in response_generator:
                    adivices += response_part
                message(adivices)

            except Exception as e:
                inner_exception = e.__context__
                print(f"Outer exception: {e}")
                print(f"Inner exception: {inner_exception}")

    elif file_type == "Video":
        uploaded_file = st.file_uploader("Upload a video of the food", type=["mp4", "mov"])
        if uploaded_file:
            st.video(uploaded_file)
            ingredients_text = "Example OCR result text for video."  # Example OCR result text for video simulation
            get_model_response(ingredients_text)

    elif file_type == "Text":
        ingredients_text = st.text_area("Enter or paste the list of ingredients")
        if ingredients_text:
            # Display ingredients as labels
            ingredients_list = ingredients_text.split(",")  # Assuming ingredients are comma-separated
            labels_html = generate_labels(ingredients_list)
            message(f'<div>Ingredients: {labels_html}</div>', is_user=True, allow_html=True)

            # Display allergies
            labels_html_allergies = generate_labels(st.session_state["user_allergies"])
            message(f'<div>My allergies: {labels_html_allergies}</div>', is_user=True, allow_html=True)

            # Check for potential cross-reactions
            response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state["user_allergies"]))
            adivices = ""
            for response_part in response_generator:
                adivices += response_part
            message(adivices)

    elif file_type == "Camera":
        enable = st.checkbox("Enable camera")
        img_file_buffer = st.camera_input("Take a picture", disabled=not enable)
        if img_file_buffer:
            image = Image.open(img_file_buffer)
            st.image(image, caption="Captured Image", use_column_width=True)
            ingredients_text = "Example OCR result text for camera image."  # Example OCR result text for camera image simulation
            get_model_response(ingredients_text)
