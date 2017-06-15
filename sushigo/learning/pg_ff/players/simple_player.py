import uuid
import random
from sushigo.player import Player
import numpy as np
from sushigo.deck import ALL_CARDTYPES
from collections import OrderedDict  #https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists

NUM_CARDS = len(ALL_CARDTYPES)
CARDS_IDX = {card:i for i,card in enumerate(ALL_CARDTYPES)}






class Simple_player(Player):
    def __init__(self,weights, name="simple_player"):
        super(Simple_player, self).__init__()
        self.weights = {key:value for key,value in zip(ALL_CARDTYPES,weights)}
        self.N_cards = len(weights)


    def act(self, reward, observation=None, action_space=None):
        state = self.obs_to_state(observation)
        actions = list(OrderedDict.fromkeys(action_space))
        distro = np.array([self.weights[action] for action in actions],dtype=np.float32) + 1E-9
        distro = (distro)/float(np.sum(distro))

        idx = np.random.choice(len(distro),p=distro)
        return actions[idx]

    def obs_to_state(self,obs):
        state_hand = [0]*NUM_CARDS
        for card in obs['hand']:
            state_hand[CARDS_IDX[card]] += 1
        state_table = [0]*NUM_CARDS
        for card in obs['table'][self.name]:
            state_table[CARDS_IDX[card.type]] += 1
        return state_hand + state_table
