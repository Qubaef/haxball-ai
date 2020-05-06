import pygame
import sys
import math
import random

from pygame.locals import *
from Post import Post
from Player import Player
from GameEngine import GameEngine
from Ball import Ball

class GameController( object ):

    def __init__(self):
        # initialize game, ball, and player
        self.game = GameEngine()

        self.ball = Ball(self.game, 500, 300, 0)
        self.game.new_ball(self.ball)

        self.player1 = Player(self.game, 400, 300, 1, (0, 0, 255))
        self.game.new_player(self.player1)

        self.player2 = Player(self.game, 400, 300, 1, (0, 0, 255))
        self.game.new_player(self.player2)

        # movement options
        # 0 = v(-1,-1) # 1 = v( 0,-1) # 2 = v( 1, 1)
        # 3 = v(-1, 0)                # 4 = v( 1, 0)
        # 5 = v(-1, 1) # 6 = v( 0, 1) # 7 = v( 1, 1)

        self.states_translation_array = [None] * 8
        self.states_translation_array[0] = pygame.math.Vector2(-1,-1).normalize()
        self.states_translation_array[1] = pygame.math.Vector2(0,-1).normalize()
        self.states_translation_array[2] = pygame.math.Vector2(1, 1).normalize()
        self.states_translation_array[3] = pygame.math.Vector2(-1, 0).normalize()
        self.states_translation_array[4] = pygame.math.Vector2(1, 0).normalize()
        self.states_translation_array[5] = pygame.math.Vector2(-1, 1).normalize()
        self.states_translation_array[6] = pygame.math.Vector2(0, 1).normalize()
        self.states_translation_array[7] = pygame.math.Vector2(1, 1).normalize()
        
    def next_frame(self, input_player1, input_player2):

        # Player's input is formated as follows:
        # [0] - number from range <0,7> - used to determine direction of player's movement
        # [1] - integer - used to determine if player is in ball controll mode (0 - normal mode, 1 - ball control mode)
        # [2] - integer - used to determine if player attempts to kick the ball (0 - no attempt, !0 - attempt)
        # [3] - tuple of 2 numbers (a,b) - used to kick the ball if [2] was 1

        # set players moves
        self.player1.velocity_add(self.states_translation_array[input_player1[0]])
        self.player2.velocity_add(self.states_translation_array[input_player2[0]])

        # set ball control
        if input_player1[1] == 0:
            self.player1.mode_normal()
        else:
            self.player1.mode_ball_control()

        if input_player2[1] == 0:
            self.player2.mode_normal()
        else:
            self.player2.mode_ball_control()

        # kick the ball
        if input_player1[2] == 1:
            self.player1.kick(input_player1[3])
        
        if input_player1[2] == 1:
            self.player2.kick(input_player2[3])

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

        reward_player2 = -(self.player2.p - self.ball.p).length()

        return reward_player1, reward_player2

    def game_quit(self):
        self.game.quit()
