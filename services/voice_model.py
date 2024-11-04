from playsound import playsound

def synthesize_voice(text, is_dangerous=False):
    # Placeholder for voice synthesis model integration
    audio_output = f"voice_output_{text}.wav"  # Example filename for synthesized audio
    # Your voice synthesis model integration goes here

    # If food is dangerous, play an alarm sound
    if is_dangerous:
        alarm_sound = "alarm_sound.mp3"  # Path to your alarm sound file
        playsound(alarm_sound)  # Play the alarm sound
    
    return audio_output
