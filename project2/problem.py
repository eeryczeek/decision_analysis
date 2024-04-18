import pandas as pd


class Problem:
    def __init__(self, file_path: str, parameters: dict):
        self.data = pd.read_csv(file_path, index_col=0)
        self.parameters = parameters

    def get_dataset(self):
        return self.dataset
