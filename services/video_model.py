import re
import time
import requests
import streamlit as st
from streamlit_chat import message
from services.multi_modal import get_video_instructions_model_response  # Import the function
bot_image = "https://i.ibb.co/py1Kdv4/image.png"
doctor_image = "https://i.ibb.co/6HMSRys/2.png"

bearer_token = st.secrets["ALLEGRO_API_KEY"]
st.session_state["video_key"] = 1
def generate_videos(allergies):

    allergy_list = []

    with st.spinner('generating symptom descriptions...'):
        prompt = "".join(get_video_instructions_model_response(allergies))
        allergy_list = re.findall(r'\((.*?)\)', prompt)

        url = "https://api.rhymes.ai/v1/generateVideoSyn"
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
    
    for allergy in allergy_list:
        
         
        try:
            print("----start")
            title_and_scenes = allergy.split(':')
            title = title_and_scenes[0].strip()
            print("----title: "+ title)
            scenes_str = ':'.join(title_and_scenes[1:])  
            print("----scenes_str: "+ scenes_str)
            scenes = re.findall(r'\[(.*?)\]', scenes_str)
            scene =scenes[0]
            description =scenes[1]
            print("----scenes: "+ scenes[0])
            print("----description: "+ scenes[1])
            with st.spinner(f'generating video for allergy symptoms to {title} ...'):
                refined_prompt = scene
                data = {
                    "refined_prompt": refined_prompt,
                    "num_step": 90,
                    "cfg_scale": 7.5,
                    "user_prompt": refined_prompt,
                    "rand_seed": 12345
                }
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                response_data = response.json()
                request_id = response_data.get('data')
                
                if not request_id:
                    print(f"Erro: request_id não retornado para a alergia '{title}'.")
                    continue
                
                time.sleep(10)
                
                status_url = "https://api.rhymes.ai/v1/videoQuery"
                params = {"requestId": request_id}
                finish = False
                while not finish:
                    status_response = requests.get(status_url, headers=headers, params=params)
                    status_response.raise_for_status()
                    status_data = status_response.json()
                    
                    if status_data.get('status') != 0:
                        print(status_data)
                        finish = True
                    
                    elif status_data.get('data') == '':
                        time.sleep(5)  
                    else: 
                        video_link = status_data.get('data')
                        print(f"Vídeo finalizado para alergia '{title}'. URL:", video_link)
                        message("Symptoms of " + (title if title.startswith("(") else title) + " : " +description, logo=doctor_image, key=f'mgs_{st.session_state["video_key"]}')
                        st.video(video_link)
                        st.session_state["video_key"] += 1
                        finish = True
                time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro durante a requisição à API para a alergia '{title}': {str(e)}")