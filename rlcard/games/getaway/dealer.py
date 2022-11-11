'''
Dealer class for Get Away
'''
import random
from rlcard.games.getaway.card import Suit, GetAwayCard, ranks

class GetAwayDealer():
    ''' Defines dealing methods
    '''
    def __init__(self):
        self.deck = []
        for suit in Suit.__members__.values():
            for rank in ranks:
                self.deck.append(GetAwayCard(suit, rank))

    def shuffle_cards(self):
        ''' Shuffles cards
        '''
        random.shuffle(self.deck)

    def deal_cards(self, players):
        ''' Deals all cards to players
        '''
        num_players = len(players)
        self.shuffle_cards()
        player_idx = 0
        while len(self.deck) > 0:
            players[player_idx].add_card(self.deck.pop())
            player_idx = (player_idx+1) % num_players
