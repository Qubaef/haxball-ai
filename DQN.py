import numpy as np
import random
import tensorflow as tf
import os

class DQN:

    def __init__(self, state_size, actions_number, print_model):

        self.input_count = state_size
        self.output_count = actions_number
        self.discount_factor = 0.9
        self.epsilon = 1
        self.epsilon_min_val = 0.05
        self.epsilon_decay = 0.995
        self.learning_rate = 0.01
        self.gamma = 0.95

        self.model = self.define_model(print_model)


    def define_model(self, print_model):
        # Initialization of tensorflow model
        # RandomNormal(mean=0.0, stddev=0.05) sets network to random state (for more efficient learning)

        config = tf.compat.v1.ConfigProto(gpu_options = 
                         tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
        # device_count = {'GPU': 1}
        )
        config.gpu_options.allow_growth = True
        session = tf.compat.v1.Session(config=config)
        tf.compat.v1.keras.backend.set_session(session)

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(16, input_dim = self.input_count, activation = 'relu', kernel_initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.05) ))
        model.add(tf.keras.layers.Dense(32, activation ='relu', kernel_initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.05) ))
        model.add(tf.keras.layers.Dense(64, activation ='relu', kernel_initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.05) ))
        model.add(tf.keras.layers.Dense(256, activation = 'relu', kernel_initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.05) ))
        model.add(tf.keras.layers.Dense(self.output_count, activation = 'linear', kernel_initializer=tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.05)))

        model.compile(loss='Huber', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

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
    def learn(self, batch):
        for state, action, reward, next_state, done in batch:
            target = self.model.predict(state)

            target[0][action] = reward

            if not done:
                target[0][action] += self.gamma * np.amax(self.model.predict(next_state)[0])

            # TODO?
            # self.model.fit_generate(state, target, epochs=1, verbose=0)
            self.model.fit(state, target, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min_val:
            self.epsilon *= self.epsilon_decay

        batch.clear()


    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_count)  # make random move
        else:
            q_values = self.model.predict(state)        # calculate Q values for every possible move for current state using model
            return np.argmax(q_values)
