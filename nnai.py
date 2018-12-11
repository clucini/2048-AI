import random
import numpy as np

def sigmoid(s):
    return 1/(1+np.exp(-s))

class Synapse:
    def __init__(self):
        self.weight = random.random()
        self.value = 0

class Neuron:
    def __init__(self):
        self.value = 0
        self.outSynapses = []
        self.inSynapes = []
    
    def addSynapses(self, layer):
        for neuron in layer.neurons:
            s = Synapse()
            neuron.inSynapes.append(s)
            self.outSynapses.append(s)
    
    def run(self, val = -1):
        if val != -1:
            for s in self.outSynapses:
                s.value = val
            self.value = val
        else:
            svalue = 0
            for s in self.inSynapes:
                svalue += s.value * s.weight
            svalue = sigmoid(svalue)
            for s in self.outSynapses:
                s.value = svalue
            self.value = svalue

class Layer:
    def __init__(self, count, val):
        self.neurons = []
        for i in range(count):
            self.neurons.append(Neuron())
    
    def setup(self, next):
        for n in self.neurons:
            n.addSynapses(next)

    def highestValue(self):
        highest = 0
        count = 0
        for i in range(0, len(self.neurons)):
            if self.neurons[i].val > highest:
                highest = self.neurons[i].val
                count = i
        return count

class NN:
    def __init__(self, weights = None):
        self.layers = []
        self.layers.append(Layer(17, -1))
        self.layers.append(Layer(10, 0))
        self.layers.append(Layer(4, -1))
        for i in range(0, len(self.layers)-1):
            self.layers[i].setup(self.layers[i+1])
        if weights != None:
            self.loadWeights(weights)

    def Run(self, inputs):
        for i in range(0, len(self.layers[0].neurons)):
            self.layers[0].neurons[i].run(inputs[i])
        for i in range(1, len(self.layers)):
            for f in range(0, len(self.layers[i].neurons)):
                self.layers[i].neurons[f].run()

        return self.layers[len(self.layers)-1].highestValue

    def loadWeights(self, weights):
        for layer in range(len(self.layers)):
            for neuron in range(len(self.layers[layer].neurons)):
                for synapse in range(len(self.layers[layer].neurons[neuron].outSynapses)):
                    self.layers[layer].neurons[neuron].outSynapses[synapse].weight = weights[layer][neuron][synapse]

    def saveWeights(self):
        weights = []
        for layer in range(len(self.layers)):
            weights.append([])
            for neuron in range(len(self.layers[layer].neurons)):
                weights[layer].append([])
                for synapse in self.layers[layer].neurons[neuron].outSynapses:
                    weights[layer][neuron].append(synapse.weight)
        return weights