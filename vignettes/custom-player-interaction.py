import sushigo
import random

POSSIBLE_CARDS = list(set([str(_) for _ in sushigo.deck.StandardDeck()]))

class CustomPlayer(sushigo.player.Player):
    def act(self, reward, observation=None, action_space=None):
        if not action_space:
            raise ValueError("player received an empty set of actions")

        # the player can get a notion of possible cards, give them an order
        order = {j: i for i, j in enumerate(set([str(_) for _ in POSSIBLE_CARDS]))}
        ordered_actions = sorted(action_space, key = lambda _: order[str(_)])

        # the action space consists of objects now, which we may need to sort
        return ordered_actions[0]


def simulate(n_games = 10):
    res = []
    for _ in range(n_games):
        p1 = sushigo.player.Player(name="p1")
        p2 = CustomPlayer(name="custom")

        players = [p1,p2]
        game = sushigo.game.Game(players, deck=sushigo.deck.StandardDeck())
        game.simulate_game()
        res.append(game.did_player_win("custom"))
    return sum(res)

# let's do a super naive random search
for i in range(10):
    random.shuffle(POSSIBLE_CARDS)
    score = simulate(10)
    print("card:{}\nscore:{}".format(POSSIBLE_CARDS, score))