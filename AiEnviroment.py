import numpy as np
import random
import time
import _collections as col
import copy
import os
from threading import Thread
import matplotlib.pyplot as plt
from GameController import GameController
from DQN import DQN

# FUNCTIONS
def clone_dqn(dqn):
     # create directory

     # save weights from dqn
     dqn.save_weights(foldername + filename_copy)

     # load weights to dqn_copy
     dqn_copy = DQN(dqn.input_count, dqn.output_count, 0)
     dqn_copy.load_weights(foldername + filename_copy)

     dqn_copy.epsilon = dqn.epsilon

     # return new instance of DQN
     return dqn_copy


def play_games(games_number, frames_per_game, display_mode, dqn):
    # Load enviroment
    env = GameController(display_mode)

    for game in range(games_number):
        env.game.game_reset()
        
        # Get players states
        state_player1 = env.get_state_1()
        state_player2 = env.get_state_2()
        
        state_player1 = np.reshape(state_player1,[1, len(state_player1)])
        state_player2 = np.reshape(state_player2,[1, len(state_player2)])
        
        for frame in range(frames_per_game):
      
            # make actions depending on states
            action_player1 = dqn.make_move(state_player1)
            action_player2 = dqn.make_move(state_player2)
    
            # simulate frame
            reward, done = env.next_frame(1, action_player2)

            reward_story_1.append(reward[0])
            reward_story_2.append(reward[1])
      
            # get players states
            next_state_player1 = env.get_state_1()
            next_state_player2 = env.get_state_2()
    
            next_state_player1 = np.reshape(next_state_player1,[1, len(next_state_player1)])
            next_state_player2 = np.reshape(next_state_player2,[1, len(next_state_player2)])
    
            # memorize frames
            if random.random() < (batch_size / frames_per_game):
                batch.append((state_player1, action_player1, reward[0], next_state_player1, done))
            if random.random() < (batch_size / frames_per_game):
                batch.append((state_player2, action_player2, reward[1], next_state_player2, done))
    
            # overwrite state of the players
            state_player1 = next_state_player1
            state_player2 = next_state_player2
    
            if done:
                break

        if(display_mode == 3):
            plt.plot(range(frames_per_game), reward_story_1, 'b')
            plt.plot(range(frames_per_game), reward_story_2, 'r')
            plt.show(block = True)
        
            reward_story_1.clear()
            reward_story_2.clear()



# START

# Set to gpu
# If you dont have nvidia gpu, comment lines below
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Constants

# displayMode = 0 - no display, only console window
# displayMode = 1 - display game
# displayMode = 2 - display game; control one player with mouse; LPM displays reward for his current state
# displayMode = 3 - same as 1, but display plots
display_mode = 0

# weights folder name
foldername = "weights"

if not os.path.exists(foldername):
   os.makedirs(foldername)

# weights filename
filename_dqn = "/dqn"

# copy of weights filename
filename_copy = "/copy"

# load_model = 0 - initailize new model with random weights
# load_model = 1 - load model from file
load_model = 0

# save_model = 0 - don't save learned model after every epoch
# save_model = 1 - save learned model afetr every epoch (will overwrite previously saved model)
save_model = 1

# Number of epochs
epochs_number = 1000

# Number of games per epoch
games_per_epoch = 20

# Number of frames per game (frames_per_game / 60 = seconds in display mode)
frames_per_game = 1000

# Number of threads to procces games
threads_number = 1

# TODO?: Random shuffle
# average batch size (probability of frame being memorized in batch equals batch_size / frames_per_game)
batch_size = frames_per_game / 1

# Saved steps
batch = col.deque(maxlen = 100000)
reward_story_1 = col.deque(maxlen = frames_per_game)
reward_story_2 = col.deque(maxlen = frames_per_game)

# Load enviroment
env_for_size = GameController(display_mode)

# Initalize dqn
dqn_learn = DQN(env_for_size.get_state_length(), env_for_size.get_action_length(), 1)
if(load_model == 1):
    dqn_learn.load_weights(foldername + filename_dqn)
if(display_mode == 3):
    dqn_learn.print_model(25)

env_for_size = None



for epoch in range(epochs_number):

    # Make copy of dqn_learn to make decisions during this epoch
    # dqn_decide = clone_dqn(dqn_learn)

    print("Epoch:", epoch, "epsilon:", dqn_learn.epsilon)

    if not os.path.exists(foldername + '/' + str(epoch)):
        os.makedirs(foldername + '/' + str(epoch))
    if save_model == 1:
        dqn_learn.save_model(10, foldername + '/' + str(epoch))

    # Play games and save batch
    start_time = time.time()

    # threads = [None] * 4
    # 
    # for t in range(threads_number):
    #     threads[t] = Thread(target = play_games, args = (int(games_per_epoch / threads_number), frames_per_game, display_mode, dqn_decide,))
    #     threads[t].start()
    # 
    # # wait for all threads to finish
    # for t in range(threads_number):
    #     threads[t].join()

    play_games(games_per_epoch, frames_per_game, display_mode, dqn_learn)

    end_time = time.time()
    print(games_per_epoch, "games of", frames_per_game, "frames simulated in", end_time - start_time, "seconds")

    # Learn from data gathered in batch
    start_time = time.time()

    dqn_learn.learn(batch)

    # save weights
    if(save_model == 1):
        dqn_learn.save_weights(foldername + '/' + str(epoch) + filename_dqn)

    end_time = time.time()

    print("Learning finished in", end_time - start_time, "seconds\n")