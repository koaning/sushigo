from sushigo.deck import Deck, StandardDeck


def test_standard_deck_has_all_cards():
    cardtypes = ["maki-1","maki-2","maki-3","pudding",
                 "egg-nigiri","salmon-nigiri","squid-nigiri",
                 "tempura","sashimi","dumpling"]
    deck_cardtypes = [_.type for _ in StandardDeck().cards]
    for cardtype in deck_cardtypes:
        assert cardtype in cardtypes


def test_decks_automatically_shuffle():
    deck1 = Deck()
    deck2 = Deck()
    assert deck1.cards[0].id != deck2.cards[0].id