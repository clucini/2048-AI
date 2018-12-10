import game

board = game.Board()
game_status = ""
while game_status != 'over':
    a = input("Move: ")
    if int(a) not in [0,1,2,3]:
        print("Invalid key")
    else:
        game_status = board.move(int(a))