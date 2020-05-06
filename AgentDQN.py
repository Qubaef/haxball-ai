import numpy as np
import random

class AgentDQN:

    def __init__(self, state_size, actions_size):
        self.state_size = state_size
        self.actions_size = actions_size

        self.discount_factor = 0.9
        self.epsilon = 1
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.99

        self.model = None # Neural network

    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.actions_size) # make random move
        else:
            q_values = self.model.predict(state) # calculate Q values for every possible move for current state using model
            return np.argmax(q_values) # make move with maximum Q value (return index of thr highest Q value which corresponds to a certain action)