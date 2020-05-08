import numpy as np
import random
import time
from GameController import GameController
from DQN import DQN

# Constants
display_mode = 1
epochs_number = 1000
frames_per_game_number = 1500
batch_size = frames_per_game_number / 6

# Load enviroment
env = GameController(display_mode)
# Initalize dqn
dqn = DQN(env.get_state_length(), env.get_action_length())

# dqn.load()

for epoch in range(epochs_number):
    env.game.game_reset()

    # get players states
    state_player1 = env.get_state_1()
    state_player2 = env.get_state_2()

    state_player1 = np.reshape(state_player1,[1, len(state_player1)])
    state_player2 = np.reshape(state_player2,[1, len(state_player2)])

    print("Epoch: ", epoch, "epsilon: ", dqn.epsilon)

    start_time = time.time()
    for frame in range(frames_per_game_number):
        
        # make actions depending on states
        action_player1 = dqn.make_move(state_player1)
        action_player2 = dqn.make_move(state_player2)

        # simulate frame
        reward, done = env.next_frame(action_player1, action_player2)
        
        # get players states
        next_state_player1 = env.get_state_1()
        next_state_player2 = env.get_state_2()

        next_state_player1 = np.reshape(next_state_player1,[1, len(next_state_player1)])
        next_state_player2 = np.reshape(next_state_player2,[1, len(next_state_player2)])

        # memorize frames
        if random.random() < (batch_size / frames_per_game_number):
            dqn.memorize(state_player1, action_player1, reward[0], next_state_player1, done)
            dqn.memorize(state_player2, action_player2, reward[1], next_state_player2, done)

        # overwrite state of the players
        state_player1 = next_state_player1
        state_player2 = next_state_player2

        if done:
            print("Epoch finished at frame: ", frame, " with result: ", done)
            break

    end_time = time.time()
    print("Game of ", frames_per_game_number, " frames simulated in ", end_time - start_time, " seconds")

    # learn and save model
    start_time = time.time()
    dqn.learn()
    dqn.save_model()
    end_time = time.time()
    print("Learning finished in ", end_time - start_time, " seconds")