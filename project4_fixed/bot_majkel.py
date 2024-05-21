import random
from player import Player


class BotMajkel(Player):

    def putCard(self, declared_card):
        highest = max(self.cards, key=lambda x: x[0])
        lowest = min(self.cards, key=lambda x: x[0])
        
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"
        
        if not declared_card or highest[0] > declared_card[0]:
            return highest, highest
        
        return lowest, (declared_card[0], (declared_card[1] + 1) % 4)
        

    def checkCard(self, opponent_declaration):
        return True