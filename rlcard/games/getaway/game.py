'''
Game Class for Get Away
'''
from copy import deepcopy
import random
from rlcard.games.getaway.dealer import GetAwayDealer
from rlcard.games.getaway.card import Suit,GetAwayCard
from rlcard.games.getaway.round import GetAwayRound
from rlcard.games.getaway.player import GetAwayPlayer

ACE_OF_SPADES = GetAwayCard(Suit.S, "A")
class GetAwayGame():
    ''' Game environment
    '''

    def __init__(self):
        self.players = []
        self.waste_pile = []
        self.winners = dict()
        self.num_players = 0
        self.round_counter = 0
        self.payoffs = [-1 for _ in range(self.num_players)]
        self.allow_step_back = False

    def configure(self, game_config):
        ''' Specifiy some game specific parameters, such as number of players
        '''
        self.num_players = game_config['game_num_players']
    def init_game(self):
        ''' Start game after adding players
        '''
        GetAwayPlayer.playerCount = 0
        self.num_players = len(self.players)
        self.payoffs = [-1 for _ in range(self.num_players)]
        dealer = GetAwayDealer()
        dealer.deal_cards(self.players)
        self.round_counter = 0
        self.current_player_id = self.starting_player()
        GetAwayRound.round_number = 0
        self.round = GetAwayRound(self.players[self.current_player_id], self)

        # Save the hisory for stepping back to the last state.
        self.history = []

        player_id = self.round.current_player.get_player_id()
        state = self.get_state(player_id)

        return state, player_id
        # return self.get_state(), self.current_player_id

    def add_player(self, player):
        ''' Adds player to game
        '''
        self.players.append(player)

    def get_next_player(self, current_player):
        ''' Get next player
        '''
        first_id = current_player.get_player_id()
        next_id = (first_id + 1) % self.num_players
        while first_id != next_id:
            if self.players[next_id].alive:
                return self.players[next_id]
            next_id = (next_id + 1) % self.num_players
        return None

    def print_state(self):
        ''' Prints current state
        '''
        print("State at round : ", self.round_counter)
        for player in self.players:
            player.print_cards()
        print("Waste pile:")
        print(self.waste_pile)
        print("End of current state description")

    def starting_player(self):
        ''' Find the player who starts
        '''
        print("Finding player with Ace of spades")
        for player in self.players:
            if ACE_OF_SPADES in player.hand:
                return player.player_id

    def next_round(self, leading_player, verbose=False):
        ''' General round
        '''
        if self.num_players - 1 == len(self.winners):
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
            leading_player = self.starting_player()
            leading_suit = Suit.S
        else:
            first_round = False
            leading_suit = None
        future_leader = tuple()
        for i in range(self.num_players):
            player_id = (i + leading_player) % self.num_players
            if verbose:
                print("Turn: Player ", player_id)
            current_player = self.players[player_id]
            if current_player.no_cards():
                if not trick and player_id not in self.winners:
                # if not trick and player_id not in self.winners:
                    draw_size = len(self.waste_pile) - 1
                    # draw_size = len(self.waste_pile) - (self.num_players - len(self.winners))
                    random_index = random.randrange(draw_size)
                    current_player.add_card(self.waste_pile.pop(random_index))
                else:
                    if verbose:
                        print("This player has already won.")
                    self.winners[player_id] = self.winners.get(player_id, self.round_counter)
                    continue
            card_played = current_player.next_round(leading_suit, first=first_round)
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

    def get_num_players(self):
        ''' Return the number of players in Limit Texas Hold'em

        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''

        return self.round.get_legal_actions(self.players, self.round.current_player.get_player_id())

    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        winner = self.round.winner
        if winner is not None and len(winner) > 0:
            for player in winner.keys():
                self.payoffs[player] = 1
        return self.payoffs
    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        state = self.round.get_state(self.players, player_id)
        state['num_players'] = self.get_num_players()
        state['current_player'] = self.round.current_player
        return state
    def step(self, action):
        ''' Take one step
        '''
        if self.allow_step_back:
            # First snapshot the current state
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_players, his_round))
        next_player = self.round.step(action)
        if self.round.done:
            self.round = GetAwayRound(self.players[next_player], self)
        return self.get_state(next_player), next_player

    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if not self.history:
            return False
        self.players, self.round = self.history.pop()
        return True
    @staticmethod
    def get_num_actions():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 61 actions
        '''
        return 53

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        return self.round.done