'''
Get Away Round
'''

class GetAwayRound():
    ''' Round class for Get Away
    '''
    round_number = 0
    def __init__(self, leading_player):
        self.trick = []
        GetAwayRound.round_number += 1
        self.leading_player = leading_player
        self.current_player = leading_player
        self.next_leading_player = None
        self.leading_suit = None

        def step(self, action):
            if GetAwayRound.round_number == 1:
                first_round = True
            leading_suit = action2card(action).suit

    # def next_round(self, leading_player, verbose=False):
    #     ''' General round
    #     '''

    #     next_round_leader = None
    #     if self.round_counter == 1:
    #         first_round = True
    #         leading_player = self.starting_player()
    #         leading_suit = Suit.S
    #     else:
    #         first_round = False
    #         leading_suit = None
    #     future_leader = tuple()
    #     for i in range(self.num_players):
    #         player_id = (i + leading_player) % self.num_players
    #         if verbose:
    #             print("Turn: Player ", player_id)
    #         current_player = self.players[player_id]
    #         if current_player.no_cards():
    #             if not trick and player_id not in self.winners:
    #             # if not trick and player_id not in self.winners:
    #                 draw_size = len(self.waste_pile) - 1
    #                 # draw_size = len(self.waste_pile) - (self.num_players - len(self.winners))
    #                 random_index = random.randrange(draw_size)
    #                 current_player.add_card(self.waste_pile.pop(random_index))
    #             else:
    #                 if verbose:
    #                     print("This player has already won.")
    #                 self.winners[player_id] = self.winners.get(player_id, self.round_counter)
    #                 continue
    #         card_played = current_player.next_round(leading_suit, first=first_round)
    #         if verbose:
    #             print("Player ", player_id, "played card: ", str(card_played))
    #         action = tuple([player_id, card_played])
    #         trick.append(card_played)
    #         if leading_suit is None or future_leader == tuple():
    #             leading_suit = card_played.suit
    #             future_leader = action
    #         elif leading_suit == card_played.suit:
    #             if future_leader[1] < card_played:
    #                 future_leader = action
    #         else:
    #             if not first_round:
    #                 self.players[future_leader[0]].add_cards(trick)
    #                 return future_leader[0]
    #         next_round_leader = future_leader[0]
    #     self.waste_pile += trick
    #     return next_round_leader