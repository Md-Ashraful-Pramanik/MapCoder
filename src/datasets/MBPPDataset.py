from .Dataset import Dataset
from evaluations.func_evaluate import evaluate_io, evaluate_functional_correctness
from constants.paths import *


class MBPPDataset(Dataset):
    def __init__(
        self,
        path: str = MBPP_DATA_PATH,
    ):
        super().__init__(path)
        self.id_key = "name"

    def evaluate(
        self,
        item: dict,
        cur_imp: str,
        language: str,
    ):
        # result, _ = evaluate_io(item['test_list'],cur_imp,5,True)
        # return result
        result = evaluate_functional_correctness(
            problem=item,
            completion=cur_imp
        )
        return result == "passed"

    def evaluate_sample_io(
        self,
        item: dict,
        cur_imp: str,
        language: str,
    ):
        if "sample_io" not in item:
            return True, ""
        if len(item["sample_io"]) == 0:
            return True, ""
        return evaluate_io(
            sample_io=item["sample_io"],
            completion=cur_imp,
        )

    @staticmethod
    def get_prompt(item):
        # function_signature = item['code'].split('\n')[0].strip()
        # return f"{item['text']}\nFunction Signature: {function_signature}"
        return item["prompt"]
