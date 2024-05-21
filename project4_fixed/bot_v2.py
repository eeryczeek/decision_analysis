import random
from player import Player


class BotV2(Player):
    def __init__(self, name):
        super().__init__(name)
        self.pile = []
        self.cards_in_game = set()
        self.first_draw = True

    def putCard(self, declared_card):
        lowest = min(self.cards, key=lambda x: x[0])
        highest = max(self.cards, key=lambda x: x[0])

        # if len(self.pile) >= 3 and self.first_draw:
        #     self.first_draw = False
        #     return "draw"

        self.cards_in_game.update(self.cards)
        sorted_cards = sorted(self.cards)
        if declared_card is None:
            self.pile.append((lowest, lowest))
            return lowest, lowest

        hand_valid_cards = list(
            filter(lambda card: card[0] >= declared_card[0], sorted_cards))

        self.pile.append(('?', declared_card))
        if len(self.cards) == 1 and self.cards[0][0] < declared_card[0]:
            return "draw"

        if len(hand_valid_cards) > 0:
            self.pile.append((hand_valid_cards[-1], hand_valid_cards[-1]))
            return (hand_valid_cards[-1], hand_valid_cards[-1])

        if random.random() < 0.5:
            return highest, (random.randint(declared_card[0], 14), random.randint(0, 4))

        return "draw"

    def checkCard(self, opponent_declaration):
        if len(self.cards_in_game) >= 12:
            opponent_declaration in self.cards or (
                opponent_declaration, opponent_declaration) in self.pile or opponent_declaration not in self.cards_in_game
        return opponent_declaration in self.cards or (opponent_declaration, opponent_declaration) in self.pile

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if not checked:
            return
        self.pile[:-noTakenCards]
        if iChecked and iDrewCards:
            self.cards_in_game.difference_update(self.cards)
            self.cards_in_game.add(revealedCard)

    def startGame(self, cards):
        super().startGame(cards)
        self.opponent_cards = [('?', '?') for _ in cards]
