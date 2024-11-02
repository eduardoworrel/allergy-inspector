import base64
from textwrap import dedent
from openai import OpenAI

# Configuração da API
base_url = 'https://api.rhymes.ai/v1'
api_key = ''

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

# Função para carregar o prompt a partir de um arquivo .txt
def load_prompt(filepath):
    with open(filepath, 'r') as file:
        return file.read().strip()

# Função para montar o payload com base no tipo de entrada
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
    print (prompt_text)
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
    yield "We identify:\n"
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content