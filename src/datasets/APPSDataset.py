from .Dataset import Dataset
from evaluations.evalute import contest_evaluate, contest_evaluate_public_tests
from constants.paths import *


class APPSDataset(Dataset):
    def __init__(
        self,
        path: str = APPS_DATA_PATH,
    ):
        super().__init__(path)
        self.id_key = "id"

    def evaluate(
        self,
        item: dict,
        cur_imp: str,
        language: str,
    ):
        return contest_evaluate(
            generated_code=cur_imp,
            id=item["id"],
            tests=item["test_list"],
            lang=language
        )

    def evaluate_sample_io(
        self,
        item: dict,
        cur_imp: str,
        language: str,
    ):
        if len(item["sample_io"]) == 0:
            return True, ""
        return contest_evaluate_public_tests(
            generated_code=cur_imp,
            id=item["id"],
            tests=item["sample_io"],
            lang=language
        )

    @staticmethod
    def get_prompt(item):
        sample_io_format = ""
        if len(item['sample_io']) > 0:
            sample_io_format = f"Sample Input Format:\n{item['sample_io'][0]['input']}\nSample Output Format:\n{item['sample_io'][0]['output'][0]}\n\n-------\n"

        return f"{item['description']}\n\n{sample_io_format}Important: You must follow the input output format. Input should be taken from standard input and output should be given to standard output.\nNote: If you are writing a function then after the function definition take input from using `input()` function, call the function with specified parameters and finally print the output of the function."
