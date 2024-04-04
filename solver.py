from abc import abstractmethod
import pandas as pd

from problem import Problem


class Solver:
    @abstractmethod
    def rank(self, problem: Problem):
        pass

    @abstractmethod
    def classify(self, problem: Problem):
        pass

    def comprehensive_prefference_matrix(self, problem: Problem):
        comprehensive_prefference_matrix = pd.DataFrame(
            0, index=problem.data.index, columns=problem.data.index, dtype=float)
        marginal_prefference_matrices = {criterion: self.marginal_prefference_matrix(
            criterion, problem) for criterion in problem.data.columns}
        for alternative1 in problem.data.index:
            for alternative2 in problem.data.index:
                comprehensive_prefference_matrix.at[alternative1, alternative2] = sum(
                    [marginal_prefference_matrices[criterion].at[alternative1, alternative2] * problem.parameters[criterion]['weight'] for criterion in problem.data.columns])

        for alternative1 in problem.data.index:
            for alternative2 in problem.data.index:
                comprehensive_prefference_matrix.at[alternative1, alternative2] /= sum(
                    [problem.parameters[criterion]['weight'] for criterion in problem.data.columns])
        return comprehensive_prefference_matrix

    def marginal_prefference_matrix(self, criterion, problem: Problem):
        marginal_prefference_matrix = pd.DataFrame(
            0, index=problem.data.index, columns=problem.data.index, dtype=float)
        for alternative1 in problem.data.index:
            for alternative2 in problem.data.index:
                marginal_prefference_matrix.at[alternative1, alternative2] = self.marginal_prefference(
                    alternative1, alternative2, criterion, problem)
        return marginal_prefference_matrix

    def marginal_prefference(self, alternative1, alternative2, criterion, problem: Problem):
        if problem.parameters[criterion]['type'] == 'gain':
            if problem.data[criterion][alternative1] - problem.data[criterion][alternative2] > problem.parameters[criterion]['p']:
                return 1
            if problem.data[criterion][alternative1] - problem.data[criterion][alternative2] <= problem.parameters[criterion]['q']:
                return 0
            return (problem.data[criterion][alternative1] - problem.data[criterion][alternative2] - problem.parameters[criterion]['q']) / (
                problem.parameters[criterion]['p'] - problem.parameters[criterion]['q'])

        if problem.parameters[criterion]['type'] == 'cost':
            if problem.data[criterion][alternative2] - problem.data[criterion][alternative1] > problem.parameters[criterion]['p']:
                return 1
            if problem.data[criterion][alternative2] - problem.data[criterion][alternative1] <= problem.parameters[criterion]['q']:
                return 0
            return (problem.data[criterion][alternative2] - problem.data[criterion][alternative1] - problem.parameters[criterion]['q']) / (
                problem.parameters[criterion]['p'] - problem.parameters[criterion]['q'])
