import pygame
import math
from HaxballEngine.Ball import Ball
from HaxballEngine.CirclePhysical import CirclePhysical


class Player(CirclePhysical):
    # Object containing player's methods

    def __init__(self, game, px, py, number, color):
        super().__init__(game, px, py, number, 1, 15, color)
        self.mouse_pos = 0

    def kick(self, pos):
        # check if ball is in hitbox range
        for ball in self.game.balls:
            dist = (self.p.x - ball.p.x) ** 2 + (ball.p.y - self.p.y) ** 2
            if dist <= (self.hitbox + ball.hitbox) ** 2:
                # kick ball to given pos
                ball.v = (pos - ball.p).normalize() * (pos - ball.p).length() / 12

    def mode_ball_control(self):
        # turn down ball_control to reduce the bounce
        self.ball_control = 0.1
        self.v_max = 2 / math.pow(self.weight, 2 / 3)

    def mode_normal(self):
        # bring back normal mode
        self.ball_control = 1.0
        self.v_max = 6 / math.pow(self.weight, 2 / 3)
