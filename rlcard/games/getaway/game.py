'''
Game Class for Get Away
'''

import random
from dealer import GetAwayDealer
from card import Suit

class GetAwayGame():
    ''' Game environment
    '''
    def __init__(self):
        self.players = []
        self.waste_pile = []
        self.winners = dict()
        self.num_players = 0
        self.round_counter = 0

    def init_game(self):
        ''' Start game after adding players
        '''
        self.num_players = len(self.players)
        dealer = GetAwayDealer()
        dealer.deal_cards(self.players)
        self.round_counter = 0

    def add_player(self, player):
        ''' Adds player to game
        '''
        self.players.append(player)

    def print_state(self):
        ''' Prints current state
        '''
        print("State at round : ", self.round_counter)
        for player in self.players:
            player.print_cards()
        print("Waste pile:")
        print(self.waste_pile)
        print("End of current state description")

    def next_round(self, leading_player, verbose = False):
        ''' General round
        '''
        if self.num_players-1 == len(self.winners):
            if verbose:
                print("Game has concluded")
            return -1
        self.round_counter += 1
        if verbose:
            print("Beginning play for round: ", self.round_counter)
        trick = []
        next_round_leader = None
        if self.round_counter == 1:
            first_round = True
            leading_player = 0
            leading_suit = Suit.S
        else:
            first_round = False
            leading_suit = None
        future_leader = tuple()
        for i in range(self.num_players):
            player_id = (i+leading_player)% self.num_players
            if verbose:
                print("Turn: Player ", player_id)
            current_player = self.players[player_id]
            if current_player.no_cards():
                if not trick and player_id not in self.winners:
                    draw_size = len(self.waste_pile)-(self.num_players-len(self.winners))
                    random_index = random.randrange(draw_size)
                    current_player.add_card(self.waste_pile.pop(random_index))
                else:
                    if verbose:
                        print("This player has already won.")
                    self.winners[player_id] = self.winners.get(player_id, self.round_counter)
                    continue
            card_played = current_player.next_round(leading_suit, first = first_round)
            if verbose:
                print("Player ", player_id, "played card: ", str(card_played))
            action = tuple([player_id, card_played])
            trick.append(card_played)
            if leading_suit is None or future_leader == tuple():
                leading_suit = card_played.suit
                future_leader = action
            elif leading_suit == card_played.suit:
                if future_leader[1] < card_played:
                    future_leader = action
            else:
                if not first_round:
                    self.players[future_leader[0]].add_cards(trick)
                    return future_leader[0]
            next_round_leader = future_leader[0]
        self.waste_pile += trick
        return next_round_leader
