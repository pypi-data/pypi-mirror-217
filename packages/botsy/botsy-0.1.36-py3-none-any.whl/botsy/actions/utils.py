import tempfile
from time import time

import openai
import pkg_resources
import speech_recognition as sr
from jprint import jprint

beep_prompt = None


def audio_data_to_wave(data, filename):
    if not filename.endswith(".wav"):
        raise ValueError("filename must be a *.wav file.")

    with open(filename, "wb") as f:
        f.write(data.get_wav_data())


def listen_to_mic(
    non_speaking_duration=0.75,
    pause_threshold=1.5,
    phrase_time_limit=20,
    recognize="whisper",
    initial=False,
):
    from botsy.actions.converse import ConverseAction

    global beep_prompt
    if not beep_prompt:
        beep_prompt = pkg_resources.resource_filename("botsy", "sounds/beep_prompt.wav")

    import pygame  # noqa - here for faster loads on single_show converse actions

    r = sr.Recognizer()
    r.non_speaking_duration = non_speaking_duration
    r.pause_threshold = pause_threshold
    with sr.Microphone() as source:
        # Added noise cancellation
        r.adjust_for_ambient_noise(source, duration=1.0)
        if initial:
            ConverseAction.speak(f"Botsy online.")
        print("listening to mic...")
        sound = pygame.mixer.Sound(beep_prompt)
        sound.play()
        audio = r.listen(source, phrase_time_limit=phrase_time_limit)

        t1 = time()
        if recognize == "google":
            # Transcribe using google
            # Faster, but less accurate than whisper
            try:
                text = r.recognize_google(audio, language="en-US")
            except sr.UnknownValueError:
                print("Unable to recognize speech. Please try again.")
                text = None
        elif recognize == "whisper":
            # Transcribe using openai whisper.
            # Overly complex to try and avoid writing to disk
            audio_bytes = audio.get_wav_data()

            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False
            ) as temp_audio_file:
                temp_audio_file.write(audio_bytes)
                temp_audio_file.seek(0)
                temp_audio_file.name = "test.wav"
                # Transcribe the audio using OpenAI API
                transcript = openai.Audio.transcribe("whisper-1", file=temp_audio_file)

            # Extract the transcribed text
            text = transcript.get("text")
            text.strip()
            if text.endswith("."):
                text = text[:-1]

            # whisper sometimes returns empty like ". . . ."
            valid_chars = [".", " "]
            if all(char in valid_chars for char in text):
                print("Invalid string returning None")
                return None

        print(f"translation using {recognize} took {time() - t1}")
        return text
