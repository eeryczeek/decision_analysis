import random
from player import Player


class BotV1(Player):

    def __init__(self, name):
        super().__init__(name)
        self.seen_cards = set()
        self.owned_cards = set()

    def putCard(self, declared_card):
        self.owned_cards = set(self.cards) | self.owned_cards
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"

        valid_cards = self.cards if declared_card is None else [
            card for card in self.cards if card[0] >= declared_card[0]]

        if valid_cards:
            valid_cards = sorted(valid_cards, key=lambda x: x[0])
            return valid_cards[0], valid_cards[0]
        else:
            true_card = random.choice(self.cards)
        if declared_card is not None and true_card[0] < declared_card[0]:
            random_card = (min(declared_card[0]+1, 14), true_card[1])
        return true_card, random_card

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.owned_cards:
            return True
        return False

    def __str__(self):
        return "ZdjeciePdfa"

    def __repr__(self):
        return "ZdjeciePdfa"
