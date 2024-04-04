import pandas as pd

from solver import Solver
from problem import Problem


class Promethee1(Solver):
    def rank(self, problem: Problem):
        comprehensive_prefference_matrix = self.comprehensive_prefference_matrix(
            problem)
        positive_flow = pd.Series(0, index=problem.data.index, dtype=float)
        negative_flow = pd.Series(0, index=problem.data.index, dtype=float)
        for alternative1 in problem.data.index:
            positive_flow.at[alternative1] = comprehensive_prefference_matrix.loc[alternative1].sum(
            )
            negative_flow.at[alternative1] = comprehensive_prefference_matrix[alternative1].sum(
            )

        for alternative1 in problem.data.index:
            for alternative2 in problem.data.index:
                if alternative1 != alternative2:
                    continue

    def classify(self, problem: Problem):
        pass
