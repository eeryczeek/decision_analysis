from abc import abstractmethod
import pandas as pd


class Solver:
    @abstractmethod
    def rank(self, matrix: pd.DataFrame):
        pass

    @abstractmethod
    def classify(self, matrix: pd.DataFrame):
        pass
