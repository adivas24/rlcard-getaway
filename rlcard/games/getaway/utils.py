'''
Utilities for Get Away
'''
import numpy as np

from rlcard.games.getaway.card import Suit, GetAwayCard, ranks, rev_ranks

cards = [GetAwayCard(suit, rank) for suit in Suit.__members__.values() for rank in ranks]
ACTION_SPACE = {str(card):card.get_index() for card in cards}
ACTION_SPACE['draw'] = 52

ACTION_LIST = list(ACTION_SPACE.keys())

def card_from_index(index):
    ''' Fetches card from its index
    '''
    return GetAwayCard(Suit(index//13), rev_ranks[index%13 + 2])

def action2card(action):
    ''' Fetches card from action
    '''
    return card_from_index(ACTION_SPACE[action])

def hand2dict(hand):
    ''' Get the corresponding dict representation of hand

    Args:
        hand (list): list of string of hand's card

    Returns:
        (dict): dict of hand
    '''
    hand_dict = {}
    for card in hand:
        hand_dict[card] = hand_dict.get(card, 0)+1
    return hand_dict

def encode_hand(plane, hand):
    ''' Encode hand and represerve it into plane

    Args:
        plane (array): 3*4*15 numpy array
        hand (list): list of string of hand's card

    Returns:
        (array): 3*4*15 numpy array
    '''
    plane[0] = np.ones((4, 13), dtype=int)
    hand = hand2dict(hand)
    for card, count in hand.items():
        color = card.suit.value
        rank = ranks[card.rank]-2
        plane[0][color][rank] = 0
        plane[count][color][rank] = 1
    return plane

def encode_target(plane, target):
    ''' Encode target and represerve it into plane

    Args:
        plane (array): 1*4*15 numpy array
        target(str): string of target card

    Returns:
        (array): 1*4*15 numpy array
    '''
    target = hand2dict(target)

    for card in target:
        color = card.suit.value
        rank = ranks[card.rank]-2
        plane[color][rank] = 1
    return plane
