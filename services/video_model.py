import os
import requests

# Predefined allergy symptoms to use for video generation
allergy_symptom_prompts = {
    "pollen": "Person sneezing and rubbing eyes due to pollen allergy symptoms",
    "peanut": "Person experiencing skin rash and swelling from peanut allergy",
    "dust": "Person sneezing and coughing from dust allergy symptoms",
    "cat": "Person showing signs of pet allergy with a cat nearby",
    "gluten": "Person with a stomach ache and discomfort from gluten allergy",
    # Add more allergies as necessary
}

def get_allergy_prompt(allergy):
    """Return the prompt for a given registered allergy."""
    return allergy_symptom_prompts.get(allergy.lower())

# Generate video filename
def generate_video_instructions(allergy):
    return f"video_output_{allergy}_symptoms.mp4"

# Generate video using the Allegro API model
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

# Main function for generating allergy symptom videos
def main():
    # Fetch API token from environment
    bearer_token = os.getenv("ALLEGRO_API_KEY")
    if not bearer_token:
        print("API token not found. Set the ALLEGRO_API_KEY environment variable.")
        return

    # Registered allergies for the user
    registered_allergies = input("Please enter your registered allergies, separated by commas: ").split(',')

    for allergy in registered_allergies:
        allergy = allergy.strip()  # Remove whitespace
        allergy_prompt = get_allergy_prompt(allergy)
        
        if allergy_prompt:
            print(f"Generating video for {allergy} allergy symptoms.")
            
            # Generate video output filename
            video_filename = generate_video_instructions(allergy)
            
            # Generate video using the Allegro API
            response_data = generate_video(bearer_token, allergy_prompt)
            
            print(f"Generated video filename: {video_filename}")
            print("API response:", response_data)
        else:
            print(f"No prompt found for allergy: {allergy}")

# Run the main function
if __name__ == "__main__":
    main()
