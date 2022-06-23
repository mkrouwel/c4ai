# Created by M. Krouwel
# based on work by Milo Spencer-Harper https://github.com/miloharper/simple-neural-network
from typing import List
import warnings
import numpy as np

class NN:

    __synaptic_weights : List[float]
    __numberOfInputs : int

    def __init__(self, numberOfInputs : int, numberOfOutputs : int):
        self.__numberOfInputs = numberOfInputs
        np.random.seed(1)
        self.__synaptic_weights = 2 * np.random.random((numberOfInputs, numberOfOutputs)) - 1

    @staticmethod
    def __sigmoid(x):
        warnings.filterwarnings('ignore')
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def __sigmoid_derivative(x):
        return x * (1 - x)

    def train(self, dataset, iterations : int):
        input = []
        output = []
        for data in dataset:
            input.append(data[1])
            output.append(data[0])

        X = np.array(input).reshape((-1, self.__numberOfInputs))
        Y = np.array(output).reshape((-1, 1))

        for _ in range(iterations):
            # Pass the training set through our neural network (a single neuron).
            NNguess = self.think(X)
            #print(NNguess)

            # Calculate the error (The difference between the desired output and the predicted output).
            error = Y - NNguess
            #print(error)

            # Multiply the error by the input and again by the gradient of the Sigmoid curve.
            # This means less confident weights are adjusted more.
            # This means inputs, which are zero, do not cause changes to the weights.
            adjustment = np.dot(X.T, error * self.__sigmoid_derivative(NNguess))
            #print(adjustment)

            # Adjust the weights.
            self.__synaptic_weights += adjustment

    def think(self, data):
        return self.__sigmoid(np.dot(np.array(data).reshape(-1, self.__numberOfInputs), self.__synaptic_weights))

    def getSW(self):
        return self.__synaptic_weights