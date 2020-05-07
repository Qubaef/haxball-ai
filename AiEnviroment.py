from GameController import GameController
from DQN import DQN

env = GameController()
dqn = DQN(len(env.get_state()), 32)


state = env.get_state()
moves = [0] * 32
i = 0
while(i < 10000):
    i += 1

    choice = dqn.make_move(state)
    moves[choice] += 1
    input_player1 = choice

    choice = dqn.make_move(state)
    moves[choice] += 1
    input_player2 = dqn.make_move(state)

    next_state, rewards, done = env.next_frame(input_player1, input_player2)

print(moves)