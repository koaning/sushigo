from sushigo.deck import Deck

class Game():
    def __init__(self, agents, deck=None, cards_per_player=10, n_games=3):
        if len(set([_.name for _ in agents])) != len(agents):
            raise ValueError("two players in game have the same name")
        self.turn = 1
        self.game = 1
        self.max_games = n_games
        self.cards_per_player = cards_per_player
        self.deck = Deck()
        if deck:
            self.deck = deck
        self.players = {_.name:_ for _ in agents}
        for name in self.players.keys():
            self.players[name].hand = self.deck.cards[:cards_per_player]
            self.deck.cards = self.deck.cards[cards_per_player:]

    def play_turn(self):
        """
        This method simulates a single turn in a game.
        """
        # lets play every players choice
        for player_name in self.players.keys():
            # first we determine the card choice
            # observation = self.player_state(player_name)
            # action_space = self.player_action_space(player_name)
            # TODO implement player_state and player_action_space
            player = self.players[player_name]
            card = player.act(observation=1, action_space=player.hand)
            # next we determine the new player_state
            player.table.append(card)
            player.hand = [c for c in player.hand if c.id != card.id]

        # last thing we need to do is ensure that everybody switches hand
        current_hands = [p.hand for p in self.players.values()]
        for i, name in enumerate(self.players.keys()):
            self.players[name].hand = current_hands[i - 1]



    def calc_scores(self):
        n_pudding = [self.count_cards(p, 'pudding') for p in range(self.players)]
        n_maxi = [self._maki_roll_count(p) for p in range(self.players)]
        score_dict = {}
        for player in range(self.players):
            # handle simple scores
            score = (self._nigiri_score(player) +
                     self._nigiri_score(player) +
                     self._sashimi_score(player) +
                     self._tempura_score(player))
            # handle pudding score
            if self.count_cards(player, 'pudding') == max(n_pudding):
                score += 6 / sum([_ == max(n_pudding) for _ in n_pudding])
            if self.count_cards(player, 'pudding') == min(n_pudding):
                if len(self.players) > 2:
                    score -= 6 / sum([_ == min(n_pudding) for _ in n_pudding])
            # handle best maki score
            if self._maki_roll_count(player) == max(n_pudding):
                score += 6 / sum([_ == max(n_maxi) for _ in n_maxi])
            # handle second best maki score
            scores_without_best = [_ for _ in n_pudding]
            if len(scores_without_best) != 0:
                if self._maki_roll_count(player) == max(scores_without_best):
                    score += 3 / sum([_ == max(scores_without_best) for _ in scores_without_best])
            score_dict[player.name] = score
        return score_dict

    def count_cards(self, player_id, cardtype):
        return len([_ for _ in self.players[player_id].table if _.type == cardtype])

    def _maki_roll_count(self, player_id):
        score_map = {'maki-1': 1, 'maki-2': 2, 'maki-3': 3}
        return sum([score_map[_.type] for _ in self.players[player_id].table if _.type in score_map.keys()])

    def _nigiri_score(self, player_id):
        nigiri_score = 0
        multiplier = 1
        for card in self.players[player_id].table:
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

    def _dumpling_score(self, player_id):
        score_map = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15}
        n_dumplings = self.count_cards(player_id, 'dumpling')
        return score_map[n_dumplings]

    def _tempura_score(self, player_id):
        n_tempura = self.count_cards(player_id, 'tempura')
        return round(n_tempura/2)*5

    def _sashimi_score(self, player_id):
        n_sashimi = self.count_cards(player_id, 'sashimi')
        return round(n_sashimi/3)*10
