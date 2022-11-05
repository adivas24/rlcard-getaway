'''
Card class for Getaway
'''
from enum import Enum

class Suit(Enum):
    ''' Defines a suit.
    '''
    C = 0
    D = 1
    H = 2
    S = 3

ranks = {
    "A":14,"K":13,"Q":12,"J":11,"T":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2
}

class GetAwayCard():
    ''' Defines a card
    '''
    def __init__(self, suit, rank):
        assert isinstance(suit, Suit) and rank in ranks
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return self.suit.name + self.rank

    def __eq__(self, other):
        return (self.suit == other.suit) and (self.rank == other.rank)

    def __hash__(self) -> int:
        return self.suit.value*13 + ranks[self.rank]-2

    def __lt__(self, other):
        assert self.suit == other.suit
        return ranks[self.rank] < ranks[other.rank]

    def __le__(self, other):
        assert self.suit == other.suit
        return ranks[self.rank] <= ranks[other.rank]

    def __gt__(self, other):
        assert self.suit == other.suit
        return ranks[self.rank] > ranks[other.rank]

    def __ge__(self, other):
        assert self.suit == other.suit
        return ranks[self.rank] >= ranks[other.rank]

    def __ne__(self, other):
        return self.suit != other.suit or self.rank != other.rank

    def is_suit(self, suit):
        '''Does this card belong to this suit?
        '''
        return self.suit is suit

ACE_OF_SPADES = GetAwayCard(Suit.S, "A")
