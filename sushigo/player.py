import uuid
import random

class Player():
    def __init__(self, name=None):
        self.name = 'random-player-{}'.format(str(uuid.uuid4())[:4])
        if name:
           self.name = name
        self.table = []
        self.hand = []

    def act(self, reward, observation=None, action_space=None):
        if not action_space:
            raise ValueError("player received an empty set of actions")
        return random.choice(action_space)

    def __repr__(self):
        return "<sushio.player.Player name={} at {}>".format(self.name, hex(id(self)))


class OrderedPlayer(Player):
    def __init__(self, name=None, order=None):
        super(OrderedPlayer, self).__init__()
        self.name = 'ordered-player-{}'.format(str(uuid.uuid4())[:4])
        if name:
            self.name = name
        self.order = ["pudding", "squid-nigiri", "maki-3",
                     "tempura", "salmon-nigiri", "dumpling", "maki-2",
                     "maki-1", "egg-nigiri", "sashimi", "wasabi"]
        if order:
            if any([(_ not in order) for _ in self.order]):
                raise ValueError("forgot card type in OrderedPlayer init")
            self.order = order

    def act(self, reward, observation=None, action_space=None):
        if not action_space:
            raise ValueError("player received an empty set of actions")
        preference_dict = {t: i for i,t in enumerate(self.order)}
        return sorted(action_space, key = lambda _: preference_dict[_])[0]
