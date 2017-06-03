import random

ALL_CARDTYPES = ["maki-1","maki-2","maki-3","pudding",
                 "egg-nigiri","salmon-nigiri","squid-nigiri",
                 "tempura","sashimi","dumpling"]

class Card():
    def __init__(self, type, id):
        if type not in ALL_CARDTYPES:
            raise ValueError("card type does not exist")
        self.type = type
        self.id = id

class Deck():
    def __init__(self, maki1=5, maki2=5, maki3=5, pudding=5,
                 egg=5, salmon=5, squid=5, tempura=5,
                 sashimi=5, dumpling=5, chopsticks=5):
        string_list = (['maki-1'] * maki1 +
                       ['maki-2'] * maki2 +
                       ['maki-3'] * maki3 +
                       ['pudding'] * pudding +
                       ['egg-nigiri'] * egg +
                       ['salmon-nigiri'] * salmon +
                       ['squid-nigiri'] * squid +
                       ['tempura'] * tempura +
                       ['sashimi'] *  sashimi +
                       ['dumpling'] * dumpling)
        card_list = [Card(type=_, id=i) for i,_ in enumerate(string_list)]
        random.shuffle(card_list)
        self.cards = card_list

class StandardDeck(Deck):
    def __init__(self):
        deck = Deck()
        self.cards = deck.cards