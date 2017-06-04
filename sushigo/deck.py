import random

ALL_CARDTYPES = ["maki-1","maki-2","maki-3","pudding",
                 "egg-nigiri","salmon-nigiri","squid-nigiri",
                 "tempura","sashimi","dumpling","wasabi"]

class Card():
    def __init__(self, type, id):
        if type not in ALL_CARDTYPES:
            raise ValueError("card type does not exist")
        self.type = type
        self.id = id

    def __repr__(self):
        return "<Card id:{} type:{} @{}> at ".format(self.id, self.type, hex(id(self)))

class Deck():
    def __init__(self, maki1=7, maki2=7, maki3=7, pudding=8,
                 egg=6, salmon=6, squid=5, tempura=10,
                 sashimi=10, dumpling=15, wasabi=4):
        string_list = (['maki-1'] * maki1 +
                       ['maki-2'] * maki2 +
                       ['maki-3'] * maki3 +
                       ['pudding'] * pudding +
                       ['egg-nigiri'] * egg +
                       ['salmon-nigiri'] * salmon +
                       ['squid-nigiri'] * squid +
                       ['tempura'] * tempura +
                       ['sashimi'] *  sashimi +
                       ['dumpling'] * dumpling +
                       ['wasabi'] * wasabi)
        card_list = [Card(type=_, id=i) for i,_ in enumerate(string_list)]
        random.shuffle(card_list)
        self.cards = card_list

class StandardDeck(Deck):
    def __init__(self):
        deck = Deck()
        self.cards = deck.cards