from sushigo.player import Player
from sushigo.deck import StandardDeck, Deck
from sushigo.game import Game


def test_game_contains_players_cards_and_deck_2player():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2], cards_per_player=10)
    assert len(game.players.keys()) == 2
    assert isinstance(game.deck, Deck)
    print(game.players)
    print(game.players["bob"])
    assert len(game.players["bob"].hand) == 10
    assert len(game.players["sharon"].hand) == 10


def test_game_assigns_correct_number_of_cards_3player():
    p1 = Player("bob")
    p2 = Player("sharon")
    p3 = Player("alice")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2, p3], cards_per_player=8)
    assert len(game.players.keys()) == 3
    assert isinstance(game.deck, Deck)
    assert len(game.players["bob"].hand) == 8
    assert len(game.players["sharon"].hand) == 8
    assert len(game.players["alice"].hand) == 8


def test_after_turn_hands_exchange_two_player():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2], cards_per_player=10)
    p1_hand_before, p2_hand_before = p1.hand, p2.hand
    game.play_turn()
    assert len(p1.hand) == 9
    assert len(p2.hand) == 9
    assert all([(_ in p2_hand_before) for _ in p1.hand])
    assert all([(_ in p1_hand_before) for _ in p2.hand])


def test_after_turn_hands_exchange_three_player():
    p1 = Player("bob")
    p2 = Player("sharon")
    p3 = Player("alice")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2, p3], cards_per_player=10)
    p1_hand_before, p2_hand_before, p3_hand_before = p1.hand, p2.hand, p3.hand
    game.play_turn()
    assert len(p1.hand) == 9
    assert len(p2.hand) == 9
    assert len(p3.hand) == 9
    assert all([(_ in p3_hand_before) for _ in p1.hand])
    assert all([(_ in p2_hand_before) for _ in p3.hand])
    assert all([(_ in p1_hand_before) for _ in p2.hand])


def test_after_game_players_have_no_cards():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2], n_rounds=1)
    game.play_round()
    assert len(p1.hand) == 0
    assert len(p2.hand) == 0


def test_turns_update():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2], n_rounds=2)
    game.play_round()
    assert game.turn == 10
    game.play_round()
    assert game.turn == 20


def test_interal_game_reset_functionality():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2], n_rounds=2, cards_per_player=10)
    game.play_round()
    assert game.turn == 10
    game.play_round()
    assert game.turn == 20
    game.reset_game()
    assert game.turn == 0
    assert len(p1.hand) == 10
    assert len(p2.hand) == 10
