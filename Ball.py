import pygame
from CirclePhysical import CirclePhysical

class Ball( CirclePhysical ):

    def __init__(self, game, px, py, number):
        super().__init__(game, px, py, number, 0.2, 10, (255,255,255))
        if(game.display_mode != 0):
            self.ballImage = pygame.image.load("ball.png").convert_alpha()