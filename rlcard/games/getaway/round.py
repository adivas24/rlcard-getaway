'''
Get Away Round
'''

from rlcard.games.getaway.card import Suit
from rlcard.games.getaway.utils import action2card


class GetAwayRound():
    ''' Round class for Get Away
    '''
    round_number = 0

    def __init__(self, leading_player, game):
        self.trick = []
        GetAwayRound.round_number += 1
        self.current_player = leading_player
        self.leading_player = leading_player
        self.next_leading_player_card = None
        self.leading_suit = None
        self.game = game
        self.done = False

    def step(self, action):
        ''' Takes one step in the round
        '''
        first_round = False
        if GetAwayRound.round_number == 1:
            first_round = True
            self.leading_suit = Suit.S
        if action == "draw":
            draw_size = len(self.game.waste_pile) - 1
            random_index = self.game.random.randrange(draw_size)
            card_played = self.game.waste_pile.pop(random_index)
        else:
            card_played = action2card(action)
            self.current_player.hand.remove(card_played)

        self.trick.append(card_played)
        if self.leading_suit is None or self.next_leading_player_card is None:
            self.leading_suit = card_played.suit
            self.next_leading_player_card = (self.current_player, card_played)
        elif self.leading_suit == card_played.suit:
            if self.next_leading_player_card[1] < card_played:
                self.next_leading_player_card = (self.current_player, card_played)
        else:
            if not first_round:
                self.next_leading_player_card[0].add_cards(self.trick)
                self.trick = []
                self.end_trick()
                return self.next_leading_player_card[0].get_player_id()
        next_player = self.game.get_next_player(self.current_player)
        self.current_player = next_player
        if next_player == self.leading_player:
            self.end_trick()
        return next_player.get_player_id()

    def add_winner(self, player_id):
        ''' Marks player as winner
        '''
        self.game.winners[player_id] = GetAwayRound.round_number

    def end_trick(self):
        ''' Ends the trick
        '''
        for player in self.game.players:
            if player.no_cards():
                if player != self.leading_player:
                    self.current_player.alive = False
                    self.add_winner(self.current_player.get_player_id())
        self.game.waste_pile += self.trick
        self.trick = []
        self.current_player = None
        self.leading_suit = None
        self.done = True

    def get_legal_actions(self, players, player_id):
        ''' Gets legal actions for the player
        '''
        legal_actions = []
        hand = players[player_id].hand
        if GetAwayRound.round_number == 1:
            actions = [str(card) for card in hand if card.suit == Suit.S]
            if not actions:
                legal_actions = [str(c) for c in hand]
            else:
                legal_actions = actions
        else:
            if self.leading_suit is None:
                actions = [str(c) for c in hand]
            else:
                actions = [str(card) for card in hand if card.suit == self.leading_suit]

            if not actions:
                legal_actions = [str(c) for c in hand]
            else:
                legal_actions = actions

            if legal_actions == []:
                return ["draw"]

        return legal_actions

    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players (list): The list of UnoPlayer
            player_id (int): The id of the player
        '''
        # print("Get state", player_id)
        state = {}
        player = players[player_id]
        state['hand'] = player.hand
        state['target'] = self.trick
        state['played_cards'] = self.game.waste_pile
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        state['num_cards'] = []
        for player in players:
            state['num_cards'].append(len(player.hand))
        return state
