from sushigo.deck import Deck
import pprint

pp = pprint.PrettyPrinter(indent=2)


class Game(object):
    def __init__(self, agents, deck_constructor=None, cards_per_player=10, n_rounds=3, verbose=False):
        if len(set([_.name for _ in agents])) != len(agents):
            raise ValueError("two players in game have the same name")
        self.turn = 0
        self.round = 1
        self.verbose = verbose
        self.max_rounds = n_rounds
        self.cards_per_player = cards_per_player
        self.deck_constructor = Deck
        if deck_constructor:
            self.deck_constructor = deck_constructor
        self.deck = self.deck_constructor()
        self.players = {_.name: _ for _ in agents}
        self.scores = {"round-{}".format(i): {_.name: 0. for _ in agents} for i in range(1, n_rounds + 1)}
        for name in self.players.keys():
            self.players[name].hand = self.deck.cards[:cards_per_player]
            self.deck.cards = self.deck.cards[cards_per_player:]

    def play_turn(self):
        """
        This method simulates a single turn in a game.
        """
        for player_name in self.players.keys():
            observation = self.get_observation(player_name)
            action_space = self.get_action_space(player_name)
            player = self.players[player_name]

            # the player selects a type of card
            card_type = player.act(observation=observation, action_space=action_space)

            # throw error if agent returns something strange
            if card_type not in [_.type for _ in player.hand]:
                raise ValueError("Player {} does not have card of type {}".format(player_name, card_type))
            card = sorted(player.hand, key=lambda _: _.type == card_type)[-1]

            # next we determine the new player_state
            player.table.append(card)
            player.hand = [c for c in player.hand if c.id != card.id]

        # last thing we need to do is ensure that everybody switches hand
        current_hands = [p.hand for p in self.players.values()]
        for i, name in enumerate(self.players.keys()):
            self.players[name].hand = current_hands[i - 1]

        # the very last thing is to update the turn
        self.turn += 1
        self.update_scores()
        if self.verbose:
            res = self.scores.copy()
            res["turn"] = self.turn
            pp.pprint(res)

    def reset_game(self):
        self.turn = 0
        self.round = 1
        self.deck = self.deck_constructor()
        self.scores = {"round-{}".format(i): {_: 0. for _ in self.players.keys()} for i in range(1, self.max_rounds + 1)}
        for name in self.players.keys():
            self.players[name].hand = self.deck.cards[:self.cards_per_player]
            self.deck.cards = self.deck.cards[self.cards_per_player:]

    def play_round(self):
        for turn in range(self.cards_per_player):
            self.play_turn()
        # if all games haven't been played yet, draw cards again
        if self.round < self.max_rounds:
            self.scores["round-{}".format(self.round)] = self.calc_scores()
            self.round += 1
            for name in self.players.keys():
                # if the deck is going to run out of cards: throw error
                if len(self.deck.cards) < self.cards_per_player:
                    raise RuntimeError("Deck needs more cards for this many rounds of plays")
                self.players[name].hand = self.deck.cards[:self.cards_per_player]
                self.deck.cards = self.deck.cards[self.cards_per_player:]

    def play_full_game(self):
        for game in range(self.max_rounds):
            self.play_round()
        scores = self.calc_scores().copy()
        return scores

    def simulate_game(self):
        scores = self.play_full_game()
        self.reset_game()
        return scores

    def get_action_space(self, name):
        return [_.type for _ in self.players[name].hand]

    def get_observation(self, name):
        return {
            "table": {_: self.players[_].table for _ in self.players.keys()},
            "hand": [_.type for _ in self.players[name].hand],
            "scores": self.scores
        }

    def calc_scores(self):
        n_pudding = {p: self.count_cards(p, 'pudding') for p in self.players.keys()}
        n_maxi = {p: self._maki_roll_count(p) for p in self.players.keys()}
        score_dict = {}
        for player in self.players.keys():
            # handle simple scores
            score = (self._nigiri_score(player) +
                     self._nigiri_score(player) +
                     self._sashimi_score(player) +
                     self._tempura_score(player))
            # handle pudding score
            if self.count_cards(player, 'pudding') == max(n_pudding.values()):
                score += 6 / sum([_ == max(n_pudding.values()) for _ in n_pudding.values()])
            if self.count_cards(player, 'pudding') == min(n_pudding.values()):
                if len(self.players) > 2:
                    score -= 6 / sum([_ == min(n_pudding.values()) for _ in n_pudding.values()])
            # handle best maki score
            if self._maki_roll_count(player) == max(n_pudding.values()):
                score += 6 / sum([_ == max(n_maxi) for _ in n_maxi])
            # handle second best maki score
            scores_without_best = [_ for _ in n_pudding.values()]
            if len(scores_without_best) != 0:
                if self._maki_roll_count(player) == max(scores_without_best):
                    score += 3 / sum([_ == max(scores_without_best) for _ in scores_without_best])
            score_dict[player] = float(score)
        return score_dict

    def update_scores(self):
        res = self.scores.copy()
        res['round-{}'.format(self.round)] = self.calc_scores()
        self.scores = res

    def count_cards(self, player_name, cardtype):
        return len([_ for _ in self.players[player_name].table if _.type == cardtype])

    def _maki_roll_count(self, player_id):
        score_map = {'maki-1': 1, 'maki-2': 2, 'maki-3': 3}
        return sum([score_map[_.type] for _ in self.players[player_id].table if _.type in score_map.keys()])

    def _nigiri_score(self, player_name):
        nigiri_score = 0
        multiplier = 1
        for card in self.players[player_name].table:
            if card.type == 'wasabi':
                multiplier = 3
            if card.type == 'egg-nigiri':
                nigiri_score += 1 * multiplier
                multiplier = 1
            if card.type == 'salmon-nigiri':
                nigiri_score += 2 * multiplier
                multiplier = 1
            if card.type == 'squid-nigiri':
                nigiri_score += 3 * multiplier
                multiplier = 1
        return nigiri_score

    def _dumpling_score(self, player_name):
        # TODO: what if the player receives 6 of these cards?
        score_map = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15}
        n_dumplings = self.count_cards(player_name, 'dumpling')
        return score_map[n_dumplings]

    def _tempura_score(self, player_name):
        n_tempura = self.count_cards(player_name, 'tempura')
        return round(n_tempura/2)*5

    def _sashimi_score(self, player_name):
        n_sashimi = self.count_cards(player_name, 'sashimi')
        return round(n_sashimi/3)*10
