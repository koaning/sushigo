from sushigo.player import Player
from sushigo.deck import StandardDeck, Deck
from sushigo.game import Game


def test_after_turn_hands_exchange_two_player():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck=StandardDeck(), agents=[p1, p2])
    p1_hand_before, p2_hand_before = p1.hand, p2.hand
    game.play_full_game()
    game.calc_scores()