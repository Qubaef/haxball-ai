import numpy as np
import random
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Embedding, Reshape
from tensorflow.keras.optimizers import Adam

class DQN:

    def __init__(self, state_pack_size, actions_number):
        self.input_size = state_pack_size
        self.output_size = actions_number

        self.discount_factor = 0.9
        self.epsilon = 1
        self.epsilon_min_val = 0.05
        self.epsilon_decay = 0.99

        # create network
        self.define_model()
        # self.session.run(self.initializer)


    def define_model(self):
        # Initialization of tensorflow model
        # I hava no idea wtf I am doing and I don't how does it work
        
        self.model = Sequential()
        self.model.add(Embedding(self.input_size, 32, input_length=1))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(self.output_size, activation='linear'))
        
        self.model.compile(loss='mse', optimizer=Adam())

        # import os
        # os.environ["PATH"] += os.pathsep + 'D:/Program Files/Graphviz2.38/bin/'
        # 
        # from tensorflow.keras.utils import plot_model
        # plot_model(self.model, to_file='model.png', show_shapes = True, expand_nested = True)

        # print(self.model.summary())


    def getQ(self, state):
        q_values = self.model.predict([[state]])         # calculate Q values for every possible move for current state using model
        return np.argmax(q_values)                       # return value with maximum Q value (return index of thr highest Q value which corresponds to a certain action)


    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_size)   # make random move
        else:
            return getQ(state) 