import numpy as np
import tensorflow as tf
from tensorflow import keras


class Memory:
    def __init__(self, max_size, input_dims):
        self.max_size = max_size
        self.mem_count = 0

        self.state_memory = np.zeros((self.max_size, input_dims), dtype=np.float32)
        self.next_state_memory = np.zeros((self.max_size, input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.max_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.max_size, dtype=np.float32)
        self.done_memory = np.zeros(self.max_size, dtype=np.int32)

    def remember(self, state, action, reward, next_state, done):
        index = self.mem_count % self.max_size
        self.state_memory[index] = state
        self.next_state_memory[index] = next_state
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.done_memory[index] = done
        self.mem_count += 1

    def sample_batch(self, batch_size):
        max_index = min(self.mem_count, self.max_size)
        batch = np.random.choice(max_index, batch_size, replace=False)

        states = self.state_memory[batch]
        next_states = self.next_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        dones = self.done_memory[batch]

        return states, next_states, rewards, actions, dones
