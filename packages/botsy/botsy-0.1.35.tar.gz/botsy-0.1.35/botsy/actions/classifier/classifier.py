import importlib.util
import inspect
import os
import sys

import openai
from dotenv import load_dotenv

from botsy.actions.base_action import BaseAction
from botsy.actions.converse import ConverseAction

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)


class ActionClassifier:
    actions = {
        ConverseAction.action_type: ConverseAction(),  # This gets reinitialized with name=Botsy
    }

    action_types = list(actions.keys())

    @classmethod
    def load_remote_actions(cls, actions_dir: str, actions_dict: dict = None):
        # Both of these are needed to import modules from actions_dir
        # TODO This is also a giant hack!
        sys.path.insert(0, "/Users/jfurr")
        sys.path.insert(0, actions_dir)

        for root, dirs, _ in os.walk(actions_dir):
            # Process files only in the first level of subdirectories
            if root == actions_dir:
                for directory in dirs:
                    if directory.startswith("__") or directory.startswith("."):
                        continue

                    # TODO this is a hack to get the module name
                    module_name = f"botsy-actions.{directory}"

                    spec = importlib.util.spec_from_file_location(
                        module_name, os.path.join(root, directory, "__init__.py")
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for _, obj in inspect.getmembers(module):
                        if (
                            inspect.isclass(obj)
                            and issubclass(obj, BaseAction)
                            and obj != BaseAction
                        ):
                            actions_dict[obj.action_type] = obj()
                break
        sys.path.remove(actions_dir)

    @classmethod
    def classify_action(
        cls,
        input_text: str,
    ) -> str:
        # Put this in .env
        cls.load_remote_actions(
            actions_dir="/Users/jfurr/botsy-actions", actions_dict=cls.actions
        )

        from botsy.actions.classifier.build_classifier import get_prediction

        # Check if we are using the SVM classifier or GPT-3.5
        use_svm: bool = os.environ.get("SVM_ACTIONS_CLASSIFIER", "").lower() in [
            "true",
            "yes",
            "1",
        ]

        if use_svm:
            action = get_prediction([input_text])[0]
            print(f"SVM classifier.  action:={action}")
            cls.actions[action].execute(input_text)
            return action.lower()
        else:
            # classify using GPT-3.5
            messages = [
                {
                    "role": "system",
                    "content": ". ".join(
                        [
                            f"You are an AI that classifies user inputs into available actions: {','.join(cls.action_types)}"
                        ]
                    ),
                },
                {
                    "role": "user",
                    "content": ". ".join(
                        [
                            f"You are ONLY allowed to responsd with one of the following options: {','.join(cls.action_types)}",
                            f"Pleaes classify the following input: {input_text}",
                        ]
                    ),
                },
            ]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=20,
                    n=1,
                    temperature=0.0,
                )

                action = response.choices[0].message["content"].strip().lower()

                if action not in cls.action_types:
                    print(f"Invalid action: {action}")
                    input()
                else:
                    cls.actions[action].execute(input_text)

                return action.lower()

            except openai.error.InvalidRequestError as e:
                print(f"Error: {str(e)}")
                return None
