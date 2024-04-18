from functools import reduce

import pandas as pd

import boundary_profile as bp
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
            dict(), index=problem.data.index, columns=list(boundary_classes.keys())
        )

        for alternative in problem.data.index:
            for boundary_class_key, boundary_class_value in boundary_classes.items():
                matrix[boundary_class_key][alternative] = self.get_relation(
                    problem, problem.data.loc[alternative], boundary_class_value
                )

        pessimistic_classification = self.pessimistic_classification(problem, matrix)
        return pessimistic_classification

    def comprehensive_concordance(
        self,
        problem: Problem,
        alternative,
        boundary_profile_values,
        boundary_profile_criterions: dict[str, bp.Criterion],
    ) -> float:
        return sum(
            problem.parameters[criterion]["weight"]
            * self.marginal_concordance(
                problem,
                alternative,
                boundary_profile_values,
                boundary_profile_criterions,
                criterion,
            )
            for criterion in problem.data.columns
        ) / sum(
            problem.parameters[criterion]["weight"]
            for criterion in problem.data.columns
        )

    def marginal_concordance(
        self,
        problem: Problem,
        alternative1,
        alternative2,
        parameters: dict[str, bp.Criterion],
        criterion: str,
    ) -> float:
        p = parameters[criterion].p
        q = parameters[criterion].q

        if problem.parameters[criterion]["type"] == "cost":
            alternative1, alternative2 = alternative2, alternative1
        if alternative1[criterion] >= alternative2[criterion] - q:
            return 1
        if alternative1[criterion] < alternative2[criterion] - p:
            return 0
        return (p - (alternative2[criterion] - alternative1[criterion])) / (p - q)

    def marginal_discordance(
        self,
        problem: Problem,
        alternative1,
        alternative2,
        parameters: dict[str, bp.Criterion],
        criterion: str,
    ) -> float:
        if problem.parameters[criterion]["type"] == "cost":
            alternative1, alternative2 = alternative2, alternative1

        if "v" not in problem.parameters[criterion].keys():
            return 0
        else:
            v = parameters[criterion].v
            p = parameters[criterion].p

        if alternative1[criterion] <= alternative2[criterion] - v:
            return 1
        if alternative1[criterion] > alternative2[criterion] - p:
            return 0
        return (alternative2[criterion] - alternative1[criterion] - p) / (v - p)

    def outranking_credibility(
        self,
        problem: Problem,
        alternative1,
        alternative2,
        parameters: dict[str, bp.Criterion],
    ) -> float:
        marginal_discordance = lambda criterion: self.marginal_discordance(
            problem, alternative1, alternative2, parameters, criterion
        )
        comprehensive_concordance = self.comprehensive_concordance(
            problem, alternative1, alternative2, parameters
        )

        return reduce(
            lambda x, y: x * y,
            [
                (1 - marginal_discordance(criterion)) / (1 - comprehensive_concordance)
                for criterion in problem.data.columns
                if comprehensive_concordance < marginal_discordance(criterion)
            ],
            comprehensive_concordance,
        )

    def get_relation(
        self, problem: Problem, alternative, boundary_profile: bp.BoundaryProfile
    ) -> str:
        boundary_profile_values = boundary_profile.to_alternative()
        outranking_credibility_alternative = self.outranking_credibility(
            problem, alternative, boundary_profile_values, boundary_profile.criterions
        )
        outranking_credibility_boundary = self.outranking_credibility(
            problem, boundary_profile_values, alternative, boundary_profile.criterions
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

    def get_boundary_classes(
        self,
        problem: Problem,
        n_classes: int = 3,
        boundary_parameters: dict = dict(),
    ) -> dict[str, bp.BoundaryProfile]:
        if not boundary_parameters:
            boundary_profiles = {
                f"b{i}": self.get_boundary_values(problem, i, n_classes)
                for i in range(n_classes + 1)
            }
        else:
            boundary_profiles = {
                f"b{i}": self.get_boundary_values(
                    problem, i, n_classes, boundary_parameters[f"b{i}"]
                )
                for i in range(n_classes + 1)
            }
        return boundary_profiles

    def get_boundary_values(
        self,
        problem: Problem,
        index: int,
        n_classes: int,
        boundary_parameters: dict = dict(),
    ):
        criterions = {
            criterion_name: bp.Criterion(
                v=boundary_parameters.get(
                    "v", problem.parameters[criterion_name].get("v", None)
                ),
                p=boundary_parameters.get(
                    "p", problem.parameters[criterion_name].get("p", 0)
                ),
                q=boundary_parameters.get(
                    "q", problem.parameters[criterion_name].get("q", 0)
                ),
                value=(
                    (
                        problem.data[criterion_name].max()
                        - problem.data[criterion_name].min()
                    )
                    * (
                        index
                        if problem.parameters[criterion_name]["type"] == "gain"
                        else n_classes - index
                    )
                    / n_classes
                    + problem.data[criterion_name].min()
                ),
            )
            for criterion_name in problem.data.columns
        }

        return bp.BoundaryProfile(criterions)

    def pessimistic_classification(self, problem: Problem, relations: pd.DataFrame):
        """Returns the class in which each alternative should be classified according to the pessimistic classification method"""
        number_of_classes = len(relations.columns)
        class_assignments = {
            country: f"C{number_of_classes - sum(1 for value in performances if value in ['<', '?'])}"
            for country, performances in relations.iterrows()
        }
        return pd.DataFrame(
            class_assignments.values(),
            index=list(class_assignments.keys()),
            columns=["Class"],
        )
