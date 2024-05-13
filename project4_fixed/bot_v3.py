import random
from player import Player


class BotV3(Player):
    def __init__(self, name):
        super().__init__(name)
        self.pile = []
        self.cards_in_game = set()
        self.cheat_probability = 1
        self.cheat_probability_decrease = 0.5

    def putCard(self, declared_card):
        self.cards_in_game.update(self.cards)
        sorted_cards = sorted(self.cards)
        if declared_card is None:
            self.pile.append((sorted_cards[0], sorted_cards[0]))
            return sorted_cards[0], sorted_cards[0]

        self.pile.append(('?', declared_card))
        if len(self.cards) == 1 and self.cards[0][0] < declared_card[0]:
            return "draw"

        cheat = False
        if random.random() < self.cheat_probability:
            self.cheat_probability *= self.cheat_probability_decrease
            cheat = True

        valid_cards = list(
            filter(lambda card: card[0] >= declared_card[0], sorted_cards))
        all_games_valid_cards = list(
            filter(lambda card: card[0] >= declared_card[0], sorted(self.cards_in_game)))

        if len(valid_cards) > 0:
            self.pile.append((valid_cards[0], valid_cards[0]))
            return (sorted_cards[0], valid_cards[0]) if cheat else (valid_cards[0], valid_cards[0])

        if len(all_games_valid_cards) > 0:
            self.pile.append(
                (all_games_valid_cards[0], all_games_valid_cards[0]))
            return sorted_cards[0], all_games_valid_cards[0]

        random_card = (random.randint(
            declared_card[0], 14), random.randint(0, 4))
        return sorted_cards[0], random_card

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
        self.opponent_cards = [('?', '?') for card in cards]

    def __str__(self):
        return "eryk"

    def __repr__(self):
        return "eryk"
