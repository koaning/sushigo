import sushigo

p1 = sushigo.player.OrderedPlayer()
p2 = sushigo.player.Player()

players = [p1,p2]
game = sushigo.game.Game(players, verbose=True)
game.simulate_game()
print(game.scores)
print(game.gamelog)

print('Did player1 win? %s'%(game.calc_reward(p1.name)>game.calc_reward(p2.name)))