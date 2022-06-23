# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
import numpy as np
from keras.layers import Dense # type: ignore
from keras.models import Sequential # type: ignore
from keras.utils import to_categorical # type: ignore
from keras.callbacks import CSVLogger # type: ignore

class ConnectFourModel:

    __numberOfInputs : int
    __batchSize : int

    def __init__(self, numberOfInputs : int, numberOfOutputs : int, batchSize : int):
        self.__numberOfInputs = numberOfInputs
        self.__batchSize = batchSize
        self.model : Sequential = Sequential()
        self.model.add(Dense(numberOfInputs, activation='relu', input_shape=(numberOfInputs,)))
        self.model.add(Dense(numberOfInputs, activation='relu'))
        self.model.add(Dense(numberOfOutputs, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])
        #self.csv_logger = CSVLogger('log.csv', append=True, separator=';')

    def train(self, dataset, iterations : int):
        input = []
        output = []
        for data in dataset:
            input.append(data[1])
            output.append(data[0])

        X = np.array(input).reshape((-1, self.__numberOfInputs))
        y = to_categorical(output, num_classes=3)
        limit = int(0.8 * len(X))
        X_train = X[:limit]
        X_test = X[limit:]
        y_train = y[:limit]
        y_test = y[limit:]
        
        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=iterations, batch_size=self.__batchSize)#, callbacks=[self.csv_logger])

    def predict(self, data, index):
        a = self.model.predict(np.array(data).reshape(-1, self.__numberOfInputs))#, callbacks=[self.csv_logger])
        #print('a: ', a)
        return a[0][index]