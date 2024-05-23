from player import Player
from copy import copy


class PlayerModel:
    def __init__(self, no_cards: int, cards: list[tuple[int, int]] = [], cards_in_game: set = set(), pile: list = []):
        self.no_cards = no_cards
        self.cards = cards
        self.cards_in_game = cards_in_game
        self.pile = pile
        self.checks_probabilities = {True: 0.5, False: 0.5}
        self.checks_no = 0
        self.actions_no = 0

    def update_checks_probabilities(self):
        self.checks_probabilities[True] = (self.checks_no) / (self.actions_no)
        self.checks_probabilities[False] = (
            self.actions_no - self.checks_no) / (self.actions_no)

    def __copy__(self):
        return PlayerModel(
            self.no_cards,
            [tuple(card) for card in self.cards],
            {tuple(card) for card in self.cards_in_game},
            [[tuple(declaration[0]), tuple(declaration[1])]
             for declaration in self.pile]
        )

    def __str__(self):
        return f"pile: {self.pile}, no_cards: {self.no_cards}, cards ({len(self.cards)}): {self.cards} cards_in_game ({len(self.cards_in_game)}): {self.cards_in_game}"


class ErykPtaszynski_ErykWalter(Player):
    def simulate_one_turn(self, player: PlayerModel, opponent: PlayerModel, move: tuple, decision: bool):
        player.pile.append(move)
        opponent.pile.append(('?', move[1]))
        player.no_cards -= 1
        if decision and move[0] != move[1]:
            playerToTake = player.pile[max([-3, -len(player.pile)]):]
            player.cards += [card[0]
                             for card in playerToTake if card[0] != ('?', '?')]
            player.no_cards += len(playerToTake)
            opponent.cards_in_game.add(move[0])
            return player, opponent

        if decision and move[0] == move[1]:
            playerToTake = player.pile[max([-3, -len(player.pile)]):]
            opponent.no_cards += len(playerToTake)
            opponent.cards_in_game.update(
                [card[0] for card in playerToTake if card[0] != ('?', '?')])
            return player, opponent
        return player, opponent

    def function_to_minimize(self, player: PlayerModel, opponent: PlayerModel) -> int:
        return player.no_cards - opponent.no_cards + sum([14 - card[0] for card in player.cards]) / 4

    def rank_position(self, move):
        for decision in [True, False]:
            player_after_sim, opponent_after_sim = self.simulate_one_turn(
                copy(self.player), copy(self.opponent), move, decision)
            yield self.function_to_minimize(player_after_sim, opponent_after_sim) * self.player.checks_probabilities[decision]

    def get_all_possible_moves(self, declared_card) -> dict:
        if declared_card is None:
            all_possible_cards = [(number, color)
                                  for color in range(4) for number in range(9, 15)]
        else:
            all_possible_cards = [(number, color)
                                  for color in range(4) for number in range(declared_card[0], 15)]
        return {(x, y): max(self.rank_position((x, y))) for x in self.cards for y in all_possible_cards}

    def putCard(self, declared_card):
        self.player.cards_in_game.update(self.cards)
        self.player.cards = sorted(self.cards)
        self.player.no_cards = len(self.cards)

        if declared_card is None:
            self.player.pile.append(
                (self.player.cards[0], self.player.cards[0]))
            self.player.no_cards -= 1
            return self.player.cards[0], self.player.cards[0]

        self.player.pile.append((('?', '?'), declared_card))
        self.opponent.no_cards -= 1
        self.opponent.actions_no += 1
        self.opponent.update_checks_probabilities()

        if len(self.cards) == 1 and self.cards[0][0] < declared_card[0]:
            return "draw"

        best_move = min(self.get_all_possible_moves(
            declared_card).items(), key=lambda x: x[1])[0]
        return best_move

    def checkCard(self, opponent_declaration: tuple) -> bool:
        opponent_declaration = tuple(opponent_declaration)
        if all([card[0] < opponent_declaration[0] for card in self.cards]):
            return True
        if len(self.player.cards_in_game) >= 12:
            return opponent_declaration in self.cards or (opponent_declaration, opponent_declaration) in self.player.pile or opponent_declaration not in self.player.cards_in_game
        return opponent_declaration in self.cards or (opponent_declaration, opponent_declaration) in self.player.pile

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if not checked:
            return

        self.removed_player_cards = [
            card[0] for card in self.player.pile[-noTakenCards:] if card[0] != ('?', '?')]
        self.player.pile = self.player.pile[:-noTakenCards]

        if iChecked and iDrewCards:
            self.player.cards_in_game.add(revealedCard)
            self.opponent.cards_in_game.add(revealedCard)
            self.opponent.no_cards -= 1
            self.opponent.actions_no += 1
        if iChecked and not iDrewCards:
            self.player.cards_in_game.add(revealedCard)
            self.opponent.cards_in_game.add(revealedCard)
            self.opponent.no_cards -= 1
            self.opponent.actions_no += 1
            self.opponent.no_cards += noTakenCards
        if not iChecked and iDrewCards:
            self.opponent.checks_no += 1
        if not iChecked and not iDrewCards:
            self.opponent.checks_no += 1
            self.opponent.no_cards += noTakenCards

    def startGame(self, cards):
        super().startGame(cards)
        self.player = PlayerModel(len(self.cards), [], set(), [])
        self.opponent = PlayerModel(len(self.cards), [], set(), [])
