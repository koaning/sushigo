import sushigo
import random

def shuffle(arr):
    res = arr.copy()
    random.shuffle(res)
    return res

order = ["pudding", "squid-nigiri", "maki-3",
         "tempura", "salmon-nigiri", "dumpling", "maki-2",
         "maki-1", "egg-nigiri", "sashimi", "wasabi"]

p1_order = order
p2_order = shuffle(order)
p1 = sushigo.player.OrderedPlayer(order=p1_order)
p2 = sushigo.player.OrderedPlayer(order=p2_order)

print(p1_order)
print(p2_order)

for i in range(3):
    g = sushigo.game.Game([p1, p2])
    #print(g.game_id)
    print(g.simulate_game())
    print(g.gamelog)