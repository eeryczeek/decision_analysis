import pandas as pd

from solver import Solver
from problem import Problem


class SRF():
    def get_weights(self, ratio: int, ranking: list[str]):
        ranks = dict()
        white_cards = 0
        maximal_rank = 0
        rank = 1
        for criterion_or_white_cards in ranking[::-1]:
            if 'white card' in criterion_or_white_cards:
                white_cards += int(criterion_or_white_cards.split()[0])
            else:
                ranks[criterion_or_white_cards] = rank + white_cards
                maximal_rank = rank + white_cards
                rank += 1

        non_normalized = {criterion: 1 + (ratio-1) * (rank-1)/(maximal_rank-1)
                          for criterion, rank in ranks.items()}

        normalized = {criterion: value / sum(non_normalized.values())
                      for criterion, value in non_normalized.items()}

        return normalized
