from collections import namedtuple

Card = namedtuple("Card", ["type"])

class Deck():
    def __init__(self):
        self.cards = ([Card('maki-1')] * 5 +
                     [Card('maki-2')] * 5 +
                     [Card('maki-3')] * 5 +
                     [Card('pudding')] * 5 +
                     [Card('egg-nigiri')] * 5 +
                     [Card('salmon-nigiri')] * 5 +
                     [Card('squid-nigiri')] * 5 +
                     [Card('tempura')] * 5 +
                     [Card('sashimi')] * 5 +
                     [Card('dumpling')] * 5)

class Player():
    def __init__(self):
        self.table = []
        self.hand = []
    pass

class Game():
    def __init__(self):
        pass

    def calc_scores(self):
        n_pudding = [self.count_cards(p, 'pudding') for p in self.players]
        n_maxi = [self._maki_roll_count(p) for p in self.players]
        score_dict = {}
        for player in self.players:
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
            scores_without_best = [_ for _ in n_pudding _ != max(n_pudding)]
            if len(scores_without_best) != 0:
                if self._maki_roll_count(player) == max(scores_without_best):
                    score += 3 / sum([_ == max(scores_without_best) for _ in scores_without_best])
            score_dict[player.name] = score
        return score_dict

    def count_cards(self, player, cardtype):
        return len([_ for _ in player.cards if _.type == cardtype])

    def _maki_roll_count(self, player):
        score_map = {'maxi-1':1, 'maxi-2':2, 'maxi-3':3}
        return sum([score_map[_.type] for _ in player.cards if _.type in score_map.keys()])

    @staticmethod
    def _nigiri_score(player):
        nigiri_score = 0
        multiplier = 1
        for card in player.cards:
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

    def _dumpling_score(self, player):
        score_map = {1:1, 2:3, 3:6, 4:10, 5:15}
        n_dumplings = self.count_cards(player, 'dumpling')
        return score_map[n_dumplings]

    def _tempura_score(self, player):
        n_tempura = self.count_cards(player, 'tempura')
        return round(n_tempura/2)*5

    def _sashimi_score(self, player):
        n_sashimi = self.count_cards(player, 'sashimi')
        return round(n_sashimi/3)*10
