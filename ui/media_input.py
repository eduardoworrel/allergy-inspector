# ui/media_input.py

import streamlit as st
from PIL import Image
from services.multi_modal import get_model_response
from services.voice_model import synthesize_voice
from services.video_model import generate_video_instructions

def media_input():
    file_type = st.radio("Choose the type of media:", ["Image", "Video", "Text", "Camera"])

    # Função para processar resposta e exibir vídeo final
    def process_and_display_result(response):
        audio_output = synthesize_voice(response)
        video_output = generate_video_instructions(response)
        final_video = merge_audio_video(audio_output, video_output)
        st.video(final_video)

    if file_type == "Image":
        uploaded_file = st.file_uploader("Upload an image of the food", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            ingredients_text = "Example OCR result text for image."  # Exemplo de texto para simulação do OCR
            response = get_model_response(ingredients_text)
            st.write("Instructions and transcription:", response)
            process_and_display_result(response)

    elif file_type == "Video":
        uploaded_file = st.file_uploader("Upload a video of the food", type=["mp4", "mov"])
        if uploaded_file:
            st.video(uploaded_file)
            ingredients_text = "Example OCR result text for video."  # Exemplo de texto para simulação do OCR
            response = get_model_response(ingredients_text)
            st.write("Instructions and transcription:", response)
            process_and_display_result(response)

    elif file_type == "Text":
        ingredients_text = st.text_area("Enter or paste the list of ingredients")
        if ingredients_text:
            response = get_model_response(ingredients_text)
            st.write("Instructions and transcription:", response)
            process_and_display_result(response)

    elif file_type == "Camera":
        enable = st.checkbox("Enable camera")
        img_file_buffer = st.camera_input("Take a picture", disabled=not enable)
        if img_file_buffer:
            image = Image.open(img_file_buffer)
            st.image(image, caption="Captured Image", use_column_width=True)
            ingredients_text = "Example OCR result text for camera image."  # Exemplo de texto para simulação do OCR
            response = get_model_response(ingredients_text)
            st.write("Instructions and transcription:", response)
            process_and_display_result(response)