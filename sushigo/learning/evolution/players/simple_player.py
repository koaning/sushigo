import uuid
import random
from sushigo.player import Player
import numpy as np
from sushigo.deck import ALL_CARDTYPES
from collections import OrderedDict  #https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists


class Simple_player(Player):
    def __init__(self,weights, name="simple_player"):
        super(Simple_player, self).__init__()
        self.weights = {key:value for key,value in zip(ALL_CARDTYPES,weights)}
        self.N_cards = len(weights)


    def act(self, reward, observation=None, action_space=None):
        actions = list(OrderedDict.fromkeys(action_space))
        distro = np.array([self.weights[action] for action in actions],dtype=np.float32) + 1E-9
        distro = (distro)/float(np.sum(distro))

        idx = np.random.choice(len(distro),p=distro)
        return actions[idx]
