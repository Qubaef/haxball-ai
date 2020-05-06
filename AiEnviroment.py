from GameController import GameController
from AgentDQN import AgentDQN

env = GameController()
agent = AgentDQN(len(env.get_state()), 32)

input_player1 = [None] * 4
input_player1[0] = 0
input_player1[1] = 0
input_player1[2] = 0
input_player1[3] = 0

input_player2 = [None] * 4
input_player2[0] = 7
input_player2[1] = 0
input_player2[2] = 0
input_player2[3] = 0

state = env.get_state()
while(True):
    input_player1 = agent.make_move(state)
    input_player2 = agent.make_move(state)
    next_state, reward, done = env.next_frame(input_player1, input_player2)

