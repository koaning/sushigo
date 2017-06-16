from sushigo.cards import Card, MakiCard, SashimiCard, WasabiCard, DumplingCard, PuddingCard, NigiriCard, TempuraCard


def test_sum_scores():
    from sushigo.cards import sum_scores
    score_a = {'a': 0, 'b': 1, 'c': 2}
    score_b = {'a': 5, 'b': 1, 'c': 8}
    summed_scores = sum_scores(score_a, score_b)
    assert summed_scores['a'] == 5
    assert summed_scores['b'] == 2
    assert summed_scores['c'] == 10
    assert len(summed_scores) == 3
