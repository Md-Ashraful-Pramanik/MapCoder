import os

from utils.jsonl import read_jsonl, write_jsonl

"""
In this file, we define the Results class, 
which is used to store the results of the simulation.

It will take a result path at first and after each 
simulation, it will save the results in that path.

Results are in the form of a list of dictionaries
and will be saved as a jsonl file.
"""


class Results(object):
    def __init__(
        self, 
        result_path: str, 
        discard_previous_run: bool = False
    ):
        self.result_path = result_path
        self.discard_previous_run = discard_previous_run
        self.load_results()

    def add_result(self, result: dict):
        self.results.append(result)
        self.save_results()

    def save_results(self):
        write_jsonl(self.result_path, self.results)

    def load_results(self):
        if os.path.exists(self.result_path):
            if self.discard_previous_run:
                os.remove(self.result_path)
            else:
                self.results = read_jsonl(self.result_path)
        else:
            self.results = []

    def get_results(self):
        return self.results

    def __len__(self):
        return len(self.results)

    def __getitem__(self, idx):
        return self.results[idx]
