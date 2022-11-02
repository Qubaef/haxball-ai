import pygame
import pygame.gfxdraw

from HaxballEngine.Physics.CirclePhysical import CirclePhysical
from HaxballEngine.Physics.Drawable import Drawable
from HaxballEngine.Properties import Properties, InternalProperties
from Utils.Types import Color


class Ball(CirclePhysical, Drawable):
    WEIGHT: float = 0.2
    SIZE: float = 10

    def __init__(self, game, pos: pygame.Vector2):
        super().__init__(game, pos, 0, self.WEIGHT, self.SIZE, Color(255, 255, 255))

        if not Properties.HEADLESS_MODE:
            self.ballImage = pygame.image.load("Assets/ball.png").convert_alpha()

    def draw(self):
        self.engine.screen.blit(
            self.ballImage, pygame.rect.Rect(self.p.x - self.size, self.p.y - self.size, self.size, self.size))

        # Draw hitboxes
        if Properties.DEBUG_MODE:
            pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), int(self.hitbox), (0, 0, 255))

    def getState(self, teamDir: int):
        xPosRelative: float = abs(self.p.x + teamDir * InternalProperties.SCREEN_WIDTH)
        yPosRelative: float = abs(self.p.y + teamDir * InternalProperties.SCREEN_HEIGHT)
        # agentPosXRel: float = abs(agent.p.x + teamDir * InternalProperties.SCREEN_WIDTH) / InternalProperties.SCREEN_WIDTH
        # agentPosYRel: float = abs(agent.p.y + teamDir * InternalProperties.SCREEN_HEIGHT) / InternalProperties.SCREEN_HEIGHT

        valMultiplier: float = teamDir * 2 + 1
        xVelRelative: float = self.v.x * valMultiplier
        yVelRelative: float = self.v.y * valMultiplier
        # xVelRelative: float = self.v.x * valMultiplier / self.v_max
        # yVelRelative: float = self.v.y * valMultiplier / self.v_max

        return [xPosRelative, yPosRelative, xVelRelative, yVelRelative]
