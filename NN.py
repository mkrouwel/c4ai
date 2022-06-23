# Created by M. Krouwel
# based on work by Milo Spencer-Harper https://github.com/miloharper/simple-neural-network
from typing import Any, List
import warnings
import numpy as np

class NN:

    __synaptic_weights : np.ndarray[Any, np.dtype[np.floating[Any]]]#List[List[float]]# : np.ndarray[np.floating]
    __numberOfInputs : int
    __numberOfOutputs : int

    def __init__(self, numberOfInputs : int, numberOfOutputs : int):
        self.__numberOfInputs = numberOfInputs
        self.__numberOfOutputs = numberOfOutputs
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
        output = np.zeros((len(dataset), self.__numberOfOutputs))

        for i in range(len(dataset)):
            input.append(dataset[i][1])
            output[i][dataset[i][0]] = 1

        X = np.array(input).reshape((-1, self.__numberOfInputs))
        #Y = to_categorical(output, num_classes=self.__numberOfOutputs)

        for _ in range(iterations):
            # Pass the training set through our neural network (a single neuron).
            NNguess = self.__think(X)
            #print(NNguess)

            # Calculate the error (The difference between the desired output and the predicted output).
            error = output - NNguess
            #print(error)

            # Multiply the error by the input and again by the gradient of the Sigmoid curve.
            # This means less confident weights are adjusted more.
            # This means inputs, which are zero, do not cause changes to the weights.
            adjustment = np.dot(X.T, error * self.__sigmoid_derivative(NNguess))
            #print(adjustment)

            # Adjust the weights.
            self.__synaptic_weights += adjustment

    def __think(self, data):
        return self.__sigmoid(np.dot(np.array(data).reshape(-1, self.__numberOfInputs), self.__synaptic_weights))

    def predict(self, data, index):
        return self.__think(data)[0][index]

    def save(self, path : str):
        np.savetxt(path, self.__synaptic_weights, delimiter=',')

    def load(self, path : str):
        self.__synaptic_weights = np.loadtxt(path, delimiter=',')
