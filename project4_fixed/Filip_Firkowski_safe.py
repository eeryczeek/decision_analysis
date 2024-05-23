import numpy as np
import copy
import random
from player import Player


class Filip_Firkowski_safe(Player):

    def startGame(self, cards):
        super().startGame(cards)
        self.all_present_cards = copy.copy(self.cards)
        self.deck = [(number, color) for color in range(4)
                     for number in range(9, 15)]
        self.opponent = 8
        self.turn = 0

    def putCard(self, declared_card):
        if self.turn == 1:
            self.opponent -= 1
        for card in self.cards:
            if card not in self.all_present_cards:
                self.all_present_cards.append(card)
        my_cost = self.cost(self.cards, len(self.cards))
        enemy_cost = self.cost([], self.opponent)
        return self.ultra_safe(declared_card)

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards:
            return True
        if len(self.cards) == 1 and self.cards[0][0] < opponent_declaration[0]:
            return True
        my_cost = self.cost(self.cards, len(self.cards))
        enemy_cost = self.cost([], self.opponent)
        return False

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=False):
        self.turn = 1
        super().getCheckFeedback(checked, iChecked, iDrewCards,
                                 revealedCard, noTakenCards, log=False)
        if revealedCard is not None and revealedCard not in self.all_present_cards:
            self.all_present_cards.append(revealedCard)
        if checked == 1 and iDrewCards == 0:
            self.opponent += noTakenCards

    def cost(self, hand, size):
        cost = 0
        for card in hand:
            cost += (15 - card[0])
        cost += (size - len(hand)) * 3
        return cost

    def safe(self, declared_card):
        declared_card = [8, 0] if declared_card is None else declared_card
        if all(declared_card[0] > x[0] for x in self.cards):
            card = min(self.cards, key=lambda x: x[0])
            temp = [card for card in self.deck if card[0] >=
                    declared_card[0] and card not in self.all_present_cards]
            temp = [[14, 0]] if len(temp) == 0 else temp
            declaration = random.choice(temp)
        else:
            card = random.choice(
                [card for card in self.cards if card[0] >= declared_card[0]])
            declaration = card
        return card, declaration

    def greedy(self, declared_card):
        declared_card = [8, 0] if declared_card is None else declared_card
        card = min(self.cards, key=lambda x: x[0])
        temp = [card for card in self.deck if card[0] >=
                declared_card[0] and card not in self.all_present_cards]
        temp = [[14, random.choice([0, 1, 2, 3])]] if len(temp) == 0 else temp
        declaration = random.choice(temp)
        return card, declaration

    def ultra_safe(self, declared_card):
        declared_card = [8, 0] if declared_card is None else declared_card
        if all(declared_card[0] > x[0] for x in self.cards):
            card = min(self.cards, key=lambda x: x[0])
            temp = [card for card in self.deck if card[0] >=
                    declared_card[0] and card not in self.all_present_cards]
            temp = [[14, 0]] if len(temp) == 0 else temp
            declaration = random.choice(temp)
        else:
            card = min([card for card in self.cards if card[0]
                       >= declared_card[0]], key=lambda x: x[0])
            declaration = card
        return card, declaration
