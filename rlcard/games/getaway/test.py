''' Driver
'''


from game import GetAwayGame
from player import GetAwayPlayer

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
    current_lead = g.next_round(leading_player=current_lead, verbose = False)
    # g.print_state()
    if current_lead == -1:
        break
print(g.winners)
