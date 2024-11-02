import os
import requests
from services.video_model import generate_video_instructions  # Import the function

# Define common allergy symptom prompts
allergy_symptom_prompts = {
    "pollen": "Person sneezing and rubbing eyes due to pollen allergy symptoms",
    "peanut": "Person experiencing skin rash and swelling from peanut allergy",
    "dust": "Person sneezing and coughing from dust allergy symptoms",
    "cat": "Person showing signs of pet allergy with a cat nearby",
    "gluten": "Person with a stomach ache and discomfort from gluten allergy",
    # Add more allergies as necessary
}

def get_allergy_prompt(allergy):
    """Return the prompt for a given allergy if it exists in the dictionary."""
    prompt = allergy_symptom_prompts.get(allergy.lower())
    if prompt:
        print(f"Found prompt for allergy '{allergy}': {prompt}")
    else:
        print(f"No prompt found for allergy '{allergy}'")
    return prompt

# Function to make the API request to generate a video
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
        response.raise_for_status()  # Check for HTTP errors
        print("API request successful.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {str(e)}")
        return None

# Main function to orchestrate the allergy video generation
def main():
    # Fetch API token from environment
    bearer_token = os.getenv("ALLEGRO_API_KEY")
    if not bearer_token:
        print("API token not found. Make sure to set the ALLEGRO_API_KEY environment variable.")
        return

    # Get user input for registered allergies
    user_input = input("Please enter your registered allergies, separated by commas: ").strip()
    if not user_input:
        print("No allergies entered. Please provide at least one allergy.")
        return

    # Split and clean the list of registered allergies
    registered_allergies = [allergy.strip() for allergy in user_input.split(',')]
    print(f"Registered allergies: {registered_allergies}")

    # Process each allergy to generate videos
    for allergy in registered_allergies:
        allergy_prompt = get_allergy_prompt(allergy)
        
        if allergy_prompt:
            print(f"Generating video for '{allergy}' allergy symptoms.")
            
            # Generate video output filename using imported function
            video_filename = generate_video_instructions(allergy)
            
            # Generate video using the Allegro API
            response_data = generate_video(bearer_token, allergy_prompt)
            
            if response_data:
                print(f"Generated video filename: {video_filename}")
                print("API response data:", response_data)
            else:
                print(f"Failed to generate video for allergy '{allergy}'.")
        else:
            print(f"No video generated for '{allergy}' - no matching prompt found.")

# Run the main function
if __name__ == "__main__":
    main()

