import pandas as pd


class Problem:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def get_dataset(self):
        return self.dataset
