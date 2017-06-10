import operator

def is_winner(scores, playername):
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    if sorted_scores[-1][1] == sorted_scores[-2][1]: #Indicates draw
        return 0
    if sorted_scores[-1][0] == playername:
        return 1
    else:
        return -1