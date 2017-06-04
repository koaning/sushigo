from sushigo.player import Player
from sushigo.deck import StandardDeck, InfiniDeck
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
    assert scores0['game-1']['bob'] == 0.0
    assert scores1['game-2']['bob'] == 0.0
    assert scores2['game-2']['bob'] > 0.0
    assert scores2['game-2']['sharon'] > 0.0

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
    assert scores3['game-1']['bob'] == scores1['game-1']['bob']
    assert scores3['game-2']['alice'] > scores0['game-2']['alice']
    assert scores3['game-2']['bob'] > scores1['game-2']['bob']
    assert scores3['game-2']['sharon'] > scores1['game-2']['alice']

def test_game_reset_handles_scores_well():
    p1 = Player("bob")
    p2 = Player("sharon")
    p3 = Player("alice")
    game = Game(deck_constructor=InfiniDeck, agents=[p1, p2, p3], n_rounds=3)
    game.play_full_game()
    print(game.scores)
    game.reset_game()
    print(game.scores)
    assert game.scores['game-1']['bob'] == 0.0