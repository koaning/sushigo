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

def allow(perm):
    """
    This function acts as a predicate for allowed permutations.
    """
    # leaves us with 1108800/39916800 permutations
    order = {j: i for i, j in enumerate([str(_) for _ in perm])}
    if order['NigiriCard("egg")'] > order['NigiriCard("salmon")']:
        return False
    if order['NigiriCard("salmon")'] > order['NigiriCard("squid")']:
        return False
    if order['MakiCard("2")'] > order['MakiCard("3")']:
        return False
    if order['MakiCard("1")'] > order['MakiCard("2")']:
        return False
    return True

def rand_iterable(iter, prob=0.001, max_i = 100):
    """
    Randomly selects some items in the iterable. 
    """
    i = 0
    while i<max_i:
        if random.random() < prob:
            yield next(iter)

allowed_perms = (_ for _ in it.permutations(POSSIBLE_CARDS) if allow(_))
# if you want to sample, you can uncomment this line.
allowed_perms = rand_iterable(_ for _ in it.permutations(POSSIBLE_CARDS) if allow(_))

print("This will run for a while because brute force is stupid.")
for permutation in allowed_perms:
    if not allow(permutation):
        continue
    n = 20
    order = {j: i for i, j in enumerate([str(_) for _ in permutation])}
    score = simulate(order, n)
    print("card order:{}\nnumber of wins:{}/{}".format(permutation, score, n))
