import numpy as np
from player import Player


# This is a combination of two strategies since in testing we discovered that one player does better against opponents that declare low cards and the other against opponents that declare high cards
class Ultimate(Player):
    def __init__(self, name):
        super().__init__(name)
        self.player1 = Player1("")
        self.player2 = Player2("")
        self.players = {
            1: self.player1,
            2: self.player2
        }
        self.first_opponent_declaration = None
        self.mode = 1

    def putCard(self, declared_card):
        if declared_card is not None and self.first_opponent_declaration is None:
            self.first_opponent_declaration = declared_card
            if declared_card[0] <= 11:
                self.mode = 2
        if not self.first_opponent_declaration:
            result1 = self.player1.putCard(declared_card, self.cards)
            result2 = self.player2.putCard(declared_card, self.cards)
            return result1 if self.mode == 1 else result2
        else:
            return self.players[self.mode].putCard(declared_card, self.cards)

    def checkCard(self, opponent_declaration):
        if opponent_declaration and self.first_opponent_declaration is None:
            self.first_opponent_declaration = opponent_declaration
            if opponent_declaration[0] <= 11:
                self.mode = 2
        if not self.first_opponent_declaration:
            result1 = self.player1.checkCard(opponent_declaration, self.cards)
            result2 = self.player2.checkCard(opponent_declaration, self.cards)
            return result1 if self.mode == 1 else result2
        else:
            return self.players[self.mode].checkCard(opponent_declaration, self.cards)

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if not self.first_opponent_declaration:
            self.player1.getCheckFeedback(
                checked, iChecked, iDrewCards, revealedCard, noTakenCards, log)
            self.player2.getCheckFeedback(
                checked, iChecked, iDrewCards, revealedCard, noTakenCards, log)
        else:
            self.players[self.mode].getCheckFeedback(
                checked, iChecked, iDrewCards, revealedCard, noTakenCards, log)

# Use this player if opponent starts with high card


class Player1:
    def __init__(self, name):
        self.my_used_cards = []
        self.all_used_cards = []
        self.player_turns_on_stack = []
        self.opponent_cards = []

    def putCard(self, declared_card, cards):
        lowest = min(cards, key=lambda x: x[0])
        if declared_card is None:
            self.my_used_cards.append(lowest)
            self.all_used_cards.append(lowest)
            self.player_turns_on_stack.append('me')
            return lowest, lowest

        lowest_acceptable = min([card for card in cards if card[0]
                                >= declared_card[0]], key=lambda x: x[0], default=None)

        if lowest_acceptable is None:
            self.my_used_cards.append(lowest)
            self.all_used_cards.append(lowest)
            self.player_turns_on_stack.append('me')
            # check which card is the best to declare
            for i in range(declared_card[0], 15):
                for j in range(4):
                    if (i, j) not in self.opponent_cards:
                        return lowest, (i, j)
            return lowest, (declared_card[0], (declared_card[1] + 1) % 4)
        else:
            self.my_used_cards.append(lowest_acceptable)
            self.all_used_cards.append(lowest_acceptable)
            self.player_turns_on_stack.append('me')
            return lowest_acceptable, lowest_acceptable

    def checkCard(self, opponent_declaration, cards):
        if opponent_declaration is None:
            return False

        self.all_used_cards.append(opponent_declaration)
        self.player_turns_on_stack.append('opponent')

        lowest_acceptable = min([card for card in cards if card[0] >=
                                opponent_declaration[0]], key=lambda x: x[0], default=None)
        if lowest_acceptable is None:
            return True

        if opponent_declaration in cards or opponent_declaration in self.my_used_cards:
            return True

        return False

    def draw_cards(self, noTakenCards, iDrewCards):
        for _ in range(noTakenCards):
            self.all_used_cards.pop()
            turn = self.player_turns_on_stack.pop()
            if turn == 'me':
                my_card = self.my_used_cards.pop()
                if not iDrewCards:
                    self.opponent_cards.append(my_card)

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if noTakenCards is not None:
            self.draw_cards(noTakenCards, iDrewCards)

        if checked:
            if iChecked and iDrewCards:
                if revealedCard in self.opponent_cards:
                    self.opponent_cards.remove(revealedCard)
            elif iChecked:
                self.opponent_cards.append(revealedCard)


# Use this player if opponent starts with a low card
class Player2:
    def __init__(self, name):
        self.stack = []
        self.bluffed = set()
        self.all_cards = set()

    def putCard(self, declared_card, cards):
        declared_card = (
            declared_card[0], declared_card[1]) if declared_card else None

        highest = max(cards, key=lambda x: x[0])
        lowest = min(cards, key=lambda x: x[0])

        lowest_possible = min([card for card in cards if card[0] >= declared_card[0]],
                              key=lambda x: x[0], default=None) if declared_card else None

        if not declared_card:
            self.all_cards.add(lowest)
            self.stack.append(lowest)
            return lowest, lowest

        elif highest[0] >= declared_card[0]:
            if not lowest_possible in self.bluffed:
                self.stack.append(lowest)
                self.all_cards.add(lowest)
                self.bluffed.add(lowest_possible)
                return lowest, lowest_possible
            else:
                self.all_cards
                self.stack.append(lowest_possible)
                self.all_cards.add(lowest_possible)
                return lowest_possible, lowest_possible

        else:
            self.stack.append(lowest)
            self.all_cards.add(lowest)
            bluff = self.findNotDeclared(declared_card)
            if bluff is None:
                bluff = (declared_card[0], (declared_card[1] + 1) % 4)
            self.bluffed.add(bluff)
            return lowest, bluff

    def findNotDeclared(self, declared_card):
        for i in range(declared_card[0], 15):
            for j in range(4):
                if (i, j) not in self.stack and (i, j) not in self.bluffed:
                    return (i, j)

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if checked:
            removed = self.stack[-noTakenCards:]
            self.stack = self.stack[:-noTakenCards]
            self.bluffed = self.bluffed - set(removed)

    def checkCard(self, opponent_declaration, cards):
        opponent_declaration = (
            opponent_declaration[0], opponent_declaration[1]) if opponent_declaration else None

        if opponent_declaration is not None:
            to_check = False

            if opponent_declaration in self.stack or opponent_declaration in cards or opponent_declaration in self.bluffed:
                to_check = True

            self.stack.append(opponent_declaration)
            self.all_cards.add(opponent_declaration)

            # Drawing is never optimal so make sure we are not forced to draw
            if len(cards) == 1 and cards[0][0] < opponent_declaration[0]:
                to_check = True

            if self.findNotDeclared(opponent_declaration) is None:
                to_check = True

            lowest_possible = min([card for card in cards if card[0] >=
                                  opponent_declaration[0]], key=lambda x: x[0], default=None)
            if not lowest_possible and np.random.rand() < 0.5:
                to_check = True

        return to_check
