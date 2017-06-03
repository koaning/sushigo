from sushigo import Game, Player, Card


def test_simple_player_card_count():
    p0 = Player()
    p0.table = [Card('dumpling')] * 5
    p1 = Player()
    p1.table = [Card('dumpling')] * 3
    g = Game(players=[p0, p1])
    assert g.count_cards(0, 'dumpling') == 5
    assert g.count_cards(1, 'dumpling') == 3


def test_simple_player_card_score1():
    p0 = Player()
    p0.table = [Card('dumpling')] * 5
    p1 = Player()
    p1.table = [Card('dumpling')] * 3
    g = Game(players=[p0, p1])
    assert g._dumpling_score(0) == 15
    assert g._dumpling_score(1) == 6


def test_simple_player_card_score2():
    p0 = Player()
    p0.table = [Card('dumpling'), Card("maki-1")]
    p1 = Player()
    p1.table = [Card('dumpling'), Card("salmon-nigiri")] * 3
    g = Game(players=[p0, p1])
    assert g._dumpling_score(0) == 1
    assert g._maki_roll_count(0) == 1
    assert g._nigiri_score(0) == 0
    assert g._dumpling_score(1) == 6
    assert g._maki_roll_count(1) == 0
    assert g._nigiri_score(1) == 6

# ARGH. NEED TO REDO THIS. INTERFACE IS ALL WRONG. 
