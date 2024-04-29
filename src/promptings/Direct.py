from typing import List
import tiktoken
import os
from copy import deepcopy

from .Base import BaseStrategy
from models.Base import BaseModel
from datasets.Dataset import Dataset
from results.Results import Results


class DirectStrategy(BaseStrategy):
    def run_single_pass(self, item: dict):
        processed_input = [
            {
                "role": "user",
                "content": f'{self.data.get_prompt(item)}\n\Generate {self.language} code to solve the above mentioned problem:',
            },
        ]
        return self.gpt_chat(processed_input=processed_input)
