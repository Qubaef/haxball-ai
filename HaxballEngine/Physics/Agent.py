import math

import pygame
import pygame.gfxdraw

from HaxballEngine.Physics.CirclePhysical import CirclePhysical
from HaxballEngine.Physics.Drawable import Drawable
from HaxballEngine.Properties import Properties, ColorPalette, InternalProperties
from Utils.Types import Color, TeamId


class Agent(CirclePhysical, Drawable):
    WEIGHT: float = 2
    SIZE: float = 15

    def __init__(self, engine, pos: pygame.Vector2, number: int, teamId: TeamId):
        super().__init__(engine, pos, number, self.WEIGHT, self.SIZE, ColorPalette.TEAM[teamId])
        self.teamId: TeamId = teamId

    def kick(self, pos):
        # Check if ball is in hitbox range
        for ball in self.engine.balls:
            dist = (self.p.x - ball.p.x) ** 2 + (ball.p.y - self.p.y) ** 2
            if dist <= (self.hitbox + ball.hitbox) ** 2:
                if (pos - ball.p).length() > 0:
                    ball.v = (pos - ball.p).normalize() * (pos - ball.p).length() / 12

    def draw(self):
        pygame.gfxdraw.filled_circle(self.engine.screen, int(self.p.x), int(self.p.y), int(self.size), self.color)
        pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), int(self.size), self.border_color)
        pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), int(self.size - 1), self.border_color)

        # Draw hitboxes
        if Properties.DEBUG_MODE:
            pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), int(self.hitbox), (0, 0, 255))

    def getState(self, teamDir: int):
        xPosRelative: float = abs(
            self.p.x + teamDir * InternalProperties.SCREEN_WIDTH)
        yPosRelative: float = abs(
            self.p.y + teamDir * InternalProperties.SCREEN_HEIGHT)
        # agentPosXRel: float = abs(agent.p.x + InternalProperties.TEAM_DIRS[agent.teamId] * InternalProperties.SCREEN_WIDTH) / InternalProperties.SCREEN_WIDTH
        # agentPosYRel: float = abs(agent.p.y + InternalProperties.TEAM_DIRS[agent.teamId] * InternalProperties.SCREEN_HEIGHT) / InternalProperties.SCREEN_HEIGHT

        valMultiplier: float = teamDir * 2 + 1
        xVelRelative: float = self.v.x * valMultiplier
        yVelRelative: float = self.v.y * valMultiplier
        # xVelRelative: float = self.v.x * valMultiplier / self.v_max
        # yVelRelative: float = self.v.y * valMultiplier / self.v_max

        return [xPosRelative, yPosRelative, xVelRelative, yVelRelative]
