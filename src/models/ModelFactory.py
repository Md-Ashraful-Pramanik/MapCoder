from models.Gemini import Gemini
from models.OpenAI import ChatGPT
from models.OpenAI import GPT4


class ModelFactory:
    @staticmethod
    def get_model_class(model_name):
        if model_name == "Gemini":
            return Gemini
        elif model_name == "ChatGPT":
            return ChatGPT
        elif model_name == "GPT4":
            return GPT4
        else:
            raise Exception(f"Unknown model name {model_name}")
