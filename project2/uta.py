import pandas as pd
from problem import Problem
from solver import Solver
from pulp import LpVariable, LpProblem, LpMinimize, LpStatus, value, lpSum, LpConstraint


class BreakPoint:
    def __init__(self, value: float, utility: LpVariable):
        self.value = value
        self.utility = utility

    def __str__(self):
        return f'{self.value}: {value(self.utility)}'

    def __repr__(self):
        return self.__str__()


class UTA(Solver):
    def __init__(self):
        self.problem = LpProblem('UTA', LpMinimize)
        self.break_points = dict()
        self.binary_variables = dict()

    def add_objective(self, problem: Problem):
        self.problem += lpSum(
            set(self.binary_variables.values()))
        return self

    def add_constraints(self, problem: Problem, relations: list[str] = None):
        self.add_breaking_values_constraints(problem)
        self.add_relations_constraints(problem, relations)
        return self

    def get_resulting_ranking(self, problem: Problem) -> None:
        matrix = pd.DataFrame(
            columns=['Utility', 'Rank'], index=problem.data.index)
        for alternative in problem.data.index:
            matrix.at[alternative, 'Utility'] = self.get_utility_value(
                problem, alternative)
        matrix['Rank'] = matrix['Utility'].rank(ascending=False)
        matrix = matrix.sort_values(by='Rank')

        return matrix

    def get_utility_value(self, problem: Problem, alternative: str) -> float:
        return sum(value(break_point1.utility) + (problem.data[data_column][alternative] - break_point1.value) / (
            break_point2.value - break_point1.value) * (value(break_point2.utility) - value(break_point1.utility))
            for data_column in problem.data.columns
            for break_point1, break_point2 in zip(self.break_points[data_column][:-1],
                                                  self.break_points[data_column][1:])
            if break_point1.value <= problem.data[data_column][alternative] < break_point2.value)

    def get_utility_formula(self, problem: Problem, alternative: str):
        return sum(break_point1.utility + (problem.data[data_column][alternative] - break_point1.value) / (
            break_point2.value - break_point1.value) * (break_point2.utility - break_point1.utility)
            for data_column in problem.data.columns
            for break_point1, break_point2 in zip(self.break_points[data_column][:-1],
                                                  self.break_points[data_column][1:])
            if break_point1.value <= problem.data[data_column][alternative] < break_point2.value)

    def add_relations_constraints(self, problem: Problem, relations: list[str]) -> None:
        for relation in relations:
            alternative1, sign, alternative2 = relation.split(' ')
            variable = LpVariable(name=f'{relation}', cat='Binary')
            self.binary_variables[relation] = variable
            if sign == 'P':
                self.problem += (
                    self.get_utility_formula(problem, alternative1) >= self.get_utility_formula(problem,
                                                                                                alternative2) + 1e-6 - variable)
            elif sign == 'I':
                self.problem += (
                    self.get_utility_formula(problem, alternative1) == self.get_utility_formula(problem,
                                                                                                alternative2) - variable)
            else:
                raise ValueError(
                    f'Invalid relation sign: {sign}. Must be either ">" or "=".')

    def add_breaking_values_constraints(self, problem: Problem) -> None:
        maximal_variables = []
        self.break_points = self.get_break_points(problem)
        self.minimal_value = 1/2/len(problem.data.columns)
        for constraint in problem.data.columns:
            if problem.parameters[constraint]['type'] == 'gain':
                self.problem += (
                    self.break_points[constraint][0].utility == 0)
                self.problem += (
                    self.break_points[constraint][-1].utility <= 0.5)
                self.problem += (
                    self.break_points[constraint][-1].utility >= self.minimal_value)
                maximal_variables.append(
                    self.break_points[constraint][-1].utility)
                for break_point1, break_point2 in zip(self.break_points[constraint][:-1], self.break_points[constraint][1:]):
                    self.problem += (break_point2.utility >=
                                     break_point1.utility)
            else:
                self.problem += (
                    self.break_points[constraint][-1].utility == 0)
                self.problem += (
                    self.break_points[constraint][0].utility <= 0.5)
                self.problem += (
                    self.break_points[constraint][0].utility >= self.minimal_value)
                maximal_variables.append(
                    self.break_points[constraint][0].utility)
                for break_point1, break_point2 in zip(self.break_points[constraint][:-1], self.break_points[constraint][1:]):
                    self.problem += (break_point1.utility >=
                                     break_point2.utility)
        self.problem += (lpSum(maximal_variables) == 1)
        return None

    def get_break_points(self, problem: Problem) -> list:
        for data_column in problem.data.columns:
            n_points = problem.parameters[data_column]['break points'] + 1
            breaking_values = [(problem.data[data_column].max() - problem.data[data_column].min())
                               * index / (n_points) + problem.data[data_column].min() for index in range(n_points + 1)]
            self.break_points[data_column] = [BreakPoint(breaking_values[index], LpVariable(name=f'{data_column}_{
                                                         breaking_values[index]:.2f}', lowBound=0, upBound=1)) for index in range(n_points + 1)]
        return self.break_points
