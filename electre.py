import pandas as pd

from solver import Solver
from problem import Problem
from srf import SRF


class Electre(Solver):

    def rank(self, problem: Problem):
        pass

    def sort(self, problem: Problem, electre_srf_raw_weights: list):
        srf_weights = SRF().get_weights(8, electre_srf_raw_weights)

        boundary_classes: dict = self.get_boundary_classes(problem)
        matrix = pd.DataFrame(dict(), index=problem.data.index,
                              columns=boundary_classes.keys())

        for alternative in problem.data.index:
            for boundary_class_key, boundary_class_value in boundary_classes.items():
                matrix[boundary_class_key][alternative] = {'c(a, b)': self.comprehensive_concordance(problem, problem.data.loc[alternative], boundary_class_value),
                                                           #    'd(a, b)': self.discordance(problem, problem.data[alternative], boundary_class),
                                                           'c(b, a)': self.comprehensive_concordance(problem, boundary_class_value, problem.data.loc[alternative]),
                                                           #    'd(b, a)': self.discordance(problem, boundary_class, problem.data[alternative])
                                                           }

        return matrix

    def comprehensive_concordance(self, problem: Problem, alternative, boundary):
        return sum(problem.parameters[criterion]['weight'] * self.concordance(problem, alternative, boundary)[criterion] for criterion in problem.data.columns) / sum(problem.parameters[criterion]['weight'] for criterion in problem.data.columns)

    def concordance(self, problem: Problem, alternative1, alternative2):
        return {criterion: self.marginal_concordance(problem, alternative1, alternative2, criterion) for criterion in problem.data.columns}

    def marginal_concordance(self, problem: Problem, alternative1, alternative2, criterion):
        if alternative1[criterion] > alternative2[criterion] + problem.parameters[criterion]['p']:
            return 1
        return 0

    def discordance(self, alternative1, alternative2):
        return 0

    def get_boundary_classes(self, problem: Problem, n_classes: int = 3) -> dict:
        boundaries = {f'b{i}': self.get_boundary_values(problem, i, n_classes)
                      for i in range(n_classes + 1)}
        return boundaries

    def get_boundary_values(self, problem: Problem, index: int, n_classes: int):
        return {data_column: (problem.data[data_column].max() - problem.data[data_column].min()) * index / n_classes + problem.data[data_column].min() if problem.parameters[data_column]['type'] == 'gain' else (problem.data[data_column].max() - problem.data[data_column].min()) * (n_classes - index) / n_classes + problem.data[data_column].min() for data_column in problem.data.columns}
