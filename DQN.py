import numpy as np
import random
import tensorflow as tf
import os
from Memory import Memory
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
import matplotlib.pyplot as plt


class DQN:

    def __init__(self, state_size, actions_number, batch_size, print_model):

        self.input_count = state_size
        self.output_count = actions_number
        self.epsilon = 1
        self.epsilon_min_val = 0.05
        self.epsilon_decay = 1e-5
        self.learning_rate = 0.001
        self.gamma = 0.95
        self.batch_size = batch_size
        self.memory = Memory(max_size=1000000, input_dims=state_size)

        self.model = self.define_model(print_model)

    def define_model(self, print_model):
        # Initialization of tensorflow model
        # RandomNormal(mean=0.0, stddev=0.05) sets network to random state (for more efficient learning)

        config = tf.compat.v1.ConfigProto(gpu_options=
                                          tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
                                          # device_count = {'GPU': 1}
                                          )
        config.gpu_options.allow_growth = True
        session = tf.compat.v1.Session(config=config)
        tf.compat.v1.keras.backend.set_session(session)

        model = tf.keras.Sequential()
        # model.add(tf.keras.layers.LeakyReLU(input_shape = (self.input_count,)))
        model.add(tf.keras.layers.Dense(16, input_dim=self.input_count, activation="tanh"))
        model.add(tf.keras.layers.Dense(32, activation="relu"))
        # model.add(tf.keras.layers.Dense(64, kernel_initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.05) ))
        model.add(tf.keras.layers.Dense(self.output_count))

        model.compile(loss= tf.keras.losses.Huber() , optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

        # save model as model.png
        # os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\bin\'
        # tf.keras.utils.plot_model(model, to_file='model.png', show_shapes = True, expand_nested = True)

        if (print_model == 1):
            print(model.summary())

        # print available devices
        # print(tf.config.list_physical_devices())

        return model

    def save_weights(self, filename):
        self.model.save_weights(filename)

    def load_weights(self, filename):
        self.model.load_weights(filename)


    # learn model from given batch
    def learn(self):
        if not self.memory.mem_count < self.batch_size:
            states, next_states, rewards, actions, dones = self.memory.sample_batch(self.batch_size)

            q_eval = self.model.predict(states)
            q_next = self.model.predict(next_states)

            q_target = np.copy(q_eval)
            batch_index = np.arange(self.batch_size, dtype=np.int32)

            q_target[batch_index, actions] = rewards + self.gamma * np.max(q_next, axis=1)

            self.model.train_on_batch(states, q_target)
            if self.epsilon > self.epsilon_min_val:
                self.epsilon -= self.epsilon_decay


    def print_model(self, accuracy):
        data = []
        for i in range(0, accuracy, 1):
            row = []
            for j in range(int(-accuracy / 2), int(accuracy / 2), 1):
                state = [i / accuracy, j / accuracy, 0.5]
                state = np.reshape(state, [1, len(state)])
                row.append(np.argmax(self.model.predict(state)))
            data.append(row)

        plt.imshow(data, cmap='gray_r', interpolation='nearest')
        plt.xlabel('Player vector')
        plt.ylabel('Player pos')
        plt.colorbar()
        plt.show(block=True)
        plt.clf()


    def save_model(self, accuracy, filepath):
        fig = plt.figure(figsize=(16, 12))

        data1 = []
        data2 = []
        data3 = []
        for i in range(0, accuracy, 1):
            row1 = []
            row2 = []
            row3 = []
            for j in range(int(-accuracy / 2), int(accuracy / 2), 1):
                state = [i / accuracy, j / accuracy, 0.5]
                state = np.reshape(state, [1, len(state)])
                state2 = [i / accuracy, 0, j / accuracy]
                state2 = np.reshape(state2, [1, len(state2)])
                pr = self.model.predict(state)
                pr2 = self.model.predict(state2)
                row2.append(np.argmax(pr))
                row3.append(np.argmax(pr2))
                if np.argmax(pr) == 0:
                    row1.append(-abs(pr[0][0]-pr[0][1]))
                else:
                    row1.append(abs(pr[0][0] - pr[0][1]))

            data1.append(row1)
            data2.append(row2)
            data3.append(row3)

        norm = mpl.colors.Normalize(vmin=5, vmax=10)

        ax1 = fig.add_subplot(131)
        im1 = ax1.imshow(data1, cmap='RdBu', interpolation='nearest',  vmin=-1, vmax=1)
        ax1.set_xlabel('Player vector')
        ax1.set_ylabel('Player pos')

        divider = make_axes_locatable(ax1)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im1, cax=cax, orientation='vertical')

        ax2 = fig.add_subplot(132)
        im2 = ax2.imshow(data2, cmap='RdBu', interpolation='nearest', vmin=0, vmax=1)
        ax2.set_xlabel('Player vector')
        ax2.set_ylabel('Player pos')

        divider = make_axes_locatable(ax2)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im2, cax=cax, orientation='vertical');

        ax3 = fig.add_subplot(133)
        im3 = ax3.imshow(data3, cmap='RdBu', interpolation='nearest', vmin=0, vmax=1)
        ax3.set_xlabel('Ball pos')
        ax3.set_ylabel('Player pos')

        divider = make_axes_locatable(ax3)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im3, cax=cax, orientation='vertical');

        # TODO
        # Fix
        # Add figure closing
        # Overwrites average reward chart
        # Saves only 10 charts to shared folder
        fig.savefig(filepath + '/' + 'model.png')
        fig.savefig(filepath + '/../' + 'plots/' + filepath[len(filepath) - 1] + 'a.png')

        file = open(filepath + '/' + 'parameters.txt', 'w')
        print('Epsilon:\t\t', self.epsilon,
              '\nEpsilon decay:\t\t', self.epsilon_decay,
              '\nLearning rate:\t\t', self.learning_rate,
              '\nGamma:\t\t\t', self.gamma,
              '\n\n\nInput size:\t\t', self.input_count,
              '\nOutput size:\t\t', self.output_count,
              file=file)
        file.close()

    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_count)  # make random move
        else:
            q_values = self.model.predict(state)  # calculate Q values for every possible move for current state using model
            return np.argmax(q_values)
