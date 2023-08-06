import os
import tempfile
import time
from datetime import datetime
from io import BytesIO

import boto3
import pkg_resources
from pydub import AudioSegment

from botsy.actions.base_action import BaseAction
from botsy.actions.utils import listen_to_mic

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

polly_client = boto3.client("polly", region_name="us-east-1")


DONE = [
    "thats all",
    "that's all",
    "thank you",
    "thanks",
    "done",
    "exit",
    "i'm done",
    "all set",
    "that's it",
]


class ConverseAction(BaseAction):
    action_type = "converse"

    training_data = [
        "How's the weather today?",
        "Tell me a joke.",
        "How's your day going?",
        "What's your favorite food?",
        "Do you like music?",
        "What's your favorite book?",
        "Can we chat about movies?",
        "What's your favorite holiday?",
        "Do you enjoy traveling?",
        "Tell me something interesting about yourself.",
        "botys",
        "hey botsy",
    ]

    # # use GPT to generate responses for these prompts
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with open(f"{dir_path}/training_data.txt") as f:
    #     training_data = f.read().splitlines()

    def __init__(self, name="botsy", model="gpt-3.5-turbo"):
        self.model = model
        # self.model = "text-davinci-003"

        self.name = name
        self.debug = False

        # NOTE: Leave Personal Info out of these strings,
        self.messages = [
            {
                "role": "system",
                "content": f"You are {self.name}.  A helpful, creative, clever, funny, and very friendly assistant.  Current Datetime {str(datetime.now())}.",
            }
        ]

    @classmethod
    def speak(cls, text):
        import pygame  # noqa

        try:
            MAX_TEXT_LENGTH = (
                3000  # Assuming the maximum allowed length is 3000 characters
            )
            text_chunks = [
                text[i : i + MAX_TEXT_LENGTH]
                for i in range(0, len(text), MAX_TEXT_LENGTH)
            ]

            for chunk in text_chunks:
                response = polly_client.synthesize_speech(
                    Text=chunk, OutputFormat="mp3", VoiceId="Joanna"
                )
                audio_data = BytesIO(response["AudioStream"].read())
                audio = AudioSegment.from_mp3(audio_data)
                audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                audio.export(audio_file.name, format="mp3")
                pygame.mixer.music.load(audio_file.name)
                pygame.mixer.music.play()
                time.sleep((audio.duration_seconds))
                pygame.mixer.music.stop()
                audio_file.close()
                os.unlink(audio_file.name)
        except Exception as e:
            print(f"Error speaking: {e}")

    def execute(self, input_text: str, single_shot=False, brief=True) -> str:
        if brief:
            input_text += ". Keep your response brief"
        # Initialize messages list with initial user input
        self.add_message({"role": "user", "content": input_text})

        # Call ChatCompletion API to generate response for initial user input
        response = self.chat_completion()

        if single_shot:
            return response

        import pygame  # noqa

        print("response: ", response)
        print("single_shot", single_shot)

        for line in response.splitlines():
            for sentence in line.split("."):
                ConverseAction.speak(sentence)

        while True:
            text = listen_to_mic()

            if text not in [None, ""]:
                text = text.lower()

                # TODO There has to be a better way to handle this.
                for done in DONE:
                    if text.startswith(done):
                        print("Breaking from here", text)
                        ConverseAction.speak(
                            "Let me know if I can be of further assistance"
                        )
                        return

                self.add_message({"role": "user", "content": text})

                # Print messages list for debugging
                for message in self.messages:
                    print(message)

                # Play thinking sound
                # TODO this sound may not be ideal...
                prompt_file = pkg_resources.resource_filename(
                    "botsy", "sounds/thinking.wav"
                )
                sound = pygame.mixer.Sound(prompt_file)
                sound.play(10)

                # Call ChatCompletion API to generate response
                response = self.chat_completion()
                sound.stop()

                for line in response.splitlines():
                    for sentence in line.split("."):
                        ConverseAction.speak(sentence)

            else:
                print("Breaking from here")
                break

        return response
