import numpy as np
from player import Player

class MichalKalmucki_DominikLudwiczak(Player):

    def __init__(self, name):
        super().__init__(name)
        self.my_used_cards = dict()
    
    def putCard(self, declared_card):
        if declared_card is None:
            lowest = min(self.cards, key=lambda x: x[0])
            self.use_card(lowest)
            return lowest, lowest
        
        lowest_acceptable = min([card for card in self.cards if card[0] >= declared_card[0]], key=lambda x: x[0], default=None)

        if len(self.cards) == 1 and lowest_acceptable is None:
            return "draw"

        if lowest_acceptable is None:
            highest = min(self.cards, key=lambda x: x[0])
            self.use_card(highest)
            return highest, (declared_card[0], (declared_card[1] + 1) % 4)
        else:
            self.use_card(lowest_acceptable)
            return lowest_acceptable, lowest_acceptable
    
    def use_card(self, card):
        if card in self.my_used_cards:
            self.my_used_cards[card] += 1
        else:
            self.my_used_cards[card] = 1
    
    def checkCard(self, opponent_declaration):
        used_cards = self.my_used_cards.copy()
        if opponent_declaration in used_cards:
            used_cards[opponent_declaration] += 1
        else:
            used_cards[opponent_declaration] = 1
        if any([card for card in used_cards if used_cards[card] >= 4]):
            return True
        return False
    