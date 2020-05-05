from GameController import GameController

env = GameController()

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


while(True):
    env.next_frame(input_player1, input_player2)

