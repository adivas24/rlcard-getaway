'''
 Environment for Get Away
'''

from collections import OrderedDict
import numpy as np

from rlcard.envs import Env
from rlcard.games.getaway import Game
from rlcard.games.getaway.utils import ACTION_SPACE, ACTION_LIST
from rlcard.games.getaway.utils import encode_hand, encode_target, card_from_index

DEFAULT_GAME_CONFIG = {
    'game_num_players': 4,
}

class GetAwayEnv(Env):
    ''' Get Away Game Environment
    '''
    def __init__(self, config):
        self.name = 'getaway'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.state_shape = [[3,4,13] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state):
        obs = np.zeros((3, 4, 13), dtype=int)
        encode_hand(obs[:2], state['hand'])
        encode_target(obs[2], state['target'])
        legal_action_id = self._get_legal_actions()
        extracted_state = {'obs': obs, 'legal_actions': legal_action_id}
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        extracted_state['action_record'] = self.action_recorder
        return extracted_state

    def get_payoffs(self):

        return np.array(self.game.get_payoffs())

    def _decode_action(self, action_id):
        if action_id == 52:
            return "draw"
        else:
            return str(card_from_index(action_id))
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]
        # if (len(self.game.dealer.deck) + len(self.game.round.played_cards)) > 17:
        #    return ACTION_LIST[60]
        return ACTION_LIST[np.random.choice(legal_ids)]

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        legal_ids = {ACTION_SPACE[action]: None for action in legal_actions}
        return OrderedDict(legal_ids)

    def get_perfect_information(self):
        ''' Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['num_players'] = self.num_players
        state['hand_cards'] = [player.hand
                               for player in self.game.players]
        state['played_cards'] = self.game.waste_pile
        state['target'] = self.game.round.trick
        state['current_player'] = self.game.round.current_player
        state['legal_actions'] = self.game.round.get_legal_actions(
            self.game.players, state['current_player'])
        return state

    def is_over(self):
        return len(self.game.winners) == self.game.num_players-1
