from sushigo.deck import Deck, StandardDeck
from sushigo.cards import MakiCard, PuddingCard, NigiriCard, TempuraCard, SashimiCard, DumplingCard, WasabiCard


def test_deck_init():
    d = Deck(MakiCard(1), MakiCard(2))
    assert len(d.cards) == 2
    assert len(d.initial_cards) == 2


def test_deck_stop():
    d = Deck(MakiCard(1), MakiCard(2))
    _ = next(d)
    _ = next(d)
    try:
        _ = next(d)
        raise RuntimeError('Deck returns too many cards')
    except StopIteration:
        pass


def test_deck_reshuffle():
    d = Deck(MakiCard(1), MakiCard(2))
    _ = next(d)
    d.reset()
    _ = next(d)
    _ = next(d)


def test_standard_deck():
    s = StandardDeck()
    card_types = (MakiCard, PuddingCard, NigiriCard, TempuraCard, SashimiCard, DumplingCard, WasabiCard)
    x = 2
    for card_type in card_types:
        assert any(isinstance(card, card_type) for card in s.cards)
    for card in s.cards:
        assert any(isinstance(card, card_type) for card_type in card_types)
