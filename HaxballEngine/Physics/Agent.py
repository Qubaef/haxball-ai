import math

import pygame
import pygame.gfxdraw

from HaxballEngine.Physics.CirclePhysical import CirclePhysical
from HaxballEngine.Physics.Drawable import Drawable
from HaxballEngine.Properties import Properties


class Agent(CirclePhysical, Drawable):
    def __init__(self, engine, px, py, number, color):
        super().__init__(engine, px, py, number, 1, 15, color)
        self.mouse_pos = 0

    def kick(self, pos):
        # check if ball is in hitbox range
        for ball in self.engine.balls:
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

    def draw(self):
        pygame.gfxdraw.filled_circle(self.engine.screen, int(self.p.x), int(self.p.y), self.size, self.color)
        pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), self.size, self.border_color)
        pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), self.size - 1, self.border_color)

        # Draw hitboxes
        if Properties.DEBUG_MODE:
            pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), self.hitbox, (0, 0, 255))
