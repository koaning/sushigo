from sushigo.player import Player
from sushigo.deck import StandardDeck, InfiniDeck, Deck
from sushigo.game import Game


def test_after_turn_hands_exchange_two_player():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2], n_rounds=2)
    print(game.scores)
    scores0 = game.scores
    game.play_round()
    scores1 = game.scores
    game.play_round()
    scores2 = game.scores
    print(scores1)
    print(scores2)
    assert scores0['round-1']['bob'] == 0.0
    assert scores1['round-2']['bob'] == 0.0
    assert scores2['round-2']['bob'] > 0.0
    assert scores2['round-2']['sharon'] > 0.0


def test_after_turn_hands_exchange_three_player():
    p1 = Player("bob")
    p2 = Player("sharon")
    p3 = Player("alice")
    game = Game(deck_constructor=InfiniDeck, agents=[p1, p2, p3], n_rounds=3)
    scores0 = game.scores
    game.play_round()
    scores1 = game.scores
    game.play_round()
    scores2 = game.scores
    game.play_round()
    scores3 = game.scores
    print(scores3)
    assert scores3['round-1']['bob'] == scores1['round-1']['bob']
    assert scores3['round-2']['alice'] > scores0['round-2']['alice']
    assert scores3['round-2']['bob'] > scores1['round-2']['bob']
    assert scores3['round-2']['sharon'] > scores1['round-2']['alice']


def test_certain_cards_carry_no_rewards_within_rounds():
    p1 = Player("bob")
    p2 = Player("sharon")
    # create a deck with no cards that are worth points during a round
    d = Deck(egg=0, salmon=0, squid=0, tempura=0, sashimi=0, dumpling=0)
    assert all([(_.type != 'tempura') for _ in d.cards])
    g = Game(deck_constructor=lambda: d, agents=[p1, p2])
    g.play_turn()
    assert g.gamelog.shape[0] == 4
    assert g.gamelog['reward'][0] == 0.0
    assert g.gamelog['reward'][1] == 0.0
    g.play_turn()
    g.play_turn()
    g.play_turn()
    assert g.gamelog['reward'].iloc[-1] == 0.0


def test_certain_cards_carry_rewards_at_end_of_round():
    p1 = Player("bob")
    p2 = Player("sharon")
    # create a deck with no cards that are worth points during a round
    d = Deck(egg=0, salmon=0, squid=0, tempura=0,
             sashimi=0, dumpling=0, pudding=0,
             wasabi=0, maki1=0, maki2=0, maki3=100)
    assert all([(_.type != 'tempura') for _ in d.cards])
    g = Game(deck_constructor=lambda: d, agents=[p1, p2], cards_per_player=10)
    g.play_round()
    g.play_round()
    print(g.gamelog)
    assert g.gamelog.shape[0] == 42
    assert g.gamelog['reward'][0] == 0.0
    assert g.gamelog['reward'][1] == 0.0
    assert g.gamelog['reward'][2] == 0.0
    assert g.gamelog['reward'][3] == 0.0
    assert g.gamelog['reward_cs'].iloc[-2] == 3.0
    assert g.gamelog['reward_cs'].iloc[-1] == 6.0
    assert False