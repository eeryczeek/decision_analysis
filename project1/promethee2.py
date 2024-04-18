import pandas as pd

from solver import Solver
from problem import Problem


class Promethee2(Solver):
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

        flow = positive_flow - negative_flow

        assert sum(flow) < 0.001
        return flow.sort_values(ascending=False)
