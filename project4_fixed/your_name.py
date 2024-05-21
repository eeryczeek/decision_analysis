import numpy as np
from player import Player


class YourName(Player):
    def __init__(self, name):
        super().__init__(name)
        self.cards = []
        self.stack = []
        self.opp_cards = []
        self.bluffed = set()

    # player's random strategy
    def putCard(self, declared_card):

        highest = max(self.cards, key=lambda x: x[0])
        lowest = min(self.cards, key=lambda x: x[0])

        if not declared_card or highest[0] >= declared_card[0]:
            self.stack.append(highest)
            return highest, highest

        else:
            self.stack.append(lowest)
            bluff = (declared_card[0], (declared_card[1] + 1) % 4)
            self.bluffed.add(bluff)
            return lowest, bluff

    def findNotDeclared(self, declared_card):
        for i in range(declared_card[0], 15):
            for j in range(4):
                if (i, j) not in self.stack:
                    return (i, j)

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if checked:
            removed = self.stack[-noTakenCards:]
            self.stack = self.stack[:-noTakenCards]
            for card in removed:
                if card in self.bluffed:
                    self.bluffed.remove(card)

    def checkCard(self, opponent_declaration):
        if opponent_declaration is not None:
            to_check = False

            if opponent_declaration in self.stack or opponent_declaration in self.cards:
                to_check = True

            self.stack.append(opponent_declaration)
            if len(self.cards) == 1 and self.cards[0][0] < opponent_declaration[0]:
                to_check = True

            if self.findNotDeclared(opponent_declaration) is None:
                to_check = True

            if np.random.rand() < 0.2:
                to_check = True

        return to_check
