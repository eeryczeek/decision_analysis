import numpy as np
from player import Player

class Eliza_Weronika(Player):

    found_cards = []
    
    ### player's random strategy
    def putCard(self, declared_card):

        # update found cards
        for card in self.cards:
            if card not in self.found_cards:
                self.found_cards.append(card)

        lowest_card = min(self.cards, key = lambda x: x[0])
        highest_card = max(self.cards, key = lambda x: x[0])
        if declared_card is None:
            # if no cards on the table, put lowest card and call highest card
            return lowest_card, highest_card
        
        # if there are cards on the table, put the lowest card higher than the declared card
        correct_card = None
        for card in self.cards:
            if card[0] >= declared_card[0]:
                if correct_card is None or card[0] < correct_card[0]:
                    correct_card = card
        
        if correct_card is not None:
            return correct_card, correct_card
        
        # if on last card
        if len(self.cards) == 1 and correct_card is None:
            return "draw"
        
        #temporary
        if declared_card[1] !=3:
            alt = (declared_card[0], declared_card[1] + 1)
        else: 
            alt = (declared_card[0], 0)
        return lowest_card, alt




    ### randomly decides whether to check or not
    def checkCard(self, opponent_declaration):
        #print(self.found_cards)
        if opponent_declaration in self.cards:
            return True
        if len(self.found_cards) >= 12 and opponent_declaration not in self.found_cards:
            return True
        if len(self.cards) == 1 and opponent_declaration[0] > self.cards[0][0]:
            return True
        
        repeats = 0
        for card in self.found_cards:
            if card[0] == opponent_declaration[0] and card != opponent_declaration:
                repeats += 1
        if repeats > 2:
            return True

        return False
    

