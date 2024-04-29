from typing import List
import tiktoken
import os
import re
from copy import deepcopy

from .Base import BaseStrategy
from models.Base import BaseModel
from datasets.Dataset import Dataset
from results.Results import Results

# self-generate exemplars and knowledge
class AnalogicalStrategy(BaseStrategy):
    def parse_code(self, code: str):
        if "Python3 code to solve the original problem:" in code:
            code = code.split("Python3 code to solve the original problem:")[1].strip()
        
        code_pattern = r'```((.|\n)*?)```'
        if "```python" in code:
            code_pattern = r'```python((.|\n)*?)```'

        code_blocks = re.findall(code_pattern, code, re.DOTALL)

        if len(code_blocks) == 0:
            if "```" in code:
                code = code.replace("```", "")
            return code

        if type(code_blocks[-1]) == tuple or type(code_blocks[-1]) == list:
            code = "\n".join(code_blocks[-1])
        elif type(code_blocks[-1]) == str:
            code = code_blocks[-1]

        return code
    
    def run_single_pass(self, item: dict):
        input = [
            {
                "role": "user",
                "content": 
f"""Your goal is to write {self.language} code to solve competitive programming problems. Given a problem , explain the core concepts in it and provide other relevant problems. Then solve the original problem.

# Problem:
{self.data.get_prompt(item)}

# Instruction: (Your response must include the following points sequentially)

## Algorithms:
Identify the core concepts or algorithms used to solve the problem.

## Tutorial:
Write a useful tutorial about these algorithms.

## Example Problems: 
Provide three examples of relevant competitive programming problems that involve these algorithms. For each problem , describe the problem , explain the solution in detail , and then write the correct Python3 code.

## {self.language} code to solve the original problem: 
Include the following points in your response: 
- Explanation of the solution: 
- {self.language} code to solve the problem (inside ```  ``` block):""",
            },
        ]
        print(input[0]['content'])

        response, prompt_tokens, completion_tokens = self.gpt_chat(
            processed_input=input
        )

        print(response)

        return response, prompt_tokens, completion_tokens

