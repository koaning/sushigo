from sushigo.player import Player
from sushigo.cards import DumplingCard
from sushigo.deck import StandardDeck, InfiniDeck, Deck
from sushigo.game import Game


def test_reward_in_log_needs_to_accumulate():
    p1 = Player("bob")
    p2 = Player("sharon")
    d = Deck.create([DumplingCard()], [1000])
    game = Game(deck=d,  agents=[p1, p2], n_rounds=2)
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
