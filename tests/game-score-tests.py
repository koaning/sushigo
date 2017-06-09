from sushigo.player import Player
from sushigo.deck import StandardDeck, InfiniDeck, Deck
from sushigo.game import Game


def test_after_turn_hands_exchange_two_player():
    p1 = Player("bob")
    p2 = Player("sharon")
    game = Game(deck_constructor=StandardDeck, agents=[p1, p2], n_rounds=2)
    print(game.scores)
    scores0 = game.end_results()
    game.play_round()
    scores1 = game.end_results()
    game.play_round()
    scores2 = game.end_results()
    print(scores1)
    print(scores2)
    assert scores0['bob'] == 0.0
    assert scores1['bob'] > 0.0
    assert scores2['bob'] > 0.0
    assert scores2['sharon'] > 0.0


def test_after_turn_hands_exchange_three_player():
    p1 = Player("bob")
    p2 = Player("sharon")
    p3 = Player("alice")
    game = Game(deck_constructor=InfiniDeck, agents=[p1, p2, p3], n_rounds=3)
    scores0 = game.end_results()
    game.play_round()
    scores1 = game.end_results()
    game.play_round()
    scores2 = game.end_results()
    game.play_round()
    scores3 = game.end_results()
    assert scores3['bob'] > scores1['bob']
    assert scores3['alice'] > scores0['alice']
    assert scores3['bob'] > scores1['bob']
    assert scores3['sharon'] > scores1['sharon']


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
    assert g.gamelog['reward_cs'].iloc[-2] == 3.0
    assert g.gamelog['reward_cs'].iloc[-1] == 6.0

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


def simple_egg_score_test():
    p1 = Player("bob")
    p2 = Player("sharon")
    d = Deck(egg=1000, salmon=0, squid=0, tempura=0,
             sashimi=0, dumpling=0, pudding=0,
             wasabi=0, maki1=0, maki2=0, maki3=0)
    g = Game(deck_constructor=lambda: d, agents=[p1, p2], cards_per_player=10)
    g.play_round()
    g.play_round()
    print(g.gamelog)
    assert g.gamelog.shape[0] == 42
    assert g.gamelog['reward'][2] == 0.0
    assert g.gamelog['reward'][3] == 0.0
    assert g.gamelog['reward_cs'].iloc[-2] == 19.0
    assert g.gamelog['reward_cs'].iloc[-1] == 20.0


def test_simple_one_winner_one_round():
    p1 = Player("bob")
    p2 = Player("sharon")
    d = Deck(egg=19, salmon=1, squid=0, tempura=0,
             sashimi=0, dumpling=0, pudding=0,
             wasabi=0, maki1=0, maki2=0, maki3=0)
    g = Game(deck_constructor=lambda: d, agents=[p1, p2], cards_per_player=10, n_rounds=1)
    g.play_round()
    bob_log = g.gamelog[g.gamelog['player'] == 'bob']
    bob_final_reward = bob_log['reward'].iloc[-1]
    sharon_log = g.gamelog[g.gamelog['player'] == 'sharon']
    sharon_final_reward = sharon_log['reward'].iloc[-1]
    print(g.gamelog)
    assert g.gamelog.shape[0] == 22
    assert (bob_final_reward == 10.) or (bob_final_reward == 11.)
    assert (sharon_final_reward == 10.) or (sharon_final_reward == 11.)


def test_simple_one_winner_two_rounds():
    p1 = Player("bob")
    p2 = Player("sharon")
    d = Deck(egg=39, salmon=1, squid=0, tempura=0,
             sashimi=0, dumpling=0, pudding=0,
             wasabi=0, maki1=0, maki2=0, maki3=0)
    g = Game(deck_constructor=lambda: d, agents=[p1, p2], cards_per_player=10, n_rounds=2)
    g.play_round()
    g.play_round()
    bob_log = g.gamelog[g.gamelog['player'] == 'bob']
    bob_final_reward = bob_log['reward'].iloc[-1]
    sharon_log = g.gamelog[g.gamelog['player'] == 'sharon']
    sharon_final_reward = sharon_log['reward'].iloc[-1]
    print(g.gamelog)
    assert g.gamelog.shape[0] == 42
    assert (bob_final_reward == 20.) or (bob_final_reward == 21.)
    assert (sharon_final_reward == 20.) or (sharon_final_reward == 21.)


def test_reward_in_log_needs_to_accumulate():
    p1 = Player("bob")
    p2 = Player("sharon")
    d = Deck(egg=15, salmon=15, squid=15, tempura=15,
             sashimi=15, dumpling=15, pudding=0,
             wasabi=15, maki1=10, maki2=10, maki3=10)
    g = Game(deck_constructor=lambda: d, agents=[p1, p2], cards_per_player=10, n_rounds=2)
    g.simulate_game()
    df = g.gamelog.sort_values(["player", "turn"])
    for player in ["bob", "sharon", "alice"]:
        print(df[df['player'] == player])
    p1_rewards = df[df['player'] == 'bob']['reward']
    p2_rewards = df[df['player'] == 'sharon']['reward']
    print(g.scores)
    assert all([_ >= 0 for _ in (p1_rewards - p1_rewards.shift().fillna(0))])
    assert all([_ >= 0 for _ in (p2_rewards - p2_rewards.shift().fillna(0))])