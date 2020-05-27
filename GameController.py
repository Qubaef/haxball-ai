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
        # 1 = v(-1,-1) # 2 = v( 0,-1) # 3 = v( 1, -1)
        # 4 = v(-1, 0)                # 5 = v( 1, 0)
        # 6 = v(-1, 1) # 7 = v( 0, 1) # 8 = v( 1, 1)

        self.states_translation_array = [None] * 9
        self.states_translation_array[0] = pygame.math.Vector2(0, 0)
        self.states_translation_array[1] = pygame.math.Vector2(-1, -1).normalize()
        self.states_translation_array[2] = pygame.math.Vector2(0, -1).normalize()
        self.states_translation_array[3] = pygame.math.Vector2(1, -1).normalize()
        self.states_translation_array[4] = pygame.math.Vector2(-1, 0).normalize()
        self.states_translation_array[5] = pygame.math.Vector2(1, 0).normalize()
        self.states_translation_array[6] = pygame.math.Vector2(-1, 1).normalize()
        self.states_translation_array[7] = pygame.math.Vector2(0, 1).normalize()
        self.states_translation_array[8] = pygame.math.Vector2(1, 1).normalize()

        self.possible_inputs = list(itertools.product(range(9)))
        # self.possible_inputs = list(itertools.product(range(9), range(7)))
        # self.not_possible_inputs = list(itertools.product([0], range(1,7)))
        # self.possible_inputs = [item for item in self.possible_inputs if item not in self.not_possible_inputs]
        

    def next_frame(self, input_player1, input_player2):

        # Player's input is formated as follows:
        # [0] - number from range <0,8> - used to determine direction of player's movement and player kick (if [1] > 1)
        # [1] - number from range <0,5> - used to determine strength of ball kick

        # set players moves
        self.player1.velocity_add(self.states_translation_array[self.possible_inputs[input_player1][0]])
        self.player2.velocity_add(self.states_translation_array[self.possible_inputs[input_player2][0]])

        # kick the ball
        # kick_stats = [None, None]
        # d = math.sqrt(self.game.pitch_w ** 2 + self.game.pitch_h ** 2)
        # 
        ballkick_player1 = 0
        # if self.possible_inputs[input_player1][1] != 0:
        #     kick_stats[0] = (self.player1.p - self.ball.p).length() / d
        #     ballkick_player1 = self.player1.kick(self.ball.p + self.states_translation_array[self.possible_inputs[input_player1][0]] * 30 * self.possible_inputs[input_player1][1])
        # 
        ballkick_player2 = 0
        # if self.possible_inputs[input_player2][1] != 0:
        #     kick_stats[1] = (self.player2.p - self.ball.p).length() / d
        #     ballkick_player2 = self.player2.kick(self.ball.p + self.states_translation_array[self.possible_inputs[input_player2][0]] * 30 * self.possible_inputs[input_player2][1])


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
                    print(self.get_reward((ballkick_player1, ballkick_player2))[1])

                
        # render next frame
        self.game.redraw()

        # return rendered state pack
        return self.get_reward((ballkick_player1, ballkick_player2)), self.game.is_done()


    def get_action_length(self):
        # return length of the action
        return len(self.possible_inputs)


    def get_state_length(self):
        # returns length of the state
        if len(self.get_state_1()) == len(self.get_state_2()):
            return len(self.get_state_1())
        else:
            print("Player's states are different in size!")


    def get_state_1(self):
        # return np.array([self.player1.p.x / self.game.screen_w, self.player1.p.y / self.game.screen_h,
        #                  (self.player1.v.x - self.player1.v_max) / self.player1.v_max, (self.player1.v.y - self.player1.v_max) / self.player1.v_max,
        #                  self.player2.p.x / self.game.screen_w, self.player2.p.y / self.game.screen_h,
        #                  (self.player2.v.x - self.player2.v_max) / self.player2.v_max, (self.player2.v.y - self.player2.v_max) / self.player2.v_max,
        #                  self.ball.p.x / self.game.screen_w, self.ball.p.y / self.game.screen_h,
        #                  (self.ball.v.x - self.ball.v_max) / self.ball.v_max, (self.ball.v.y - self.ball.v_max) / self.ball.v_max,
        #                  self.player1_target_goal / self.game.screen_w])
        return np.array([self.player1.p.x / self.game.screen_w, self.player1.p.y / self.game.screen_h,
                         (self.player1.v.x - self.player1.v_max) / self.player1.v_max, (self.player1.v.y - self.player1.v_max) / self.player1.v_max,
                         self.ball.p.x / self.game.screen_w, self.ball.p.y / self.game.screen_h,
                         (self.ball.v.x - self.ball.v_max) / self.ball.v_max, (self.ball.v.y - self.ball.v_max) / self.ball.v_max,
                         self.player1_target_goal / self.game.screen_w])


    def get_state_2(self):
        # return np.array([self.player2.p.x / self.game.screen_w, self.player2.p.y / self.game.screen_h,
        #                  (self.player2.v.x - self.player2.v_max) / self.player2.v_max, (self.player2.v.y - self.player2.v_max) / self.player2.v_max,
        #                  self.player1.p.x / self.game.screen_w, self.player1.p.y / self.game.screen_h,
        #                  (self.player1.v.x - self.player1.v_max) / self.player1.v_max, (self.player1.v.y - self.player1.v_max) / self.player1.v_max,
        #                  self.ball.p.x / self.game.screen_w, self.ball.p.y / self.game.screen_h,
        #                  (self.ball.v.x - self.ball.v_max) / self.ball.v_max, (self.ball.v.y - self.ball.v_max) / self.ball.v_max,
        #                  self.player2_target_goal / self.game.screen_w])
        return np.array([self.player2.p.x / self.game.screen_w, self.player2.p.y / self.game.screen_h,
                         (self.player2.v.x - self.player2.v_max) / self.player2.v_max, (self.player2.v.y - self.player2.v_max) / self.player2.v_max,
                         self.ball.p.x / self.game.screen_w, self.ball.p.y / self.game.screen_h,
                         (self.ball.v.x - self.ball.v_max) / self.ball.v_max, (self.ball.v.y - self.ball.v_max) / self.ball.v_max,
                         self.player2_target_goal / self.game.screen_w])

    def get_reward(self, ballkicks):
        # get diagonal length
        d = math.sqrt(self.game.pitch_w ** 2 + self.game.pitch_h ** 2)

        # count reward from player-to-ball distance
        position_reward_player1 = (d - (self.player1.p - self.ball.p).length()) / d
        position_reward_player2 = (d - (self.player2.p - self.ball.p).length()) / d

        # count reward from ball-to-goal distance
        goal_reward_player1 = (d - self.game.team_left.goal.get_dist(self.ball.p)) / d
        goal_reward_player2 = (d - self.game.team_right.goal.get_dist(self.ball.p)) / d

        # count sum reward
        reward_player1 = goal_reward_player1 + position_reward_player1 * 0.2 + ballkicks[0] * 0.1
        reward_player2 = goal_reward_player2 + position_reward_player2 * 0.2 + ballkicks[1] * 0.1

        return [reward_player1, reward_player2]


    def game_quit(self):
        self.game.quit()