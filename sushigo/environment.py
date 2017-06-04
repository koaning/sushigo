# ignore this file for now
from sushigo.game import Game

class Environment():
    def __init__(self, name, opponents):
        self.name = name
        self.user_agent = "foo"
        self.game = Game(agents=[self.user_agent] + opponents)

    def reset(self):
        self.game.reset_game()
        return self.game.get_observation("env-player")

    def action_space(self):
        return self.game.get_action_space("env-player")

    def step(self, action):
