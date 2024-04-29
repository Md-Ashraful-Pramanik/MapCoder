from utils.jsonl import read_jsonl


class Dataset(object):
    def __init__(
        self,
        path: str,
    ):
        self.path = path
        self.data = None
        self.id_key = ""
        self.load()

    def load(self):
        self.data = read_jsonl(self.path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def evaluate(
        self,
        item: dict,
        cur_imp: str,
        language: str,
    ):
        raise NotImplementedError

    @staticmethod
    def get_prompt(item):
        raise NotImplementedError
