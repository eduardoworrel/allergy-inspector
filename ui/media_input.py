def handle_camera_input():
    selected = "camera"
    enable = st.checkbox("Enable camera")
    img_file_buffer = st.camera_input("Take a picture", disabled=not enable)
    
    if img_file_buffer:
        # Convert the captured image to base64
        image = Image.open(img_file_buffer)
        st.image(image, caption="Captured Image", use_column_width=True)
        
        # Convert the image to base64 format
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Now pass the base64 image to the model
        with st.spinner("Analyzing the captured image..."):
            try:
                ingredients_text = "".join(get_ingredients_model_response(encoded_image))
                bot_display_ingredients(ingredients_text)
                check_allergies(ingredients_text)
            except Exception as e:
                message("🔍 Something went wrong while analyzing the image.", is_user=True, allow_html=True)
