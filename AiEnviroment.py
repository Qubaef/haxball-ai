import numpy as np
from GameController import GameController
from DQN import DQN

env = GameController()
dqn = DQN(len(env.get_state()), 32)
dqn.load()

for episode in range(100):
    env.game.game_reset()
    state = env.get_state()
    state = np.reshape(state,[1, len(state)])
    print(episode)
    for t in range(200):
        input_player1 = dqn.make_move(state)
        input_player2 = dqn.make_move(state)
        next_state, reward, done = env.next_frame(input_player1, input_player2)
        next_state = np.reshape(next_state, [1, len(next_state)])
        dqn.memorize(state, input_player1, reward[0], next_state, done)
        dqn.memorize(state, input_player2, reward[1], next_state, done)
        state = next_state

        if done:
            print("Episode: ", episode)
            break
        if len(dqn.memory) % 101 == 100:
            dqn.learn(32)
    dqn.save_model()
