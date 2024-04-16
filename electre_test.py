import unittest

from electre import Electre
from problem import Problem


class TestElectre(unittest.TestCase):
    def setUp(self) -> None:
        parameters1 = {
            "g1": {"type": "gain", "q": 1, "p": 2, "weight": 3},
            "g2": {"type": "gain", "q": 0, "p": 2, "weight": 2},
            "g3": {"type": "cost", "q": 100, "p": 300, "weight": 5},
        }
        self.problem = Problem("data/data1.csv", parameters1)
        self.electre = Electre()

    def test_marginal_concordance_gain_0(self):
        alternative1 = {"g1": 1, "g2": 1, "g3": 1}
        alternative2 = {"g1": 3, "g2": 2, "g3": 2}
        criterion = "g1"
        self.assertEqual(
            self.electre.marginal_concordance(
                self.problem, alternative1, alternative2, criterion
            ),
            0,
        )

    def test_marginal_concordance_gain_1(self):
        alternative1 = {"g1": 1, "g2": 1, "g3": 1}
        alternative2 = {"g1": 2, "g2": 2, "g3": 2}
        criterion = "g1"
        self.assertEqual(
            self.electre.marginal_concordance(
                self.problem, alternative1, alternative2, criterion
            ),
            1,
        )

    def test_marginal_concordance_gain_0_5(self):
        alternative1 = {"g1": 1, "g2": 1, "g3": 1}
        alternative2 = {"g1": 2.5, "g2": 2, "g3": 2}
        criterion = "g1"
        self.assertEqual(
            self.electre.marginal_concordance(
                self.problem, alternative1, alternative2, criterion
            ),
            0.5,
        )

    def test_marginal_concordance_cost_1(self):
        alternative1 = {"g1": 1, "g2": 1, "g3": 102}
        alternative2 = {"g1": 3, "g2": 2, "g3": 2}
        criterion = "g3"
        self.assertEqual(
            self.electre.marginal_concordance(
                self.problem, alternative1, alternative2, criterion
            ),
            1,
        )

    def test_marginal_concordance_cost_0(self):
        alternative1 = {"g1": 1, "g2": 1, "g3": 401}
        alternative2 = {"g1": 3, "g2": 2, "g3": 100}
        criterion = "g3"
        self.assertEqual(
            self.electre.marginal_concordance(
                self.problem, alternative1, alternative2, criterion
            ),
            0,
        )

    def test_marginal_concordance_cost_0_5(self):
        alternative1 = {"g1": 1, "g2": 1, "g3": 300}
        alternative2 = {"g1": 3, "g2": 2, "g3": 100}
        criterion = "g3"
        self.assertEqual(
            self.electre.marginal_concordance(
                self.problem, alternative1, alternative2, criterion
            ),
            0.5,
        )
