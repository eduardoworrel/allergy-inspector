# services/openai_integration.py
# split smage
# undestond pdf
import openai

def get_model_response(input_text):
    # Replace with your OpenAI API call for the LLM model
    response = openai.Completion.create(
        engine="your_openai_model",
        prompt=f"Analyze the input for allergy risks and prepare instructions: {input_text}",
        max_tokens=150
    )
    return response["choices"][0]["text"]