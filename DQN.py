import numpy as np
import random
import tensorflow as tf
import os
from Memory import Memory
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
import matplotlib.pyplot as plt


class DQN:

    def __init__(self, state_size, actions_number, batch_size, print_model, session = None):

        self.input_count = state_size
        self.output_count = actions_number
        self.epsilon = 1
        self.epsilon_min_val = 0.05
        self.epsilon_decay = 0.9999
        self.learning_rate = 0.001
        self.gamma = 0.95
        self.batch_size = batch_size
        self.memory = Memory(max_size=1000000, input_dims=state_size)

        self.model = self.define_model(print_model, session)

    def define_model(self, print_model, session):
        # Initialization of tensorflow model
        # RandomNormal(mean=0.0, stddev=0.05) sets network to random state (for more efficient learning)

        if session is None:
            config = tf.compat.v1.ConfigProto(gpu_options=tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8))
            config.gpu_options.allow_growth = True
            self.session = tf.compat.v1.Session(config= config)
            tf.compat.v1.keras.backend.set_session(self.session)

        # probably speeds up prediction
        tf.compat.v1.disable_eager_execution()

        model = tf.keras.Sequential()
        # model.add(tf.keras.layers.LeakyReLU(input_shape = (self.input_count,)))
        model.add(tf.keras.layers.Dense(32, input_dim = self.input_count, activation="tanh"))
        model.add(tf.keras.layers.Dense(64, activation="relu"))
        model.add(tf.keras.layers.Dense(128, activation="relu"))
        model.add(tf.keras.layers.Dense(self.output_count))

        model.compile(loss= tf.keras.losses.Huber() , optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

        # save model as model.png
        # os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\bin\'
        # tf.keras.utils.plot_model(model, to_file='model.png', show_shapes = True, expand_nested = True)

        if (print_model == 1):
            print(model.summary())

        return model


    def save_weights(self, filename):
        self.model.save_weights(filename)


    def load_weights(self, filename):
        self.model.load_weights(filename).expect_partial()


    # learn model from given batch
    def learn(self):
        if not self.memory.mem_count < self.batch_size:
            states, next_states, rewards, actions, dones = self.memory.sample_batch(self.batch_size)

            q_eval = self.model.predict(states)
            q_next = self.model.predict(next_states)

            q_target = np.copy(q_eval)
            batch_index = np.arange(self.batch_size, dtype=np.int32)

            q_target[batch_index, actions] = rewards + (dones * 10) + self.gamma * np.max(q_next, axis=1)

            loss = self.model.train_on_batch(states, q_target)
            if self.epsilon > self.epsilon_min_val:
                self.epsilon *= self.epsilon_decay

            return loss
        return None


    # save model in given directory (as .txt)
    def save_model(self, accuracy, filepath, epoch_number, frames_per_game, games_per_epoch, batch_size):

        # save paramaters to .txt file
        file = open(filepath + str(epoch_number) + '/' + 'parameters' + str(epoch_number) + '.txt', 'w')
        print('Epsilon:\t\t', self.epsilon,
              '\nEpsilon decay:\t\t', self.epsilon_decay,
              '\nLearning rate:\t\t', self.learning_rate,
              '\nGamma:\t\t\t', self.gamma,
              '\n\n\nInput size:\t\t', self.input_count,
              '\nOutput size:\t\t', self.output_count,
              '\n\n\nFrames per game:\t', frames_per_game,
              '\nGames per epoch:\t', games_per_epoch,
              '\nBatch size:\t\t', batch_size,
              file=file)
        file.close()


    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_count)  # make random move
        else:
            q_values = self.model.predict(state)  # calculate Q values for every possible move for current state using model
            return np.argmax(q_values)
