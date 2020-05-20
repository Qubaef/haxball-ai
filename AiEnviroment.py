import numpy as np
import os, glob, time, random
from GameController import GameController
from DQN import DQN
from Stats import Stats

# FUNCTIONS
def clone_dqn(dqn):
     # save weights from dqn
     dqn.save_weights(results_foldername + '/' + filename_copy)

     # load weights to dqn_copy
     dqn_copy = DQN(dqn.input_count, dqn.output_count, dqn.batch_size, 0, dqn.session)
     dqn_copy.load_weights(results_foldername + '/' + filename_copy)

     # remove weights files
     for filename in glob.glob(results_foldername + '/' + filename_copy + '*'):
        os.remove(filename) 

     dqn_copy.epsilon = dqn.epsilon

     # return new instance of DQN
     return dqn_copy


# play given amount of games
def play_games(games_number, frames_per_game, display_mode):
    for game in range(games_number):
        # Reset enviroment
        env.game.game_reset()

        # Copy network
        # dqn_copy = clone_dqn(dqn_learn)
        
        # Get players states
        state_player1 = env.get_state_1()
        state_player2 = env.get_state_2()

        # Clear average reward
        average_reward_1 = 0
        average_reward_2 = 0

        for frame in range(frames_per_game):
      
            # Make actions depending on states (basing on network's copy)
            action_player1 = dqn_learn.make_move(np.reshape(state_player1, [1, len(state_player1)]))
            action_player2 = dqn_learn.make_move(np.reshape(state_player2, [1, len(state_player2)]))
    
            # simulate frame
            reward, done, kick_stats = env.next_frame(action_player1, 8)

            # count average reward
            if(save_charts == 1):
                average_reward_1 += reward[0] / frames_per_game
                average_reward_2 += reward[1] / frames_per_game

                stats.memorize_kicks(kick_stats[0])
                stats.memorize_kicks(kick_stats[1])
      
            # get players states
            next_state_player1 = env.get_state_1()
            next_state_player2 = env.get_state_2()
    
            # memorize frames in dqn_learn
            dqn_learn.memory.remember(state_player1, action_player1, reward[0], next_state_player1, done)
            dqn_learn.memory.remember(state_player2, action_player2, reward[1], next_state_player2, -done)
    
            # overwrite state of the players
            state_player1 = next_state_player1
            state_player2 = next_state_player2

            # Learn from saved memory and save loss to plot
            stats.memorize_loss(dqn_learn.learn())

            if done != 0:
                break

        # save average reward for this game
        if(save_charts == 1):
            stats.memorize_avg_reward(average_reward_1, average_reward_2)
        

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
results_foldername = "results"
plots_foldername = "plots"

# create folders
if not os.path.exists(results_foldername):
   os.makedirs(results_foldername)
if not os.path.exists(results_foldername + '/' + plots_foldername + '/'):
   os.makedirs(results_foldername + '/' + plots_foldername + '/')
   

# weights filename
filename_dqn = "weights"

# copy of weights filename
filename_copy = "copy"

# load_model = 0 - initailize new model with random weights
# load_model = 1 - load model from file
load_model = 0

# save_model = 0 - don't save learned model after every epoch
# save_model = 1 - save learned model afetr every epoch (will overwrite previously saved model)
save_model = 1

# save_charts = 0 - don't save charts
# save_charts = 1 - save charts after every epoch
save_charts = 1

# Number of epochs
epochs_number = 1000

# Number of games per epoch
games_per_epoch = 40

# Number of frames per game (frames_per_game / 60 = seconds in display mode)
frames_per_game = 800

# learn batch size
batch_size = int(100)


# Load enviroment
env = GameController(display_mode)


# Initalize dqn
dqn_learn = DQN(env.get_state_length(), env.get_action_length(), batch_size, 1)
if(load_model == 1):
    dqn_learn.load_weights(results_foldername + '/' + filename_dqn)

# Stats object to store data to plot
if save_charts == 1:
    stats = Stats(results_foldername, plots_foldername, frames_per_game, batch_size, games_per_epoch, dqn_learn.save_model)


# Learn main loop
for epoch in range(epochs_number):

    print("Epoch:", epoch, "epsilon:", dqn_learn.epsilon)

    if save_model == 1 or save_charts == 1:
        if not os.path.exists(results_foldername + '/' + str(epoch)):
            os.makedirs(results_foldername + '/' + str(epoch))

    # Play games and save batch
    start_time = time.time()

    play_games(games_per_epoch, frames_per_game, display_mode)

    # Clear average rewards array
    if save_charts == 1:
        stats.new_epoch()

    end_time = time.time()
    print(games_per_epoch, "games of", frames_per_game, "frames simulated in", end_time - start_time, "seconds")

    # Save weights
    if(save_model == 1):
        dqn_learn.save_weights(results_foldername + '/' + str(epoch) + '/' + filename_dqn)