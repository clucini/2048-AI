import game

board = game.Board()

game_running = True
while game_running:
    game_running = board.move(1)
    game_running = board.move(2)
    game_running = board.move(1)
    game_running = board.move(3)