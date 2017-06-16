from sushigo.player import Player
from sushigo.cards import DumplingCard
from sushigo.deck import StandardDeck, InfiniDeck, Deck
from sushigo.game import Game


def test_reward_in_log_needs_to_accumulate():
    p1 = Player("bob")
    p2 = Player("sharon")
    d = Deck.create([DumplingCard()], [1000])
    game = Game(deck=d,  agents=[p1, p2], n_rounds=2)
