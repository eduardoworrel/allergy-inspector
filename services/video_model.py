import os
import requests

# Common allergy prompts for video generation
allergy_prompts = {
    "pollen": "Person sneezing and having itchy eyes due to pollen allergy",
    "peanut": "Person experiencing a peanut allergy reaction",
    "dust": "Person coughing and sneezing due to dust allergy",
    "cat": "Person with red eyes and sneezing around a cat due to pet allergy",
    "gluten": "Person having a stomach ache from gluten allergy",
    # Add more allergies as needed
}

def get_allergy_prompt(user_input):
    """Return the allergy prompt based on user input if a match is found."""
    for allergy, prompt in allergy_prompts.items():
        if allergy.lower() in user_input.lower():
            return prompt
    return None

# Generate video instructions filename
def generate_video_instructions(instructions):
    return f"video_output_{instructions}.mp4"

# Generate a video using the Allegro API model
def generate_video(token, instructions):
    url = "https://api.rhymes.ai/v1/generateVideoSyn"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "refined_prompt": instructions,
        "num_step": 100,
        "cfg_scale": 7.5,
        "user_prompt": instructions,
        "rand_seed": 12345
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"

# Main function for allergy video generation
def main():
    # Fetch API token from environment
    bearer_token = os.getenv("ALLEGRO_API_KEY")
    if not bearer_token:
        print("API token not found. Set the ALLEGRO_API_KEY environment variable.")
        return

    # Get user input for allergy
    user_input = input("Please describe your allergy or ask about any specific allergy: ")

    # Find the corresponding allergy prompt
    allergy_prompt = get_allergy_prompt(user_input)
    
    if allergy_prompt:
        print(f"Generating video for allergy: {allergy_prompt}")
        
        # Generate video output filename
        video_filename = generate_video_instructions(allergy_prompt)
        
        # Generate video using the Allegro API
        response_data = generate_video(bearer_token, allergy_prompt)
        
        print("Generated video filename:", video_filename)
        print("API response:", response_data)
    else:
        print("No specific allergy detected in input. Please specify a known allergy.")

# Run the main function
if __name__ == "__main__":
    main()
