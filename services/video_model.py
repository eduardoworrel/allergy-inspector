import time
import requests
import streamlit as st
from services.multi_modal import get_video_instructions_model_response  # Import the function

bearer_token = st.secrets["ALLEGRO_API_KEY"]

def generate_videos(allergies):

    prompt = "".join(get_video_instructions_model_response(allergies))
    allergy_scenes = prompt.split("},")
    
    url = "https://api.rhymes.ai/v1/generateVideoSyn"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    
    for scene in allergy_scenes:
        scene = scene.strip("()") + ")" if "()" not in scene else scene
        allergy_type, symptoms = scene.split(":", 1)
        allergy_type = allergy_type.strip()
        refined_prompt = symptoms.strip()
        yield refined_prompt
        data = {
            "refined_prompt": refined_prompt,
            "num_step": 5,
            "cfg_scale": 7.5,
            "user_prompt": refined_prompt,
            "rand_seed": 42
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            st.json(response_data)
            request_id = response_data.get('data')
            
            if not request_id:
                print(f"Erro: request_id não retornado para a alergia '{allergy_type}'.")
                continue
            
            print(f"Vídeo iniciado para alergia '{allergy_type}' com request_id: {request_id}. Aguardando processamento...")
            
            time.sleep(120)
            
            
            status_url = "https://api.rhymes.ai/v1/videoQuery"
            params = {"requestId": request_id}
             
            while True:
                status_response = requests.get(status_url, headers=headers, params=params)
                status_response.raise_for_status()
                status_data = status_response.json()
                 
                if status_data.get('status') == 'completed':
                    video_link = status_data.get('data')
                    print(f"Vídeo finalizado para alergia '{allergy_type}'. URL:", video_link)
                    yield (allergy_type, video_link) 
                    break
                elif status_data.get('status') == 'processing':
                    print(f"Processando alergia '{allergy_type}'... Aguardando mais um tempo.")
                    time.sleep(60)  
                else:
                    print(f"Erro no processamento do vídeo para a alergia '{allergy_type}'.")
                    break

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro durante a requisição à API para a alergia '{allergy_type}': {str(e)}")