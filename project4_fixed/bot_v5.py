import random

from player import Player


class PlayerModel:
    def __init__(self, no_cards: int):
        self.pile = []
        self.no_cards = no_cards
        self.cards_in_game = set()

    def __str__(self):
        return f"pile: {self.pile}, no_cards: {self.no_cards}, cards_in_game: {self.cards_in_game}"

    def __repr__(self):
        return self.__str__()


class CostFunction:
    def __init__(self, player: PlayerModel, opponent: PlayerModel):
        self.player = player
        self.opponent = opponent
        self.cost = 0

    def __call__(self,) -> int:
        return self.player.no_cards - len(self.player.cards_in_game) - self.opponent.no_cards + len(self.opponent.cards_in_game)

    def __str__(self):
        return f"cost: {self.cost}, player: {self.player}, opponent: {self.opponent}"

    def __repr__(self):
        return self.__str__()


class BotV5(Player):
    def __init__(self, name):
        super().__init__(name)
        self.last_played_card = None

    def putCard(self, declared_card):
        self.player.cards_in_game.update(self.cards)
        self.player.no_cards = len(self.cards)

        sorted_cards = sorted(self.cards)

        if declared_card is None:
            self.player.pile.append((sorted_cards[0], sorted_cards[0]))
            self.opponent.pile.append(('?', sorted_cards[0]))
            self.player.no_cards -= 1
            self.last_played_card = sorted_cards[0]
            return sorted_cards[0], sorted_cards[0]

        self.player.pile.append(('?', declared_card))
        self.opponent.pile.append(('?', declared_card))
        self.opponent.no_cards -= 1

        if len(self.cards) == 1 and self.cards[0][0] < declared_card[0]:
            self.last_played_card = None
            return "draw"

        valid_cards = [
            card for card in sorted_cards if card[0] >= declared_card[0]]
        if len(valid_cards) > 0:
            self.player.pile.append((valid_cards[0], valid_cards[0]))
            self.opponent.pile.append(('?', valid_cards[0]))
            self.last_played_card = valid_cards[0]
            return valid_cards[0], valid_cards[0]

        all_games_valid_cards = [
            card for card in self.player.cards_in_game if card[0] >= declared_card[0]]
        if len(all_games_valid_cards) > 0:
            self.player.pile.append(
                (all_games_valid_cards[0], all_games_valid_cards[-1]))
            self.opponent.pile.append(
                ('?', all_games_valid_cards[-1]))
            self.last_played_card = sorted_cards[0]
            return sorted_cards[0], all_games_valid_cards[0]

        random_card = (random.randint(
            declared_card[0], 14), random.randint(0, 4))
        self.player.pile.append((sorted_cards[0], random_card))
        self.opponent.pile.append(('?', random_card))
        self.last_played_card = sorted_cards[0]
        return sorted_cards[0], random_card

    def checkCard(self, opponent_declaration):
        if all([card[0] < opponent_declaration[0] for card in self.cards]) or (self.opponent.no_cards <= 2 and self.opponent.no_cards < self.player.no_cards):
            return True
        if len(self.player.cards_in_game) >= 14:
            return opponent_declaration in self.cards or (opponent_declaration, opponent_declaration) in self.player.pile or opponent_declaration not in self.player.cards_in_game
        return opponent_declaration in self.cards or (opponent_declaration, opponent_declaration) in self.player.pile

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if not checked:
            self.removed_cards = None
            return

        self.removed_player_cards = [
            card[0] for card in self.player.pile[-noTakenCards:] if card[0] != '?']
        self.player.pile = self.player.pile[:-noTakenCards]
        self.removed_opponent_cards = [
            card[0] for card in self.opponent.pile[-noTakenCards:] if card[0] != '?']
        self.opponent.pile = self.opponent.pile[:-noTakenCards]

        if iChecked and iDrewCards:
            self.player.cards_in_game.add(revealedCard)
            self.opponent.cards_in_game.add(revealedCard)
            self.opponent.no_cards -= 1
        if iChecked and not iDrewCards:
            self.player.cards_in_game.add(revealedCard)
            self.opponent.cards_in_game.add(revealedCard)
            self.opponent.no_cards -= 1
            self.opponent.no_cards += noTakenCards
        if not iChecked and iDrewCards:
            self.opponent.cards_in_game.update(
                card[0] for card in self.opponent.pile[-noTakenCards:] if card[0] != '?')
        if not iChecked and not iDrewCards:
            self.opponent.cards_in_game.update(
                card[0] for card in self.opponent.pile[-noTakenCards:] if card[0] != '?')
            self.opponent.no_cards += noTakenCards

    def startGame(self, cards):
        super().startGame(cards)
        self.player = PlayerModel(len(self.cards))
        self.opponent = PlayerModel(len(self.cards))
