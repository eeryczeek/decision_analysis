from electre import Electre
from problem import Problem
from promethee1 import Promethee1
from promethee2 import Promethee2

if __name__ == "__main__":
    parameters1 = {
        "g1": {"type": "gain", "q": 1, "p": 2, "weight": 3},
        "g2": {"type": "gain", "q": 0, "p": 2, "weight": 2},
        "g3": {"type": "cost", "q": 100, "p": 300, "weight": 5},
    }
    parameters2 = {
        "Gross Domestic Product": {"type": "gain", "q": 100, "p": 1000, "weight": 1},
        "Unemployment Rate": {"type": "cost", "q": 0.1, "p": 0.2, "weight": 1},
        "Income Tax Rate": {"type": "cost", "q": 1, "p": 1, "weight": 1},
        "Inflation": {"type": "cost", "q": 0, "p": 0.1, "weight": 1},
        "Total Reserves": {"type": "gain", "q": 1, "p": 1000, "weight": 1},
        "GINI": {"type": "cost", "q": 1, "p": 1, "weight": 1},
    }
    parameters3 = {
        "g1": {"type": "gain", "q": 1, "p": 1, "weight": 3},
        "g2": {"type": "gain", "q": 0, "p": 2, "weight": 2},
        "g3": {"type": "cost", "q": 100, "p": 300, "weight": 5},
        "g4": {"type": "gain", "q": 1, "p": 1, "weight": 3},
    }
    problem = Problem("data/test_data_electre.csv", parameters3)
    promethee1 = Promethee1()
    promethee2 = Promethee2()
    electre = Electre()

    ranking1 = promethee1.rank(problem)
    ranking2 = promethee2.rank(problem)

    electre_srf_raw_weights = [
        "Unemployment Rate",
        "1 white card",
        "Income Tax Rate",
        "GINI",
        "3 white cards",
        "Inflation",
        "Gross Domestic Product",
        "Total Reserves",
    ]
    assert all(key in electre_srf_raw_weights for key in parameters2.keys())

    ranking3 = electre.sort(problem, electre_srf_raw_weights)
    print(ranking1)
    print(ranking2)
    print(ranking3)
