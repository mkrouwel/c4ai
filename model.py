# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
import numpy as np
from keras.layers import Dense # type: ignore
from keras.models import Sequential # type: ignore
from keras.utils import to_categorical # type: ignore
from keras.callbacks import CSVLogger # type: ignore
from tensorflow import keras # type: ignore

class ConnectFourModel:

    __numberOfInputs : int
    __numberOfOutputs : int
    __batchSize : int
    __model : Sequential

    def __init__(self, numberOfInputs : int, numberOfOutputs : int, batchSize : int):
        self.__numberOfInputs = numberOfInputs
        self.__numberOfOutputs = numberOfOutputs
        self.__batchSize = batchSize
        self.__model = Sequential()
        self.__model.add(Dense(numberOfInputs, activation='relu', input_shape=(numberOfInputs,)))
        self.__model.add(Dense(numberOfInputs, activation='relu'))
        self.__model.add(Dense(numberOfOutputs, activation='softmax'))
        self.__model.compile(loss='categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])
        #self.csv_logger = CSVLogger('log.csv', append=True, separator=';')

    def train(self, dataset, iterations : int):
        input = []
        output = []
        for data in dataset:
            input.append(data[1])
            output.append(data[0])

        X = np.array(input).reshape((-1, self.__numberOfInputs))
        #print(output)
        y = to_categorical(output, num_classes=self.__numberOfOutputs)
        #print(y)
        limit = int(0.8 * len(X))
        X_train = X[:limit]
        X_test = X[limit:]
        y_train = y[:limit]
        y_test = y[limit:]
        
        self.__model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=iterations, batch_size=self.__batchSize)#, callbacks=[self.csv_logger])

    def predict(self, data, index):
        
        print('DATA: ', data)
        #print('MODEL', self.__model.)
        print('HERE: ', np.array(data).reshape(-1, self.__numberOfInputs))
        a = self.__model.predict(np.array(data).reshape(-1, self.__numberOfInputs))#, callbacks=[self.csv_logger])
        print('a: ', a)# type(a[0][0]))
        return a[0][index]

    def save(self, path : str):
        self.__model.save(path)

    def load(self, path : str):
        self.__model = keras.models.load_model(path)