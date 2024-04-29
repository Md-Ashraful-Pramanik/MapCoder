import pprint
import os
import google.generativeai as genai
import dotenv
import time

from .Base import BaseModel

dotenv.load_dotenv()


class Gemini(BaseModel):
    def __init__(self, temperature=0):
        genai.configure(api_key=os.getenv("Google_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')

    # @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def prompt(self, processed_input):
        for i in range(10):
            try:
                response = self.model.generate_content(
                    processed_input[0]['content'],
                    # generation_config=genai.types.GenerationConfig(
                    #     candidate_count=1,
                    #     max_output_tokens=2048,
                    #     temperature=0
                    # )
                )
                return response.text, 0, 0
            except Exception as e:
                time.sleep(2)
        
        return response.text, 0, 0

