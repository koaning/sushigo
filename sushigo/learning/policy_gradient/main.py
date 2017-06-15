import sushigo
import numpy as np
np.random.seed(123)

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable

from sushigo.deck import ALL_CARDTYPES
from sushigo.learning.policy_gradient.players.simple_player import Simple_player
from sushigo.learning.policy_gradient.players.pg_player import Pg_player
from sushigo.learning.policy_gradient.policies.first_policy import Policy, select_action, finish_game
from sushigo.game import Game

#Set up policy
policy = Policy()
torch.manual_seed(123)

#Parameters
N_cards = len(ALL_CARDTYPES)
trials = 10
games_per_trial = 25
max_weight = 100
gamma = 0.99

#Set up optim
optimizer = optim.Adam(policy.parameters(), lr=1e-2)
log_interval = 10


#Play one game
p1 = Pg_player(policy=policy,name="PG_player01")
p2 = Simple_player(weights=[26, 56, 54, 30, 77, 53, 53, 96, 78,  3, 77],name="SIMPLE_player01")
game = Game([p1,p2],verbose=False)
game.play_full_game()
win = game.calc_reward(p1.name) > game.calc_reward(p2.name)
print('Pg player did win: %s'%win)

finish_game(p1.policy, gamma=gamma, optimizer=optimizer)
