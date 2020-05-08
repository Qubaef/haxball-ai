import numpy as np
from GameController import GameController
from DQN import DQN
import os

# set to gpu
# if you dont have nvidia gpu, comment lines below
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

env = GameController()
dqn = DQN(len(env.get_state()), 32)
# dqn.load()

moves = [0] * 32

for epoch in range(1000):
    env.game.game_reset()
    state = env.get_state()
    state = np.reshape(state,[1, len(state)])
    print("Epoch: " + str(epoch))
    for t in range(1000):
        
        input_player1 = dqn.make_move(state)
        input_player2 = dqn.make_move(state)

        next_state, reward, done = env.next_frame(input_player1, input_player2)
        next_state = np.reshape(next_state, [1, len(next_state)])

        # TODO: change way of randomising values
        dqn.memorize(state, input_player1, reward[0], next_state, done)
        dqn.memorize(state, input_player2, reward[1], next_state, done)
        state = next_state

        if done:
            print("Episode: ", episode)
            break
        if len(dqn.memory) % 501 == 500:
            dqn.learn(60)
    dqn.save_model()
