import pandas as pd

from solver import Solver
from problem import Problem
from srf import SRF


class Electre(Solver):
    def rank(self, problem: Problem):
        pass

    def sort(self, problem: Problem):
        srf_weights = SRF().get_weights(8,
                                        ['g1', '1 white card', 'g2', 'g3', '3 white cards', 'g4'])

        boundary_classes = self.get_boundary_classes(problem)

        for alternative in problem.data.index:
            for boundary_class in boundary_classes:

    def concordance(self, ):
        pass

    def discordance(self, ):
        pass

    def get_boundary_classes(self, problem: Problem, n_classes: int = 3):
        boundaries = {f'b{i}': self.get_boundary_values(problem, i, n_classes)
                      for i in range(n_classes + 1)}
        print(boundaries)
        return boundaries

    def get_boundary_values(self, problem: Problem, index: int, n_classes: int):
        return {data_column: (problem.data[data_column].max() - problem.data[data_column].min()) * index / n_classes + problem.data[data_column].min() if problem.parameters[data_column]['type'] == 'gain' else (problem.data[data_column].max() - problem.data[data_column].min()) * (n_classes - index) / n_classes + problem.data[data_column].min() for data_column in problem.data.columns}
