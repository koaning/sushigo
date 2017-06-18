import uuid
import random
from sushigo.player import Player
import numpy as np
from collections import OrderedDict  #https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists
from sushigo.deck import StandardDeck


class Simple_player(Player):
    def __init__(self,weights, name="simple_player", deck = None):
        super(Simple_player, self).__init__()
        self.deck = deck if deck else StandardDeck()
        self.cards = list(set([str(_) for _ in self.deck]))

        self.num_cards = len(self.cards)
        self.cards_idx = {card:i for i,card in enumerate(self.cards)}
        self.weights = {key:value for key,value in zip(self.cards,weights)}
        self.N_cards = len(weights)


    def act(self, reward, observation=None, action_space=None):
        state = self.obs_to_state(observation)
        actions = list(OrderedDict.fromkeys(action_space))
        distro = np.array([self.weights[str(action)] for action in actions],dtype=np.float32) + 1E-9
        distro = (distro)/float(np.sum(distro))

        idx = np.random.choice(len(distro),p=distro)
        return actions[idx]

    def obs_to_state(self,obs):
        state_hand = [0]*self.num_cards
        for card in obs['hand']:
            state_hand[self.cards_idx[card]] += 1
        state_table = [0]*self.num_cards
        for card in obs['table'][self.name]:
            state_table[self.cards_idx[str(card)]] += 1
        return state_hand + state_table
