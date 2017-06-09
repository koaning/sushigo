from sushigo.player import Player
from sushigo.deck import StandardDeck, InfiniDeck, Deck
from sushigo.game import Game


def test_reward_in_log_needs_to_accumulate():
    p1 = Player("bob")
    p2 = Player("sharon")
    d = Deck(maki1=0, maki2=0, maki3=0, pudding=0,
             egg=0, salmon=0, squid=0, tempura=0,
             sashimi=0, dumpling=1000, wasabi=0)
    game = Game(deck_constructor=lambda: d, agents=[p1, p2], n_rounds=2)
    assert game._dumpling_score("bob") == 0.0
    game.play_turn()
    assert game._dumpling_score("bob") == 1.0
    game.play_turn()
    assert game._dumpling_score("bob") == 3.0
    game.play_turn()
    assert game._dumpling_score("bob") == 6.0
    game.play_turn()
    assert game._dumpling_score("bob") == 10.0
    game.play_turn()
    assert game._dumpling_score("bob") == 15.0
    game.play_turn()
    assert game._dumpling_score("bob") == 16.0
    game.play_turn()
    assert game._dumpling_score("bob") == 18.0
