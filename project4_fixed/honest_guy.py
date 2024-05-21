import numpy as np
from player import Player


class HonestGuy(Player):
    def __init__(self, name):
        super().__init__(name)
        self.cards = []
        self.stack = []
        self.opp_cards = []
        self.bluffed = set()

    # player's random strategy
    def putCard(self, declared_card):

        self.cards = sorted(self.cards, key=lambda x: x[0])
        if not declared_card:
            lowest_possible = self.cards[0]
            self.stack.append(lowest_possible)
            return lowest_possible, lowest_possible
        else:
            lowest_possible = min([card for card in self.cards if card[0]
                                  >= declared_card[0]], key=lambda x: x[0], default=None)
            if lowest_possible:
                self.stack.append(lowest_possible)
                return lowest_possible, lowest_possible
            else:
                print('this shouldn\'t happen')
                noCards = min(3, len(self.stack))
                self.stack = self.stack[:-noCards]
                return "draw"

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

            # Drawing is never optimal so make sure we are not forced to draw
            if len(self.cards) == 1 and self.cards[0][0] < opponent_declaration[0]:
                to_check = True

            lowest_possible = min([card for card in self.cards if card[0]
                                  >= opponent_declaration[0]], key=lambda x: x[0], default=None)
            if not lowest_possible:
                to_check = True

            # if opponent_declaration[0] == 14:
            #     self.stack.append(opponent_declaration)
            #     return True

            if np.random.rand() < 0.2:
                to_check = True

        return to_check
