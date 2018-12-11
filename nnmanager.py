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

    def genNew(self, count = 20, weights = None):
        for i in range(count):
            if weights == None:
                self.networks.append(Network())
            else:
                self.networks.append(Network(weights[i]))
                

    def evolveNext(self, babies = 0):
        sorted_networks = sorted(self.networks, key=lambda x: x.score, reverse=True)
        fitnesses = list(n.score for n in sorted_networks)
        print(fitnesses)
        sorted_networks = sorted_networks[:int(len(sorted_networks)/2)]
        fitnesses = list(n.score for n in sorted_networks)
        fitness_sum = sum(fitnesses)

        new_gen = []
        new_gen.append(sorted_networks[0].ai.saveWeights())
        for i in range(len(self.networks)-1 - babies):
            net = sorted_networks[self.rouletteSelect(fitnesses, fitness_sum)].ai.saveWeights()
            new_gen.append(net)
        for i in range(babies):
            net1 = sorted_networks[self.rouletteSelect(fitnesses, fitness_sum)].ai.saveWeights()
            net2 = sorted_networks[self.rouletteSelect(fitnesses, fitness_sum)].ai.saveWeights()
            new_gen.append(self.breed(net1, net2))
        return new_gen
        

    def rouletteSelect(self, fitnesses, sums):
        rand = random.randint(0,sums)
        total = fitnesses[0]
        count = 0
        while rand > total:
            count += 1
            total += fitnesses[count]
        return count

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
            if 0.02 > random.random():
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
        count = 0
        for i in range(len(shape)):
            new_list.append([])
            for f in range(len(shape[i])):
                new_list[i].append([])
                for k in range(len(shape[i][f])):
                    new_list[i][f].append(l[count])
                    count += 1
        return new_list

generations = []

generations.append(Generation())
generations[0].genNew(20)
curGen = 0
while curGen < 10000:
    for network in generations[curGen].networks:
        board = game.Board()
        game_running = True
        invalid_count = 0
        while game_running:
            if invalid_count > 3:
                game_running = False
            inputs = [j for sub in board.tiles for j in sub]
            inputs.append(invalid_count)
            game_status = board.move(network.ai.Run(inputs), False)
            if game_status == 'over':
                game_running = False
            elif game_status == 'invalid':
                invalid_count += 1
        network.score = board.score()
    new = generations[curGen].evolveNext()
    next_Gen = Generation()
    next_Gen.genNew(len(new), weights=new)
    generations.append(next_Gen)
    curGen += 1

