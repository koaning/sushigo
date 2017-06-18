from sushigo.deck import StandardDeck
from itertools import islice
import numpy as np
import pandas as pd
import datetime
import uuid
import pprint

pp = pprint.PrettyPrinter(indent=2)


class Game(object):
    def __init__(self, agents, deck=None, cards_per_player=10, n_rounds=3, verbose=False):
        if len(set([_.name for _ in agents])) != len(agents):
            raise ValueError("two players in game have the same name")
        self.turn = 1
        self.round = 1
        self.verbose = verbose
        self.max_rounds = n_rounds
        self.cards_per_player = cards_per_player
        self.deck = deck if deck else StandardDeck()
        if self.cards_per_player * len(agents) * n_rounds > self.deck.cards_left:
            raise ValueError('Deck has not enough cards.')
        self.score = self.deck.scoring_function()
        self.players = {_.name: _ for _ in agents}
        self.game_id = str(uuid.uuid4())[:6]
        self.gamelog = pd.DataFrame({
            "game_id": self.game_id,
            "round": 0,
            "turn": 0,
            "player": list(self.players.keys()),
            "action": '',
            "reward": 0,
            "round_reward": 0
        })
        self.scores = {"round-{}".format(i): {_.name: 0.0 for _ in agents} for i in range(0, n_rounds + 1)}
        for name in self.players.keys():
            self.players[name].hand = list(islice(self.deck, self.cards_per_player))

    def log_user_action(self, player_name, action):
        """
        This method appends to the log dataframe found in self.gamelog 
        :param player_name: player object, not player-name 
        :param action: action, card type string 
        """
        log = pd.DataFrame({
            'game_id': [self.game_id],
            'round': self.round,
            'turn': self.turn,
            'player': player_name,
            'action': action,
            'reward': self.calc_points(player_name),
            'round_reward': self.calc_scores()[player_name]
        })
        df = pd.concat([self.gamelog, log], ignore_index=True).sort_values(['player', 'turn'])
        self.gamelog = df

    def play_turn(self):
        """
        This method simulates a single turn in a game.
        """
        chosen_cards = {}
        for player_name in self.players.keys():
            observation = self.get_observation(player_name)
            action_space = self.get_action_space(player_name)
            last_log_player = self.gamelog[self.gamelog['player'] == player_name].iloc[-1]
            reward = last_log_player['reward']
            player = self.players[player_name]

            # the player selects a type of card
            chosen_card = player.act(reward=reward,
                                     observation=observation,
                                     action_space=action_space)
            chosen_cards[player_name] = chosen_card

            # next we determine the new player_state
            player.table.append(chosen_card)
            player.hand = [card for card in player.hand if card is not chosen_card]
        for player_name, chosen_card in chosen_cards.items():
            self.log_user_action(player_name=player_name, action=chosen_card)

        # last thing we need to do is ensure that everybody switches hand
        current_hands = [p.hand for p in self.players.values()]
        for i, name in enumerate(self.players.keys()):
            self.players[name].hand = current_hands[i - 1]

        # if this is the last turn of the round we want to remove the table
        if self.turn % self.cards_per_player == 0:
            self.calc_scores()
            self.reset_table()
        # the very last thing is to update the turn
        self.turn += 1

        if self.verbose:
            info = {}
            info['game'] = self.game_id
            info['round'] = self.round
            info['turn'] = self.turn
            info['table'] = {_: [c.type for c in self.players[_].table] for _ in self.players.keys()}
            info['points'] =  {_: self.calc_points(_) for _ in self.players.keys()}
            pprint.pprint(info, width=2)

    def reset_table(self):
        """Clears the table. Persistent cards remain."""
        for player in self.players.values():
            player.table = [card for card in player.table if card.persistent]

    def reset_game(self):
        self.turn = 0
        self.round = 1
        self.game_id = str(uuid.uuid4())[:6]
        self.deck.reset()
        for player in self.players.values():
            player.table = []
        self.scores = {"round-{}".format(i): {_: 0. for _ in self.players.keys()} for i in range(1, self.max_rounds + 1)}
        for name in self.players.keys():
            self.players[name].hand = list(islice(self.deck, self.cards_per_player))

    def play_round(self):
        for turn in range(self.cards_per_player):
            self.play_turn()
        # if all games haven't been played yet, draw cards again
        if self.round < self.max_rounds:
            self.scores["round-{}".format(self.round)] = self.calc_scores()
            self.round += 1
            for name in self.players.keys():
                self.players[name].hand = list(islice(self.deck, self.cards_per_player))

    def simulate_game(self):
        """
        This method simulates a single game and resets it.
        :return:
        """
        for round in range(self.max_rounds):
            self.play_round()
        self.reset_game()
        return self.gamelog

    def end_results(self):
        output = {}
        this_game_log = self.gamelog[self.gamelog['game_id'] == self.game_id]
        this_game_log = this_game_log[this_game_log['turn'] == this_game_log['turn'].max()]
        for player in self.players:
            player_log = this_game_log[this_game_log['player'] == player]
            output[player] = player_log['reward'].iloc[-1]
        return output

    def get_action_space(self, player_name):
        return self.players[player_name].hand

    def get_observation(self, player_name):
        return {
            "table": {_: self.players[_].table for _ in self.players.keys()},
            "hand": [repr(_) for _ in self.players[player_name].hand],
            "scores": self.scores
        }

    @property
    def is_end_of_round(self):
        return self.turn % self.cards_per_player == 0

    @property
    def is_end_of_game(self):
        return self.round == self.max_rounds and self.is_end_of_round

    def calc_points(self, player_name):
        """
        This method calculates the direct points of a player at the
        time of the method call.
        :return: float
        """
        df = self.gamelog
        df = df[df["player"] == player_name]
        df = df[df["round"] == self.round - 1]
        prev_round_score = df["reward"].max()
        return self.calc_scores()[player_name] + prev_round_score

    def did_player_win(self, player_name):
        """
        :param player_name (str): name of the player in the game
        :return (bool): True or False
        """
        df = self.gamelog
        df = df[df['turn'] == self.max_rounds * self.cards_per_player]
        return df['reward'].max() == df[df['player'] == player_name]['reward'].iloc[0]

    def calc_scores(self):
        """
        This method calculates the score of all players.
        This method should only be called at the last turn end of a round.
        :return: dict with player-name: scores for current round.
        """
        score_dict = self.score(
            player_cards={player_name: player.table for player_name, player in self.players.items()},
            end_round=self.is_end_of_round, end_game=self.is_end_of_game
        )
        for player_name, score in score_dict.items():
            self.scores["round-{}".format(self.round)][player_name] = float(score)
        return score_dict

    def count_cards(self, player_name, cardtype):
        return len([_ for _ in self.players[player_name].table if _.type == cardtype])