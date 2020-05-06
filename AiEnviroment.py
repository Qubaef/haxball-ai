from GameController import GameController
from DQN import DQN

env = GameController()
dqn = DQN(len(env.get_state()), 32)


state = env.get_state()
while(True):
    input_player1 = dqn.make_move(state)
    input_player2 = dqn.make_move(state)
    next_state, rewards, done = env.next_frame(input_player1, input_player2)