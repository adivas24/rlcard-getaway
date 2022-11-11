''' Driver
'''


from rlcard.games.getaway.game import GetAwayGame
from rlcard.games.getaway.player import GetAwayPlayer

g = GetAwayGame()
# Adding players
g.add_player(GetAwayPlayer(strategy="random"))
g.add_player(GetAwayPlayer(strategy="human"))
g.add_player(GetAwayPlayer(strategy="random"))
g.add_player(GetAwayPlayer(strategy="random"))
# Init game
g.init_game()
# g.print_state()
current_lead = -1
while True:
    current_lead = g.next_round(leading_player=current_lead, verbose = True)
    # g.print_state()
    if current_lead == -1:
        break
print(g.winners)
