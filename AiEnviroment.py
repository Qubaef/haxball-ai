from GameController import GameController
from AgentDQN import AgentDQN

env = GameController()
agent = AgentDQN(len(env.get_state()), 32)

state = env.get_state()
while(True):
    input_player1 = agent.make_move(state)
    input_player2 = agent.make_move(state)
    next_state, reward, done = env.next_frame(input_player1, input_player2)

