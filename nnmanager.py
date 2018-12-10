import game
import nnai

class Network:
    def __init__(self, weights = None):
        self.score = 0
        if weights == None:
            self.ai = nnai.NN()
        else:
            self.ai = nnai.NN(weights)


class Generation:
    def __init__(self):
        self.networks = []

    def genNew(self, count = 20):
        for i in range(count):
            self.networks.append(Network())

    def evolveNext(self):
        sorted_networks = sorted(self.networks, key=lambda x: x.score, reverse=True)
        for network in sorted_networks:
            print(str(network.score))


generations = []

generations.append(Generation())
generations[0].genNew()

for network in generations[0].networks:
    board = game.Board()
    game_running = True
    invalid_count = 0
    while game_running:
        if invalid_count > 3:
            game_running = False
        inputs = [j for sub in board.tiles for j in sub]
        game_status = board.move(network.ai.Run(inputs))
        if game_status == 'over':
            game_running = False
        elif game_status == 'invalid':
            invalid_count += 1
    network.score = board.score()

generations[0].evolveNext()