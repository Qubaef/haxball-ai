import pygame


class AgentInput:
    def __init__(self):
        self.movementDirection: pygame.Vector2 = pygame.Vector2(0, 0)
        self.kick: bool = False
        self.kickPos: pygame.Vector2 = pygame.Vector2(0, 0)

        self.reset()

    def reset(self):
        self.movementDirection: pygame.Vector2 = pygame.Vector2(0, 0)
        self.kick: bool = False
        self.kickPos: pygame.Vector2 = pygame.Vector2(0, 0)
