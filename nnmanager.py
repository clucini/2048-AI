import game
import nnai
import random

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

    def evolveNext(self, babies = 10):
        sorted_networks = sorted(self.networks, key=lambda x: x.score, reverse=True)
        fitnesses = list(n.score for n in sorted_networks)
        fitness_sum = sum(fitnesses)
        rel_fitness = [f/fitness_sum for f in fitnesses]
        probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
        new_gen = []
        for i in range(len(self.networks) - babies):
            net = sorted_networks[self.randomSelect].saveWeights()
            new_gen.append(net)

        for i in range(babies):
            net1 = sorted_networks[self.randomSelect].saveWeights()
            net2 = sorted_networks[self.randomSelect].saveWeights()
            new_gen.append(self.breed(net1, net2))

    def randomSelect(self, probs):
        rand = random.random() 
        for f in range(len(probs)):
            if rand < probs[f]:
                return f

    def breed(self, net1, net2):
        combined = self.combine(self.flatten(net1), self.flatten(net2))
        mutated = self.mutate(combined)
        baby = self.unflatten(mutated, net1)
        return baby

    def combine(self, net1, net2):
        crossover = random.randint(0, len(net1))
        baby = net1[:crossover] + net2[crossover:]
        return baby

    def mutate(self, net):
        for item in net:
            if 0.05 > random.random():
                item = 1 - item
        return net

    def flatten(self, l):
        flat_list = []
        for sublist in l:
            for sub in sublist:
                for item in sub:
                    flat_list.append(item)
        return flat_list

    def unflatten(self, l, shape):
        new_list = []
        for i in range(len(shape)):
            new_list[i] = []
            for f in range(len(shape[i])):
                new_list[i][f] = []
                for k in range(len(shape[i][f])):
                    print(str(k + f * len(shape[i][f]) + i * len(shape[i]) * len(shape[i][f])))
                    new_list[i][f][k] = l[k + f * len(shape[i][f]) + i * len(shape[i]) * len(shape[i][f])]
        return new_list

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
        game_status = board.move(network.ai.Run(inputs), False)
        if game_status == 'over':
            game_running = False
        elif game_status == 'invalid':
            invalid_count += 1
    network.score = board.score()

generations[0].evolveNext()