'''
Player class for Get Away
'''
import random
from card import ACE_OF_SPADES

class GetAwayPlayer():
    ''' Defines a player
    '''
    playerCount = 0

    def __init__(self, strategy = "random"):
        self.hand = set()
        self.player_id = GetAwayPlayer.playerCount
        GetAwayPlayer.playerCount += 1
        self.player_strategy = strategy
        self.alive = True

    def get_player_id(self):
        ''' Player id
        '''
        return self.player_id

    def add_card(self, card):
        ''' Add card to hand
        '''
        self.hand.add(card)

    def add_cards(self, cards):
        ''' Add cards to hand
        '''
        self.hand.update(cards)

    def print_cards(self):
        ''' Prints cards in hand
        '''
        print("Player number: ", self.player_id)
        print(self.hand)

    def no_cards(self):
        ''' Is the hand empty?
        '''
        return self.hand == set()

    def legal_cards(self, suit):
        ''' Which cards belong to this suit?
        '''
        return {c for c in self.hand if c.is_suit(suit)}

    def human_prompt(self, legal_cards):
        ''' Function to allow human to play
        '''
        while True:
            print("Possible options are:")
            for i,card in enumerate(legal_cards):
                print(i,card)
            chosen_idx = int(input("Please enter one of the above option numbers: "))
            if chosen_idx >= 0 and chosen_idx < len(legal_cards):
                return legal_cards[chosen_idx]

    # TODO: THIS NEEDS TO BE RELOCATED
    def strategy(self, state, legal_cards):
        ''' Playing strategy
        '''
        if state == "FIRST":
            if ACE_OF_SPADES in legal_cards:
                # Playing ace of spades in first round is compulsory.
                self.hand.remove(ACE_OF_SPADES)
                return ACE_OF_SPADES
        if self.player_strategy == "human":
            random_choice = self.human_prompt(list(legal_cards))
        else:
            random_choice = random.choice(list(legal_cards))
        self.hand.remove(random_choice)
        return random_choice

    def next_round(self, suit, first = False):
        ''' Card for subsequent rounds
        '''
        if first:
            state = "FIRST"
        else:
            state = None # This should contain state description later
        if suit is None:
            legal_card_set = self.hand
        else:
            legal_card_set = self.legal_cards(suit)
        if legal_card_set == set():
            legal_card_set = self.hand
        return self.strategy(state, legal_card_set)

    def get_state(self, pubilc_cards, legal_actions):
        ''' Returns current player state.
        '''
        return {
            "hand": [c.get_index() for c in self.hand],
            "public_cards": [c.get_index() for c in pubilc_cards],
            "legal_actions": legal_actions
        }