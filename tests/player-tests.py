from sushigo import Player


def test_player_needs_name():
    p = Player("foobar")
    assert p.name == "foobar"


def test_player_needs_default_name():
    p = Player()
    assert isinstance(p.name, str)
