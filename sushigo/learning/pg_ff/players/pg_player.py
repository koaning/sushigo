import uuid
import random
from sushigo.player import Player
import numpy as np
from sushigo.deck import ALL_CARDTYPES
from collections import OrderedDict  #https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists
from sushigo.learning.pg_ff.policies.first_policy import select_action

NUM_CARDS = len(ALL_CARDTYPES)
CARDS_IDX = {card:i for i,card in enumerate(ALL_CARDTYPES)}

class Pg_player(Player):
    def __init__(self, policy, name="simple_player"):
        super(Pg_player, self).__init__()
        self.policy = policy
        self.name = name

        self.prev_reward = None

    def act(self, reward, observation=None, action_space=None):
        self.append_reward(reward)
        state = self.obs_to_state(observation)
        allowed_actions = self.action_vec(action_space)
        action = select_action(state=state,policy=self.policy,allowed=allowed_actions)
        card = ALL_CARDTYPES[action]
        return card

    def obs_to_state(self,obs):
        state_hand = [0]*NUM_CARDS
        for card in obs['hand']:
            state_hand[CARDS_IDX[card]] += 1
        state_table = [0]*NUM_CARDS
        for card in obs['table'][self.name]:
            state_table[CARDS_IDX[card.type]] += 1
        return state_hand + state_table

    def action_vec(self, action_space):
        actions = [0]*NUM_CARDS
        for card in action_space:
            actions[CARDS_IDX[card]] += 1
        actions = list(map(lambda x: min(x,1), actions))
        return actions

    def append_reward(self,reward):
        if self.prev_reward is not None:
            self.policy.rewards.append(reward-self.prev_reward)
        self.prev_reward = reward