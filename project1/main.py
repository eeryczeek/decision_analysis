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
    parameters = {
        "Gross Domestic Product": {"type": "gain", "q": 100, "p": 1000, "weight": 3},
        "Unemployment Rate": {"type": "cost", "q": 0.01, "p": 0.2, "weight": 9},
        "Income Tax Rate": {"type": "cost", "q": 1, "p": 10, "weight": 1},
        "Inflation": {"type": "cost", "q": 0.01, "p": 0.4, "weight": 5},
        "Total Reserves": {"type": "gain", "q": 1000, "p": 1000000, "weight": 7},
        "GINI": {"type": "cost", "q": 1, "p": 10, "weight": 3},
    }
    parameters3 = {
        "g1": {"type": "gain", "q": 1, "p": 1, "weight": 3},
        "g2": {"type": "gain", "q": 0, "p": 2, "weight": 2},
        "g3": {"type": "cost", "q": 100, "p": 300, "weight": 5},
        "g4": {"type": "gain", "q": 1, "p": 1, "weight": 3},
    }
    problem = Problem("./data/prunned_dataset.csv", parameters)
    promethee1 = Promethee1()
    promethee2 = Promethee2()
    electre = Electre()

    ranking1 = promethee1.rank(problem, plot=False)
    ranking2 = promethee2.rank(problem, plot=False)

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
    assert all(key in electre_srf_raw_weights for key in parameters.keys())

    ranking3 = electre.sort(problem, electre_srf_raw_weights)
    print(ranking1)
    print(ranking2)
    print(ranking3)
