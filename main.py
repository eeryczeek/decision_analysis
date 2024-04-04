from problem import Problem
from promethee1 import Promethee1
from promethee2 import Promethee2
from electre import Electre
from srf import SRF

if __name__ == '__main__':
    parameters1 = {
        'g1': {'type': 'gain', 'q': 1, 'p': 1, 'weight': 3},
        'g2': {'type': 'gain', 'q': 0, 'p': 2, 'weight': 2},
        'g3': {'type': 'cost', 'q': 100, 'p': 300, 'weight': 5},
    }
    parameters2 = {
        'Gross Domestic Product': {'type': 'gain', 'q': 100, 'p': 1000, 'weight': 2},
        'Unemployment Rate': {'type': 'cost', 'q': 0.1, 'p': 0.2, 'weight': 2},
        'Income Tax Rate': {'type': 'cost', 'q': 1, 'p': 1, 'weight': 2},
        'Inflation': {'type': 'cost', 'q': 0, 'p': 0.1, 'weight': 2},
        'Total Reserves': {'type': 'gain', 'q': 1, 'p': 1000, 'weight': 2},
        'GINI': {'type': 'cost', 'q': 1, 'p': 1, 'weight': 2},
    }
    problem = Problem('data/prunned_dataset.csv', parameters2)
    promethee2 = Promethee2()
    ranking = promethee2.rank(problem)
    for key, value in ranking.items():
        print(key)
        print(value)
