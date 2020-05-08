import numpy as np
import random
import tensorflow as tf
import _collections as col
import os

class DQN:

    def __init__(self, state_size, actions_number):

        # set to gpu
        # if you dont have nvidia gpu, comment lines below
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"

        self.input_count = state_size
        self.output_count = actions_number
        self.memory = col.deque(maxlen = 10000)
        self.discount_factor = 0.9
        self.epsilon = 1
        self.epsilon_min_val = 0.05
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.gamma = 0.95

        self.model = self.define_model()


    def define_model(self):
        # Initialization of tensorflow model
        # I hava no idea wtf I am doing and I don't how does it work
        # Tensorflow documentation sucks for me

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim = self.input_count, activation='relu', kernel_initializer=tf.keras.initializers.RandomNormal(mean=0.0, stddev=1)))
        model.add(tf.keras.layers.Dense(48, input_dim = self.input_count, activation='relu', kernel_initializer=tf.keras.initializers.RandomNormal(mean=0.0, stddev=1)))
        model.add(tf.keras.layers.Dense(64, activation = 'relu', kernel_initializer=tf.keras.initializers.RandomNormal(mean=0.0, stddev=1)))
        model.add(tf.keras.layers.Dense(self.output_count, activation = 'linear', kernel_initializer=tf.keras.initializers.RandomNormal(mean=0.0, stddev=1)))

        model.compile(loss='Huber', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

        # save model as model.png
        # os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\bin\'
        # tf.keras.utils.plot_model(model, to_file='model.png', show_shapes = True, expand_nested = True)
        print(model.summary())

        # print available devices
        # print(tf.config.list_physical_devices())

        return model


    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def save_model(self):
        self.model.save_weights("weights.wgs")


    def load(self):
        self.model.load_weights("weights.wgs")


    def learn(self):
        for state, action, reward, next_state, done in self.memory:
            target = self.model.predict(state)

            target[0][action] = reward

            if not done:
                target[0][action] += self.gamma * np.amax(self.model.predict(next_state)[0])

            # TODO?
            # self.model.fit_generate(state, target, epochs=1, verbose=0)
            self.model.fit(state, target, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min_val:
            self.epsilon *= self.epsilon_decay

        self.memory.clear()


    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_count)  # make random move
        else:
            q_values = self.model.predict(state)        # calculate Q values for every possible move for current state using model
            return np.argmax(q_values)
