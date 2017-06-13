import sushigo
import numpy as np

from sushigo.deck import ALL_CARDTYPES
from sushigo.learning.evolution.players.simple_player import Simple_player
from sushigo.learning.evolution.utils import is_winner

N_cards = len(ALL_CARDTYPES)

trials = 10
games_per_trial = 25
max_weight = 100


best_trial_points = -99999
best_trial_weights = None
for trial in range(trials):
    trial_points = 0

    trial_weights = np.random.randint(0,max_weight,size=(N_cards,))
    for game in range(games_per_trial):

        p1 = Simple_player(weights=[26, 56, 54, 30, 77, 53, 53, 96, 78,  3, 77],name="ES_player02")
        p2 = Simple_player(weights = trial_weights, name="ES_player01")

        game = sushigo.game.Game([p1, p2], verbose=False)
        scores = game.simulate_game()
        trial_points += is_winner(scores, p2.name)

    if trial_points > best_trial_points:
        best_trial_points = trial_points
        best_trial_weights = trial_weights
    print('Trial %5i best points %5i best weights %s'%(trial,best_trial_points, best_trial_weights))

