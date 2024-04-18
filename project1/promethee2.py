import pandas as pd

from solver import Solver
from problem import Problem
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Promethee2(Solver):
    def rank(self, problem: Problem, plot: bool = False):
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
        flow = flow.sort_values(ascending=False)

        assert sum(flow) < 1e-6
        if plot:
            self.plot_graph(flow)
        return flow.sort_values(ascending=False)

    def plot_graph(self, ranking_nodes):
        plt.figure(2, figsize=(12, 8))
        options = {
            "font_size": 12,
            "node_size": 400,
            "node_color": "gray",
            "edgecolors": "gray",
            "linewidths": 2,
            "width": 2,
        }
        G = nx.DiGraph()
        for alternative1, alternative2 in zip(ranking_nodes.index[:-1], ranking_nodes.index[1:]):
            G.add_edge(alternative1, alternative2)

        pos = nx.spectral_layout(G)
        for node, position in pos.items():
            pos[node] = position + np.random.normal(scale=0.02, size=2)
        pos = nx.spring_layout(G, k=0.7, pos=pos, iterations=3)

        nx.draw_networkx(G, with_labels=True, pos=pos, **options)
        plt.title("Promethee 2 ranking")
        plt.savefig('project1/results/ranking_graph_promethee2.png')
