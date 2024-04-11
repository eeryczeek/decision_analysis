import itertools
import pandas as pd

from solver import Solver
from problem import Problem
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class RankingNode:
    def __init__(self, alternative: str, positive_flow: float, negative_flow: float):
        self.alternative = alternative
        self.positive_flow = positive_flow
        self.negative_flow = negative_flow
        self.net_flow = positive_flow - negative_flow
        self.better_than = []
        self.uncomparable_to = []
        self.indifferent_to = []
        self.to_remove = []

    def __str__(self):
        return f'{self.better_than}, {self.uncomparable_to}\n'

    def __repr__(self):
        return self.__str__()


class Promethee1(Solver):
    def rank(self, problem: Problem, plot=False):
        comprehensive_prefference_matrix = self.comprehensive_prefference_matrix(
            problem)
        positive_flow = pd.Series(0, index=problem.data.index, dtype=float)
        negative_flow = pd.Series(0, index=problem.data.index, dtype=float)

        for alternative1 in problem.data.index:
            positive_flow.at[alternative1] = comprehensive_prefference_matrix.loc[alternative1].sum(
            )
            negative_flow.at[alternative1] = comprehensive_prefference_matrix[alternative1].sum(
            )

        positive_flow.sort_values(ascending=False, inplace=True)
        negative_flow.sort_values(ascending=True, inplace=True)

        ranking_nodes = {alternative: RankingNode(alternative, positive_flow.at[alternative], negative_flow.at[alternative])
                         for alternative in positive_flow.index}

        for alternative1, alternative2 in itertools.product(problem.data.index, repeat=2):
            if positive_flow.at[alternative1] > positive_flow.at[alternative2] and negative_flow.at[alternative1] < negative_flow.at[alternative2] or \
               positive_flow.at[alternative1] == positive_flow.at[alternative2] and negative_flow.at[alternative1] < negative_flow.at[alternative2] or \
               positive_flow.at[alternative1] > positive_flow.at[alternative2] and negative_flow.at[alternative1] == negative_flow.at[alternative2]:
                ranking_nodes[alternative1].better_than.append(alternative2)
            elif positive_flow.at[alternative1] > positive_flow.at[alternative2] and negative_flow.at[alternative1] > negative_flow.at[alternative2] or \
                    positive_flow.at[alternative1] < positive_flow.at[alternative2] and negative_flow.at[alternative1] < negative_flow.at[alternative2]:
                ranking_nodes[alternative1].uncomparable_to.append(
                    alternative2)
            elif positive_flow.at[alternative1] == positive_flow.at[alternative2] and negative_flow.at[alternative1] == negative_flow.at[alternative2]:
                ranking_nodes[alternative1].indifferent_to.append(alternative2)

        for alternative in ranking_nodes.values():
            alternative.to_remove = [better_alternative for better_alternative in alternative.better_than
                                     if any(better_alternative in ranking_nodes[alternative2].better_than for alternative2 in alternative.better_than)]

        for alternative in ranking_nodes.values():
            alternative.better_than = [
                better for better in alternative.better_than if better not in alternative.to_remove]

        if plot:
            self.plot_graph(ranking_nodes)

        return ranking_nodes

    def plot_graph(self, ranking_nodes):
        plt.figure(0, figsize=(12, 8))
        options = {
            "font_size": 12,
            "node_size": 400,
            "node_color": "gray",
            "edgecolors": "gray",
            "linewidths": 2,
            "width": 2,
        }
        G = nx.DiGraph()
        for alternative in ranking_nodes.values():
            for better_alternative in alternative.better_than:
                G.add_edge(alternative.alternative, better_alternative)

        pos = nx.spectral_layout(G)
        for node, position in pos.items():
            pos[node] = position + np.random.normal(scale=0.02, size=2)
        pos = nx.spring_layout(G, k=0.7, pos=pos, iterations=3)

        nx.draw_networkx(G, with_labels=True, pos=pos, **options)
        plt.show()
