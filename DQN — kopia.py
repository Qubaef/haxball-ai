import numpy as np
import random
import tensorflow as tf

class DQN:

    def __init__(self, state_pack_size, actions_number):
        self.input_count = state_pack_size
        self.output_count = actions_number

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
        # Tensorflow documentation sucks for me
        # TODO
        return 1

    def getQ(self, state):
        # TODO
        return 1


    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_count)   # make random move
        else:
            q_values = self.model.predict(state)         # calculate Q values for every possible move for current state using model
            return np.argmax(q_values)                   # make move with maximum Q value (return index of thr highest Q value which corresponds to a certain action)