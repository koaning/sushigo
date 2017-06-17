import sushigo
import itertools as it
import random

POSSIBLE_CARDS = list(set([str(_) for _ in sushigo.deck.StandardDeck()]))

class CustomPlayer(sushigo.player.Player):
    def __init__(self, order, name=None):
        super(CustomPlayer, self).__init__()
        self.name = 'custom-player'
        if name:
            self.name = name
        self.order = order
        if any([(_ not in order) for _ in POSSIBLE_CARDS]):
            raise ValueError("forgot card type in OrderedPlayer init")

    def act(self, reward, observation=None, action_space=None):
        if not action_space:
            raise ValueError("player received an empty set of actions")

        # the player can get a notion of possible cards, give them an order
        order = {j: i for i, j in enumerate(self.order)}
        # the action space consists of objects now, which we may need to string-sort
        ordered_actions = sorted(action_space, key = lambda _: order[str(_)])

        return ordered_actions[-1]


def simulate(order, n_games = 10):
    """
    This function simulates a game, assuming a player uses certain order.
    """
    res = []
    for _ in range(n_games):
        p1 = sushigo.player.Player(name="p1")
        p2 = CustomPlayer(name="custom", order = order)
        players = [p1,p2]
        game = sushigo.game.Game(players, deck=sushigo.deck.StandardDeck())
        game.simulate_game()
        res.append(game.did_player_win("custom"))
    return sum(res)

def swap(arr):
    """
    Randomly selects some items in the iterable. 
    """
    i1 = random.randint(0, len(arr) - 1)
    i2 = random.randint(0, len(arr) - 1)
    arr[i2], arr[i1] = arr[i1], arr[i2]
    return arr

print("This will simulate games for a greedy search.")
score_before = 0
order = POSSIBLE_CARDS
for _ in range(100):
    n = 100
    new_order = swap(order)
    new_score = simulate(order, n)
    print("iteration: {}\ncard order:{}\nnumber of wins:{}/{}".format(_, new_order, new_score, n))
    if new_score > score_before:
        print("IMPROVEMENT!")
        order = new_order
        score_before = new_score
