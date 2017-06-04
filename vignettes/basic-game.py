import sushigo

players = [sushigo.player.OrderedPlayer(), sushigo.player.Player()]
game = sushigo.game.Game(players, verbose=True)
game.play_full_game()
print(game.scores)