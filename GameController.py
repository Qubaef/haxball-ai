import pygame

from HaxballEngine.Player import Player
from HaxballEngine.GameEngine import GameEngine
from HaxballEngine.Ball import Ball

from HaxballEngine.AgentInput import AgentInput


class GameController(object):

    def __init__(self):
        # initialize game, ball, and player
        self.game = GameEngine()

        self.ball = Ball(self.game, 500, 300, 0)
        self.game.new_ball(self.ball)

        self.player1 = Player(self.game, 400, 300, 1, (0, 0, 255))
        self.game.new_player(self.player1)

        # self.player2 = Player(self.game, 400, 300, 1, (0, 0, 255))
        # self.game.new_player(self.player2)

    def next_frame(self, inputs: AgentInput):

        # set players moves
        if inputs.movementDirection.length() > 0:
            self.player1.velocity_add(inputs.movementDirection.normalize())

        self.player1.mode_normal()

        # # set ball control
        # if input_player1[1] == 0:
        #     self.player1.mode_normal()
        # else:
        #     self.player1.mode_ball_control()

        # if input_player2[1] == 0:
        #     self.player2.mode_normal()
        # else:
        #     self.player2.mode_ball_control()

        # kick the ball
        if inputs.kick is True:
            self.player1.kick(inputs.kickPos)

        # if input_player1[2] == 1:
        #     # self.player2.kick(input_player2[3])

        # render next frame
        self.game.redraw()

        # return rendered state pack
        return self.create_state_pack()

    def create_state_pack(self):
        # TODO
        return 1

    def generate_current_reward(self):
        # TODO
        reward_player1 = -(self.player1.p - self.ball.p).length()

        # reward_player2 = -(self.player2.p - self.ball.p).length()

        return reward_player1, reward_player2

    def game_quit(self):
        self.game.quit()
