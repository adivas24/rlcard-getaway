'''
Player class for Get Away
'''

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

    def get_player_cards(self):
        ''' Getter method for player cards
        '''
        return self.hand

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

    def get_state(self, pubilc_cards, legal_actions):
        ''' Returns current player state.
        '''
        return {
            "hand": [c.get_index() for c in self.hand],
            "public_cards": [c.get_index() for c in pubilc_cards],
            "legal_actions": legal_actions
        }
