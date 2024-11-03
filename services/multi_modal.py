from textwrap import dedent
from openai import OpenAI
import streamlit as st

def parse_items_from_response(response_generator):
    item_buffer = ""
    in_brackets = False
    
    # Para cada pedaço de texto retornado
    for chunk in response_generator:
        content = chunk.choices[0].delta.content
        if content:
            for char in content:
                if char == '[':
                    in_brackets = True
                    item_buffer += char
                elif char == ']' and in_brackets:
                    item_buffer += char
                    in_brackets = False
                    yield item_buffer 
                    item_buffer = ""  
                elif in_brackets:
                    item_buffer += char

base_url = 'https://api.rhymes.ai/v1'

client = OpenAI(
    base_url=base_url,
    api_key=st.secrets["OPENAI_API_KEY"]
)

def load_prompt(filepath):
    with open(filepath, 'r') as file:
        return file.read().strip()

def get_ingredients_model_response(content):

    prompt_text = load_prompt('prompts/ingredients_prompt.txt')

    response = client.chat.completions.create(
        model="aria",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{content}"}},
                    {"type": "text", "text": prompt_text}
                ]
            }
        ],
        stream=True,
        temperature=0.1,
        max_tokens=1024,
        top_p=1,
        stop=["<|im_end|>"]
    )
    yield "We identify:\n"
    for chunk in response:
        if chunk.choices[0].delta.content is not None: 
            yield chunk.choices[0].delta.content

def get_crossing_data_model_response(ingredients_text, allergies_text):
 
    prompt_text = load_prompt('prompts/crossing_prompt.txt')
    prompt_text = prompt_text.format(ingredients_text, allergies_text)
    response = client.chat.completions.create(
        model="aria",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text}
                ]
            }
        ],
        stream=True,
        temperature=0.1,
        max_tokens=1024,
        top_p=1,
        stop=["<|im_end|>"]
    )
    return parse_items_from_response(response)

def get_infers_allergy_model_response(description):

    prompt_text = load_prompt('prompts/infers_allergy_prompt.txt')
    prompt_text = prompt_text.format(description)
    response = client.chat.completions.create(
        model="aria",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text}
                ]
            }
        ],
        stream=True,
        temperature=0.1,
        max_tokens=1024,
        top_p=1,
        stop=["<|im_end|>"]
    )
    for chunk in response:
        if chunk.choices[0].delta.content is not None: 
            yield chunk.choices[0].delta.content
