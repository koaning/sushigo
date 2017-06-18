import numpy as np
np.random.seed(123)
import torch
import torch.optim as optim

from sushigo.learning.pg_ff.players.simple_player import Simple_player
from sushigo.learning.pg_rnn.players.pg_player import Pg_player
from sushigo.learning.pg_rnn.policies.rnn_policy import Policy, finish_game
from sushigo.learning.pg_rnn.util.util import adjust_learning_rate
from sushigo.deck import StandardDeck
from sushigo.game import Game

#Set up policy
policy = Policy('LSTM',22,20,1,11)
torch.manual_seed(123)

#Parameters
gamma = 0.99

#Set up optim
lr = 1e-2
optimizer = optim.Adam(policy.parameters(), lr=lr)
log_interval = 10


#Play games
deck = StandardDeck()
N_cards = len(list(set([str(_) for _ in deck])))
p1 = Pg_player(policy=policy,name="PG_player01")
p2 = Simple_player(weights=[1/N_cards]*N_cards,name="SIMPLE_player01")

ewma = 0.5
alpha = 0.95
for n in range(100):
    game = Game([p1,p2],verbose=False)
    game.simulate_game()
    win = game.did_player_win(p1.name)
    ewma = alpha*ewma + (1-alpha)*int(win)
    print('At %3i ewma win ratio %5.3f'%(n,ewma))

    finish_game(policy, gamma=gamma, optimizer=optimizer)
    p1.prev_reward = None
    optimizer = adjust_learning_rate(optimizer,n,lr,30)
