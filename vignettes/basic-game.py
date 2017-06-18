import sushigo

p1 = sushigo.player.Player(name="p1")
p2 = sushigo.player.Player(name="p2")

players = [p1,p2]
game = sushigo.game.Game(players)
game.simulate_game()

df = game.gamelog
print(df[df['turn'] == 30])

print('Did player1 win? %s' % game.did_player_win("p1"))
print('Did player2 win? %s' % game.did_player_win("p2"))