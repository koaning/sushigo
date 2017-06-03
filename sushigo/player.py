import uuid
import random

class Player():
    def __init__(self, name=None):
        self.name = str(uuid.uuid4())[:6]
        if name:
           self.name = name
        self.table = []
        self.hand = []

    def act(self, observation=None, action_space=None):
        if not action_space:
            raise ValueError("player received an empty set of actions")
        return random.choice(action_space)

