import random
from player import Player


class OponentModel:
    def __init__(self):
        self.bleff_probability = None
        self.cards = set()
        self.cards_in_game = set()
        self.actions = 0
        self.bleffs = 0

    def update(self, pile):
        self.cards.update(pile)


class ErykPtaszynski_ErykWalter(Player):
    def __init__(self, name):
        super().__init__(name)
        self.last_hand = []
        self.pile = []
        self.cards_in_game = set()
        self.oponent = OponentModel()

    def putCard(self, declared_card):
        self.cards_in_game.update(self.cards)
        sorted_cards = sorted(self.cards)
        if self.removed_cards is not None:
            self.cards_in_game.update(self.removed_cards)
            self.removed_cards = None
        added_cards = list(
            card for card in self.cards if card not in self.last_hand)

        self.oponent.update(added_cards)

        if declared_card is None:
            self.pile.append((sorted_cards[0], sorted_cards[0]))
            return sorted_cards[0], sorted_cards[0]

        self.pile.append(('?', declared_card))
        if len(self.cards) == 1 and self.cards[0][0] < declared_card[0]:
            return "draw"

        valid_cards = list(
            filter(lambda card: card[0] >= declared_card[0], sorted_cards))
        all_games_valid_cards = list(
            filter(lambda card: card[0] >= declared_card[0], sorted(self.cards_in_game)))

        if len(valid_cards) > 0:
            self.pile.append((valid_cards[0], valid_cards[0]))
            return valid_cards[0], valid_cards[0]
        if len(all_games_valid_cards) > 0:
            self.pile.append(
                (all_games_valid_cards[0], all_games_valid_cards[0]))
            return sorted_cards[0], all_games_valid_cards[0]

        random_card = (random.randint(
            declared_card[0], 14), random.randint(0, 4))
        return sorted_cards[0], random_card

    def checkCard(self, opponent_declaration):
        if len(self.cards) == 1 and self.cards[0][0] < opponent_declaration[0]:
            return True
        if len(self.cards_in_game) >= 14:
            return opponent_declaration in self.cards or (opponent_declaration, opponent_declaration) in self.pile or opponent_declaration not in self.cards_in_game
        return opponent_declaration in self.cards or (opponent_declaration, opponent_declaration) in self.pile

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if not checked:
            self.removed_cards = None
            return
        self.removed_cards = self.pile[-noTakenCards:]
        self.pile = self.pile[:-noTakenCards]
        if iChecked and iDrewCards:
            self.cards_in_game.difference_update(self.cards)
            self.cards_in_game.add(revealedCard)

    def startGame(self, cards):
        super().startGame(cards)
        self.oponent.cards = {('?', '?') for _ in self.cards}
