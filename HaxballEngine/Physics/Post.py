import pygame
import pygame.gfxdraw

from HaxballEngine.Physics.CirclePhysical import CirclePhysical
from HaxballEngine.Physics.Drawable import Drawable
from Utils.Types import Color


class Post(CirclePhysical, Drawable):
    def __init__(self, game, pos: pygame.Vector2, color: Color):
        super().__init__(game, pos, 0, 1, 6, color)
        self.toSectorAdd()

    def update(self, dt: float):
        self.v = pygame.Vector2(0, 0)
        pass

    def setPos(self, pos: pygame.Vector2):
        pass

    def draw(self):
        pygame.gfxdraw.filled_circle(self.engine.screen, int(self.p.x), int(self.p.y), int(self.size), self.color)
        pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), int(self.size), self.border_color)
        pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), int(self.size - 1), self.border_color)
