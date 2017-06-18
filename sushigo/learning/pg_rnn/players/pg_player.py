import uuid
import random
from sushigo.player import Player
import numpy as np
from collections import OrderedDict  #https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists
from sushigo.learning.pg_rnn.policies.rnn_policy import select_action
from sushigo.deck import StandardDeck


class Pg_player(Player):
    def __init__(self, policy, name="simple_player", deck=None):
        super(Pg_player, self).__init__()
        self.policy = policy
        self.name = name
        self.prev_reward = None

        self.deck = deck if deck else StandardDeck()
        self.cards = list(set([str(_) for _ in self.deck]))

        self.num_cards = len(self.cards)
        self.cards_idx = {card:i for i,card in enumerate(self.cards)}
        return

    def act(self, reward, observation=None, action_space=None):
        self.append_reward(int(reward))
        state = self.obs_to_state(observation)
        allowed_actions = self.action_vec(action_space)
        action = select_action(state=state,policy=self.policy,allowed=allowed_actions)
        card = self.cards[action]
        for action_card in action_space:
            if str(action_card) == card:
                return action_card
        raise RuntimeError('Player %s picked card %s that is not in his actionspace'%(self.name,card))

    def obs_to_state(self,obs):
        state_hand = [0]*self.num_cards
        for card in obs['hand']:
            state_hand[self.cards_idx[str(card)]] += 1
        state_table = [0]*self.num_cards
        for card in obs['table'][self.name]:
            state_table[self.cards_idx[str(card)]] += 1
        return state_hand + state_table

    def action_vec(self, action_space):
        actions = [0]*self.num_cards
        for card in action_space:
            actions[self.cards_idx[str(card)]] += 1
        actions = list(map(lambda x: min(x,1), actions))
        return actions

    def append_reward(self,reward):
        if self.prev_reward is not None:
            self.policy.rewards.append(reward-self.prev_reward)
        self.prev_reward = reward
