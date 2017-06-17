from sushigo.cards import MakiCard, SashimiCard, WasabiCard, DumplingCard, PuddingCard, NigiriCard, TempuraCard
from sushigo.deck import StandardDeck


def get_score(cards, end_game=False, end_round=False):
    deck = StandardDeck()
    scorer = deck.scoring_function()
    return scorer(cards, end_game=end_game, end_round=end_round)


def test_sum_scores():
    from sushigo.cards import sum_scores
    score_a = {'a': 0, 'b': 1, 'c': 2}
    score_b = {'a': 5, 'b': 1, 'c': 8}
    summed_scores = sum_scores(score_a, score_b)
    assert summed_scores['a'] == 5
    assert summed_scores['b'] == 2
    assert summed_scores['c'] == 10
    assert len(summed_scores) == 3


def test_tempura_scores():
    cards = {
        'a': [TempuraCard()],
        'b': [TempuraCard(), TempuraCard()]
    }
    scores = get_score(cards)
    assert scores['a'] == 0
    assert scores['b'] == 5


def test_sashimi_scores():
    cards = {
        'a': [SashimiCard(), WasabiCard()],
        'b': [SashimiCard(), SashimiCard(), MakiCard(2)],
        'c': [SashimiCard(), SashimiCard(), SashimiCard(), TempuraCard()]
    }
    scores = get_score(cards)
    assert scores['a'] == 0
    assert scores['b'] == 0
    assert scores['c'] == 10


def test_nigiri_scores():
    cards = {
        'a': [NigiriCard('egg')],
        'b': [NigiriCard('squid')],
        'c': [SashimiCard(), NigiriCard('salmon'), NigiriCard('egg')]
    }
    scores = get_score(cards)
    assert scores['a'] == 1
    assert scores['b'] == 3
    assert scores['c'] == 3


def test_wasabi_scores():
    cards = {
        'a': [WasabiCard(), WasabiCard(), NigiriCard('egg'), NigiriCard('egg')],
        'b': [WasabiCard(), NigiriCard('squid')],
        'c': [SashimiCard(), NigiriCard('salmon'), NigiriCard('egg'), WasabiCard()]
    }
    scores = get_score(cards)
    assert scores['a'] == 6
    assert scores['b'] == 9
    assert scores['c'] == 3


def test_dumpling_scores():
    cards = {
        'a': [DumplingCard()],
        'b': [DumplingCard(), DumplingCard()],
        'c': [DumplingCard()]*7
    }
    scores = get_score(cards)
    assert scores['a'] == 1
    assert scores['b'] == 3
    assert scores['c'] == 15


def test_pudding_scores_2p():
    cards = {
        'a': [PuddingCard()],
        'b': [],
    }
    scores = get_score(cards)
    assert scores['a'] == 0
    scores = get_score(cards, end_round=True)
    assert scores['a'] == 0
    scores = get_score(cards, end_round=True, end_game=True)
    assert scores['a'] == 6
    assert scores['b'] == 0


def test_pudding_scores_3p():
    cards = {
        'a': [PuddingCard()],
        'b': [],
        'c': [PuddingCard()]
    }
    scores = get_score(cards)
    assert scores['a'] == 0
    scores = get_score(cards, end_round=True)
    assert scores['a'] == 0
    scores = get_score(cards, end_round=True, end_game=True)
    assert scores['a'] == 3
    assert scores['b'] == -6
    assert scores['c'] == 3


def test_maki_scores():
    cards = {
        'a': [MakiCard(3)],
        'b': [MakiCard(2)]*4,
    }
    scores = get_score(cards, end_round=True)
    assert scores['a'] == 3
    assert scores['b'] == 6
    cards = {
        'a': [MakiCard(0)],
        'b': [MakiCard(2)]*4,
    }
    scores = get_score(cards, end_round=True)
    assert scores['a'] == 0
    assert scores['b'] == 6
    cards = {
        'a': [MakiCard(3)],
        'b': [MakiCard(1)]*3,
        'c': [MakiCard(3)],
    }
    scores = get_score(cards, end_round=True)
    assert scores['a'] == 2
    assert scores['b'] == 2
    assert scores['c'] == 2


def test_complicated_score():
    cards = {
        'a': [SashimiCard(), MakiCard(2), MakiCard(1), NigiriCard('egg'),
              MakiCard(1), DumplingCard(), DumplingCard(), NigiriCard('salmon'),
              PuddingCard(), DumplingCard()],
        'b': [DumplingCard(), NigiriCard('squid'), PuddingCard(), NigiriCard('salmon'),
              WasabiCard(), SashimiCard(), NigiriCard('salmon'), PuddingCard(),
              NigiriCard('salmon'), TempuraCard()]
    }
    scores = get_score(cards, end_round=True)
    assert scores['a'] == 6+3+6
    assert scores['b'] == 0+13+1