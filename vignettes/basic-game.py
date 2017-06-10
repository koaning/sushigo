import sushigo

players = [sushigo.player.OrderedPlayer(), sushigo.player.Player()]
game = sushigo.game.Game(players, verbose=True)
game.simulate_game()

print(game.gamelog[['action', 'game_id', 'player', 'reward', 'round', 'turn']])