import os
import dotenv
from openai import OpenAI, AzureOpenAI

from .Base import BaseModel
from utils.token_count import token_count

dotenv.load_dotenv()


class OpenAIBaseModel(BaseModel):
    """
    OpenAI Model interface. Can be used for models hosted on both OpenAI's platform and
    on Azure.

    Arguments
    ---------
    api_type : str
        Must be one of "openai" or "azure". If not provided, the implementation will try
        to induce it from environment variables `OPEN_API_TYPE`, `AZURE_*` or default to
        "openai"
    api_base : str
        URL where the model is hosted. Can be left as None for models hosted on OpenAI's
        platform. If not provided, the implementation will look at environment variables
        `OPENAI_API_BASE` or `AZURE_API_URL`
    api_version : str
        Version of the API to use. If not provided, the implementation will derive it
        from environment variables `OPENAI_API_VERSION` or `AZURE_API_VERSION`. Must be
        left as None for models hosted on OpenAI's platform
    api_key : str
        Authentication token for the API. If not provided, the implementation will derive it
        from environment variables `OPENAI_API_KEY` or `AZURE_API_KEY`.
    model_name : str
        Name of the model to use. If not provided, the implementation will derive it from
        environment variables `OPENAI_MODEL` or `AZURE_ENGINE_NAME`
    engine_name : str
        Alternative for `model_name`
    temperature : float
        Temperature value to use for the model. Defaults to zero for reproducibility.
    top_p : float
        Top P value to use for the model. Defaults to 0.95
    max_tokens : int
        Maximum number of tokens to pass to the model. Defaults to 800
    frequency_penalty : float
        Frequency Penalty to use for the model.
    presence_penalty : float
        Presence Penalty to use for the model.
    """

    def __init__(
        self,
        api_type=None,
        api_base=None,
        api_version=None,
        api_key=None,
        engine_name=None,
        model_name=None,
        temperature=0,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
    ):
        api_type = api_type or os.getenv("API_TYPE")

        azure_vars = self.read_azure_env_vars()  if api_type == "azure" else {
            "api_version": None,
            "api_base": None,
            "api_key": None,
            "model": None
        }
        openai_vars = self.read_openai_env_vars() if api_type == "openai" else {
            "api_version":None, 
            "api_base": None,
            "api_key": None,
            "model": None
        }

        api_base = api_base or openai_vars["api_base"] or azure_vars["api_base"]
        api_version = api_version or openai_vars["api_version"] or azure_vars["api_version"]
        api_key = api_key or openai_vars["api_key"] or azure_vars["api_key"]
        model_name = model_name or engine_name or openai_vars["model"] or azure_vars["model"]

        # assert model_name is not None, "Model/Engine must be provided as model config or environment variable `OPENAI_MODEL`/`AZURE_ENGINE_NAME`"

        assert api_key is not None, "API Key must be provided as model config or environment variable (`OPENAI_API_KEY` or `AZURE_API_KEY`)"
        
        if api_type == "azure":
            assert api_base is not None, "API URL must be provided as model config or environment variable (`AZURE_API_BASE`)"
            assert api_version is not None, "API version must be provided as model config or environment variable (`AZURE_API_VERSION`)"

        if api_type == "azure":
            self.openai = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=api_base
            )
        else:
            self.openai = OpenAI(api_key=api_key)
        
        # GPT parameters
        self.model_params = {}
        self.model_params["model"] = model_name
        self.model_params["temperature"] = temperature
        self.model_params["top_p"] = top_p
        self.model_params["max_tokens"] = None
        self.model_params["frequency_penalty"] = frequency_penalty
        self.model_params["presence_penalty"] = presence_penalty


    @staticmethod
    def read_azure_env_vars():
        return {
            "api_version": os.getenv("AZURE_API_VERSION"),
            "api_base": os.getenv("AZURE_API_URL"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "model": os.getenv("AZURE_ENGINE_NAME", os.getenv("ENGINE_NAME")),
        }

    @staticmethod
    def read_openai_env_vars():
        return {
            "api_version": os.getenv("OPENAI_API_VERSION"),
            "api_base": os.getenv("OPENAI_API_BASE"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": os.getenv("OPENAI_MODEL"),
        }


class OpenAIModel(OpenAIBaseModel):
    def __init__(
        self,
        api_type=None,
        api_base=None,
        api_version=None,
        api_key=None,
        engine_name=None,
        model_name=None,
        temperature=0.32,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
    ):
        super().__init__(
            api_type=api_type,
            api_base=api_base,
            api_version=api_version,
            api_key=api_key,
            engine_name=engine_name,
            model_name=model_name,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
    
    def summarize_response(self, response):
        """Returns the first reply from the "assistant", if available"""
        if (
            "choices" in response
            and isinstance(response["choices"], list)
            and len(response["choices"]) > 0
            and "message" in response["choices"][0]
            and "content" in response["choices"][0]["message"]
            and response["choices"][0]["message"]["role"] == "assistant"
        ):
            return response["choices"][0]["message"]["content"]

        return response


    # @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def prompt(self, processed_input: list[dict]):
        """
        OpenAI API ChatCompletion implementation

        Arguments
        ---------
        processed_input : list
            Must be list of dictionaries, where each dictionary has two keys;
            "role" defines a role in the chat (e.g. "system", "user") and
            "content" defines the actual message for that turn

        Returns
        -------
        response : OpenAI API response
            Response from the openai python library

        """
        self.model_params["max_tokens"] = 4096

        response = self.openai.chat.completions.create(
            messages=processed_input,
            **self.model_params
        )

        return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens


class GPT4(OpenAIModel):
    def prompt(self, processed_input: list[dict]):
        self.model_params["model"] = "gpt-4-1106-preview"
        return super().prompt(processed_input)


class ChatGPT(OpenAIModel):
    def prompt(self, processed_input: list[dict]):
        self.model_params["model"] = "GPT-35-TURBO-1106"
        return super().prompt(processed_input)