import streamlit as st
from io import BytesIO
from PIL import Image
from utils.media_handler import image_to_base64
from services.multi_modal import get_crossing_data_model_response, get_ingredients_model_response

# Initialize session state variables if they do not exist
if "user_allergies" not in st.session_state:
    st.session_state["user_allergies"] = []

if "ingredients" not in st.session_state:
    st.session_state["ingredients"] = ""
    
if "explanation" not in st.session_state:
    st.session_state["explanation"] = ""

def generate_labels(allergies):
    labels_html = ""
    colors = ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF"]
    for index, allergy in enumerate(allergies):
        color = colors[index % len(colors)]
        label = f'<span style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 5px; margin-right: 5px;">{allergy}</span>'
        labels_html += label
    return labels_html

def media_input():
    file_type = st.radio("Choose the type of media:", ["Image", "Video", "Text", "Camera"])
    
    if file_type == "Image":
        uploaded_file = st.file_uploader("Upload an image of the food", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            users_image = image_to_base64(uploaded_file.getvalue())
            st.image(users_image, caption="Uploaded Image", use_column_width=True)
            
            try:
                img = Image.open(BytesIO(uploaded_file.getvalue()))
                img = img.resize((80, 80), Image.LANCZOS)

                output = BytesIO()
                img.save(output, format="JPEG", optimize=True, quality=30)
                output.seek(0)
                encoded_image = image_to_base64(output.read())

                # Get ingredients from the model
                ingredients_text = ""
                response_generator = get_ingredients_model_response(encoded_image)
                for response_part in response_generator:
                    ingredients_text += response_part

                # Update session state
                st.session_state["ingredients"] = ingredients_text
                labels_html = generate_labels(st.session_state["user_allergies"])
                st.markdown(f"### Ingredients: {ingredients_text}")
                st.markdown(f"### Known Allergies: {labels_html}", unsafe_allow_html=True)

                # Get explanations based on ingredients and allergies
                response_generator = get_crossing_data_model_response(ingredients_text, ",".join(st.session_state["user_allergies"]))
                explanation = ""
                for response_part in response_generator:
                    explanation += response_part
                
                # Update explanation in session state
                st.session_state["explanation"] = explanation
                st.markdown(f"### Explanation: {explanation.replace('\n', ' ')}")  # Remove line breaks

            except Exception as e:
                st.error(f"An error occurred: {e}")

    elif file_type == "Text":
        ingredients_text = st.text_area("Enter or paste the list of ingredients")
        if ingredients_text:
            st.session_state["ingredients"] = ingredients_text
            labels_html = generate_labels(st.session_state["user_allergies"])
            st.markdown(f"### Ingredients: {ingredients_text}")
            st.markdown(f"### Known Allergies: {labels_html}", unsafe_allow_html=True)
            
            # Simulated response for explanation
            explanation = f"This is a mock explanation for the ingredients: {ingredients_text}"
            st.session_state["explanation"] = explanation
            st.markdown(f"### Explanation: {explanation.replace('\n', ' ')}")  # Remove line breaks

    elif file_type == "Video":
        uploaded_file = st.file_uploader("Upload a video of the food", type=["mp4", "mov"])
        if uploaded_file:
            st.video(uploaded_file)
            ingredients_text = "Example OCR result text for video."  # Simulate OCR result
            st.session_state["ingredients"] = ingredients_text
            st.markdown(f"### Ingredients: {ingredients_text}")

    elif file_type == "Camera":
        img_file_buffer = st.camera_input("Take a picture")
        if img_file_buffer:
            image = Image.open(img_file_buffer)
            st.image(image, caption="Captured Image", use_column_width=True)
            ingredients_text = "Example OCR result text for camera image."  # Simulated OCR result
            st.session_state["ingredients"] = ingredients_text
            st.markdown(f"### Ingredients: {ingredients_text}")

# Call media input function to render the interface
media_input()
