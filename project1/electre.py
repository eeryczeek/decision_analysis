from functools import reduce

import pandas as pd

from problem import Problem
from solver import Solver
from srf import SRF


class Electre(Solver):
    def __init__(self, credibility_threshold: float = 0.7):
        self.credibility_threshold = credibility_threshold

    def rank(self, problem: Problem):
        pass

    def sort(self, problem: Problem, electre_srf_raw_weights: list):
        srf_weights = SRF().get_weights(8, electre_srf_raw_weights)

        boundary_classes: dict = self.get_boundary_classes(problem)
        matrix = pd.DataFrame(
            dict(), index=problem.data.index, columns=boundary_classes.keys()
        )

        print(matrix)

        for alternative in problem.data.index:
            for boundary_class_key, boundary_class_value in boundary_classes.items():
                matrix[boundary_class_key][alternative] = self.get_relation(
                    problem, problem.data.loc[alternative], boundary_class_value
                )
        return matrix

    def comprehensive_concordance(self, problem: Problem, alternative, boundary):
        print("comprehensive_concordance")
        print(f"params: {problem.parameters}")
        print(f"a: {alternative},\nb_n: {boundary}")
        return sum(
            problem.parameters[criterion]["weight"]
            * self.marginal_concordance(problem, alternative, boundary, criterion)
            for criterion in problem.data.columns
        ) / sum(
            problem.parameters[criterion]["weight"]
            for criterion in problem.data.columns
        )

    def marginal_concordance(
        self, problem: Problem, alternative1, alternative2, criterion
    ):
        p = problem.parameters[criterion]["p"]
        q = problem.parameters[criterion]["q"]

        if problem.parameters[criterion]["type"] == "cost":
            alternative1, alternative2 = alternative2, alternative1
        if alternative1[criterion] >= alternative2[criterion] - q:
            return 1
        if alternative1[criterion] < alternative2[criterion] - p:
            return 0
        return (p - (alternative2[criterion] - alternative1[criterion])) / (p - q)

    def marginal_discordance(
        self, problem: Problem, alternative1, alternative2, criterion
    ):
        if problem.parameters[criterion]["type"] == "cost":
            alternative1, alternative2 = alternative2, alternative1

        if "v" not in problem.parameters[criterion].keys():
            return 0
        else:
            v = problem.parameters[criterion]["v"]
            p = problem.parameters[criterion]["p"]

        if alternative1[criterion] <= alternative2[criterion] - v:
            return 1
        if alternative1[criterion] > alternative2[criterion] - p:
            return 0
        return (alternative2[criterion] - alternative1[criterion] - p) / (v - p)

    def outranking_credibility(self, problem: Problem, alternative1, alternative2):
        marginal_discordance = lambda criterion: self.marginal_discordance(
            problem, alternative1, alternative2, criterion
        )
        comprehensive_concordance = self.comprehensive_concordance(
            problem, alternative1, alternative2
        )

        print("outranking_credibility")
        print(f"comprensive_concordance: {comprehensive_concordance}")

        return reduce(
            lambda x, y: x * y,
            [
                (1 - marginal_discordance(criterion))
                / (1 - comprehensive_concordance)  # TODO: division by zero
                for criterion in problem.data.columns
                if comprehensive_concordance < marginal_discordance(criterion)
            ],
            comprehensive_concordance,
        )

    def get_relation(self, problem: Problem, alternative, boundary_profile):
        outranking_credibility_alternative = self.outranking_credibility(
            problem, alternative, boundary_profile
        )
        outranking_credibility_boundary = self.outranking_credibility(
            problem, boundary_profile, alternative
        )

        if outranking_credibility_alternative >= self.credibility_threshold:
            if outranking_credibility_boundary >= self.credibility_threshold:
                return "|"
            else:
                return ">"
        else:
            if outranking_credibility_boundary >= self.credibility_threshold:
                return "<"
            else:
                return "?"

    def get_boundary_classes(self, problem: Problem, n_classes: int = 3) -> dict:
        boundaries = {
            f"b{i}": self.get_boundary_values(problem, i, n_classes)
            for i in range(n_classes + 1)
        }
        return boundaries

    def get_boundary_values(self, problem: Problem, index: int, n_classes: int):
        return {
            data_column: (
                problem.data[data_column].max() - problem.data[data_column].min()
            )
            * (
                index
                if problem.parameters[data_column]["type"] == "gain"
                else n_classes - index
            )
            / n_classes
            + problem.data[data_column].min()
            for data_column in problem.data.columns
        }
