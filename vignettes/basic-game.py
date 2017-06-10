import sushigo

players = [sushigo.player.OrderedPlayer(), sushigo.player.Player()]
game = sushigo.game.Game(players, verbose=True)
game.simulate_game()
print(game.scores)
print(game.gamelog)