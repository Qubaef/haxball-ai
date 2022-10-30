import pygame
from HaxballEngine.CirclePhysical import CirclePhysical


class Ball(CirclePhysical):

    def __init__(self, game, px, py, number):
        super().__init__(game, px, py, number, 0.2, 10, (255, 255, 255))
        self.ballImage = pygame.image.load("Assets/ball.png").convert_alpha()
