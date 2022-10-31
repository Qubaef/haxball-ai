import pygame
import pygame.gfxdraw

from HaxballEngine.Physics.CirclePhysical import CirclePhysical
from HaxballEngine.Physics.Drawable import Drawable


class Post(CirclePhysical, Drawable):
    def __init__(self, game, px, py):
        super().__init__(game, px, py, 0, 1, 6, (0, 0, 0))
        self.to_sector_add()

    def update(self):
        pass

    def set_p(self, px, py):
        pass

    def draw(self):
        pygame.gfxdraw.filled_circle(self.engine.screen, int(self.p.x), int(self.p.y), self.size, self.color)
        pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), self.size, self.border_color)
        pygame.gfxdraw.aacircle(self.engine.screen, int(self.p.x), int(self.p.y), self.size - 1, self.border_color)
