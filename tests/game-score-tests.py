from sushigo.player import Player
from sushigo.deck import StandardDeck, Deck
from sushigo.game import Game


def test_after_turn_hands_exchange_two_player():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2])
    game.play_full_game()
    game.calc_scores()