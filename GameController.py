import pygame
import sys
import math
import random
import itertools
import numpy as np

from pygame.locals import *
from Post import Post
from Player import Player
from GameEngine import GameEngine
from Ball import Ball


class GameController( object ):

    def __init__(self, display_mode):
        # initialize game, ball, and player
        self.game = GameEngine(display_mode)
        self.display_mode = display_mode

        self.ball = Ball(self.game, 500, 300, 0)
        self.game.new_ball(self.ball)

        self.player1 = Player(self.game, 400, 300, 1, (0, 0, 255))
        self.game.new_player(self.player1)

        self.player2 = Player(self.game, 400, 300, 1, (0, 0, 255))
        self.game.new_player(self.player2)

        self.player1_target_goal = self.game.team_left.goal.x
        self.player2_target_goal = self.game.team_right.goal.x


        # movement options
        # 0 = v(-1,-1) # 1 = v( 0,-1) # 2 = v( 1, -1)
        # 3 = v(-1, 0)                # 4 = v( 1, 0)
        # 5 = v(-1, 1) # 6 = v( 0, 1) # 7 = v( 1, 1)

        self.states_translation_array = [None] * 9
        self.states_translation_array[0] = pygame.math.Vector2(-1, -1).normalize()
        self.states_translation_array[1] = pygame.math.Vector2(0, -1).normalize()
        self.states_translation_array[2] = pygame.math.Vector2(1, -1).normalize()
        self.states_translation_array[3] = pygame.math.Vector2(-1, 0).normalize()
        self.states_translation_array[4] = pygame.math.Vector2(0, 0)
        self.states_translation_array[5] = pygame.math.Vector2(1, 0).normalize()
        self.states_translation_array[6] = pygame.math.Vector2(-1, 1).normalize()
        self.states_translation_array[7] = pygame.math.Vector2(0, 1).normalize()
        self.states_translation_array[8] = pygame.math.Vector2(1, 1).normalize()

        self.possible_inputs = list(itertools.product(range(9)))

    def next_frame(self, input_player1, input_player2):

        # Player's input is formated as follows:
        # [0] - number from range <0,7> - used to determine direction of player's movement
        # [1] - integer - used to determine if player is in ball controll mode (0 - normal mode, 1 - ball control mode)
        # [2] - integer - used to determine if player attempts to kick the ball (0 - no attempt, !0 - attempt)
        # [3] - tuple of 2 numbers (a,b) - used to kick the ball if [2] was 1

        # set players moves
        self.player1.velocity_add(self.states_translation_array[self.possible_inputs[input_player1][0]])
        self.player2.velocity_add(self.states_translation_array[self.possible_inputs[input_player2][0]])

        #self.player1.position_add(self.states_translation_array[self.possible_inputs[input_player1][0]])
        #self.player2.position_add(self.states_translation_array[self.possible_inputs[input_player2][0]])

        # manage inputs(for debug and to avoid "not responding" communicate)

        if self.display_mode == 2:
            # self.ball.p.x = pygame.mouse.get_pos()[0]
            # self.ball.p.y = pygame.mouse.get_pos()[1]

            self.game.team_left.players[0].p.x = pygame.mouse.get_pos()[0]
            self.game.team_left.players[0].p.y = pygame.mouse.get_pos()[1]
            # self.game.team_right.players[0].p.x = pygame.mouse.get_pos()[0]
            # self.game.team_right.players[0].p.y = pygame.mouse.get_pos()[1]

        if self.display_mode != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN and self.display_mode == 2:
                    print(self.get_reward()[1])


        # render next frame
        self.game.redraw()

        # analyse ball velocity vector
        # TODO


        # return rendered state pack
        return self.get_reward(), self.game.is_done()


    def get_action_length(self):
        # return length of the action
        return len(self.possible_inputs)


    def get_state_length(self):
        # returns length of the state
        return len(self.get_state_1())


    def get_state_1(self):
        # returns array of states for current frame
        # return [int(self.player1.p.x / 2), int(self.player1.p.y / 2),
        #        int(self.player1.v.x / 2), int(self.player1.v.y / 2), 
        #        int(self.player2.p.x / 2), int(self.player2.p.y / 2),
        #        int(self.player2.v.x / 2), int(self.player2.v.y / 2),
        #        int(self.ball.p.x / 2), int(self.ball.p.y / 2), 
        #        int(self.ball.v.x / 2), int(self.ball.v.y / 2),
        #        int(self.player1_target_goal / 2)]

        return np.array([self.player1.p.x / self.game.screen_w,
                        self.player1.p.y / self.game.screen_h,
                        (self.player1.v.x - self.player1.v_max) / self.player1.v_max,
                        (self.player1.v.y - self.player1.v_max) / self.player1.v_max,
                        self.ball.p.x / self.game.screen_w,  
                        self.ball.p.y / self.game.screen_h])


    def get_state_2(self):
        # returns array of states for current frame
        # return [int(self.player2.p.x / 2), int(self.player2.p.y / 2),
        #        int(self.player2.v.x / 2), int(self.player2.v.y / 2), 
        #        int(self.player1.p.x / 2), int(self.player1.p.y / 2),
        #        int(self.player1.v.x / 2), int(self.player1.v.y / 2),
        #        int(self.ball.p.x / 2), int(self.ball.p.y / 2), 
        #        int(self.ball.v.x / 2), int(self.ball.v.y / 2),
        #        int(self.player2_target_goal / 2)]

        return np.array([self.player2.p.x / self.game.screen_w,
                         self.player2.p.y / self.game.screen_h,
                         (self.player2.v.x - self.player2.v_max) / self.player2.v_max,
                         (self.player2.v.y - self.player2.v_max) / self.player2.v_max,
                         self.ball.p.x / self.game.screen_w,
                         self.ball.p.y / self.game.screen_h])

    def get_reward(self):
        # get distance between player1 and the ball
        # reward_player1 = (self.game.pitch_w - abs(self.player1.p.x + self.player1.v.x - self.ball.p.x)) / self.game.pitch_w

        # get distance between ball and the opponent's goal
        # reward_player1 += self.game.team_left.goal.get_dist(self.ball.p) / 2

        # get distance between player2 and the ball
        # reward_player2 = (self.game.pitch_w - abs(self.player2.p.x + self.player2.v.x - self.ball.p.x)) / self.game.pitch_w


        # get distance between ball and the opponent's goal
        # reward_player2 += self.game.team_right.goal.get_dist(self.ball.p) / 2

        d = math.sqrt(self.game.pitch_w**2 + self.game.pitch_h**2)
        reward_player1 = (d - (self.player1.p - self.ball.p).length()) / d
        reward_player2 = (d - (self.player2.p - self.ball.p).length()) / d

        return [reward_player1, reward_player2]


    def game_quit(self):
        self.game.quit()