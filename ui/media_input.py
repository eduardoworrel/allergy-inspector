# Import necessary libraries
import base64
from io import BytesIO
import time
from PIL import Image
import streamlit as st
from streamlit_chat import message
from utils.media_handler import image_to_base64
from utils.html import generate_alert
from services.multi_modal import get_crossing_data_model_response, get_ingredients_model_response

# Constant variables
unknow_user_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Unknown_person.jpg/434px-Unknown_person.jpg"
bot_image = "https://i.ibb.co/py1Kdv4/image.png"

actual_response = ""

# Function to parse ingredient assessment
def parse_ingredient_assessment(assessment):
    try:
        elements = assessment.strip("[]").split(", ")
        return {
            "safety_status": elements[0],
            "emoji": elements[1],
            "ingredient_name": elements[2],
            "description": elements[3]
        }
    except:
        return None

# Function to generate labels
def generate_labels(items, label_type="ingredient"):
    css_class = "ingredient-label" if label_type == "ingredient" else "allergy-label"
    labels_html = ", ".join(f'<span class="{css_class}">{item} </span>' for item in items)
    return labels_html

# Main function for media input
def media_input():
    apply_styling() 
    
    _,_,_,_,col1, col2, col3 = st.columns(7)

    gallery = col1.button("🖼️ Library", type= "primary" if  st.session_state["selected"] == "image" else "secondary")
    camera =  col2.button("🤳 Camera", type= "primary" if  st.session_state["selected"] == "camera" else "secondary")
    video =  col3.button("📹 Video", type= "primary" if  st.session_state["selected"] == "video" else "secondary")

    if gallery or st.session_state["selected"] == "image":
        if(st.session_state["selected"] !=  "image"):
            st.session_state["selected"] = "image"
            st.rerun()
        handle_image_upload()
    if camera or st.session_state["selected"] == "camera":
        if(st.session_state["selected"] !=  "camera"):
            st.session_state["selected"] = "camera"
            st.rerun()
        handle_camera_input()
    if video or st.session_state["selected"] == "video":
        if(st.session_state["selected"] !=  "video"):
            st.session_state["selected"] = "video"
            st.rerun()
        handle_video_upload()

    handle_text_prompt()

# Function to apply custom styling
def apply_styling():
    st.markdown("""
        <style>
            .reportview-container { background-color: #f9f9f9; color: #333333; font-family: Arial, sans-serif; }
            .stTextInput>div>div>input { color: #333333; background-color: #ffffff; }
            .ingredient-label, .allergy-label {
                background-color: #d9d9d9; color: #333333; padding: 5px 8px; border-radius: 3px;
                display: inline-block; margin: 0 4px 4px 0; font-weight: bold;
            }
            .allergy-label { background-color: #ff9999; color: white; }
            .ingredient-container { line-height: 1.5; margin-bottom: 20px; padding: 15px; border: 1px solid #ddd;
                                    border-radius: 5px; background-color: #ffffff; text-align: left; }
            .explanation { font-style: italic; color: #555555; margin-top: 8px; line-height: 1.4; }
        </style>
    """, unsafe_allow_html=True)

# Function to handle image upload
def handle_image_upload():
    uploaded_file = st.file_uploader("Upload an image of the food.", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        process_image(uploaded_file)

# Function to handle video upload
def handle_video_upload():
    uploaded_file = st.file_uploader("Upload a video of the food", type=["mp4", "mov"])
    if uploaded_file:
        st.video(uploaded_file)
        get_model_response("Example OCR result text for video.")  # Placeholder for actual OCR implementation

# Function to handle camera input
def handle_camera_input():
    enable = st.checkbox("Enable camera")
    img_file_buffer = st.camera_input("Take a picture", disabled=not enable)
    if img_file_buffer:
        process_image(img_file_buffer)

# Function to process image for analysis
def process_image(image_file):
    image = Image.open(image_file)
    st.image(image, caption="Captured Image", use_column_width=True)
    
    users_image = image_to_base64(image_file.getvalue())
    with st.spinner("Analyzing the image..."):
        ingredients_text = "".join(get_ingredients_model_response(users_image))
        bot_display_ingredients(ingredients_text)
        check_allergies(ingredients_text)

# Function to handle text prompt
def handle_text_prompt():
    prompt = st.chat_input("food and or known ingredients")
    if prompt:
        ingredients_list = prompt.split(",")
        labels_html = generate_labels(ingredients_list)
        message(f'<div class="ingredient-container"><strong>🔎 Clues (Food or Ingredients):</strong><br>{labels_html}</div>', allow_html=True, is_user=True, logo=unknow_user_image)
        check_allergies(", ".join(ingredients_list))

# Helper function to display ingredients
def bot_display_ingredients(ingredients_text):
     with st.spinner("Analyzing..."):
        time.sleep(0.5)
        message(f"<div class='ingredient-container'><strong>🔎 Clues (Ingredients):</strong><br>{ingredients_text}</div>", allow_html=True, logo=bot_image)

# Helper function to check allergies 
def check_allergies(ingredients_text):
    allergies = st.session_state.get("user_allergies", [])
    labels_html = generate_labels(allergies, label_type="allergy")
    message(f"<div class='ingredient-container'>and I'm also allergic to: <strong>{labels_html}</strong></div>", is_user=True, allow_html=True, logo=unknow_user_image)
    message("I'll keep that in mind!", logo=bot_image)

    if allergies:
        with st.spinner('Checking for allergens...'):
            messages = get_crossing_data_model_response(ingredients_text, ", ".join(allergies))
            alarm = False
            if messages:
                for advice in messages:
                    obj = parse_ingredient_assessment(advice)
                    if obj:
                        if not alarm and obj["safety_status"] == "dangerous":
                            alarm = True
                            with open("./static/alert.mp3", "rb") as f:
                                data = f.read()
                                audio_base64 = base64.b64encode(data).decode('utf-8')
                                audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
                                st.markdown(audio_tag, unsafe_allow_html=True)
                        result = generate_alert(obj["emoji"], obj["ingredient_name"], obj["safety_status"], obj["description"])
                        message(result, logo=bot_image, allow_html=True)
