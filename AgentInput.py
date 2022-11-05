from typing import List

import pygame


class AgentInput:
    movementDirTranslationList: List[pygame.Vector2] = [
        pygame.Vector2(0, 0),
        pygame.Vector2(-1, 0),
        pygame.Vector2(1, 0),
        pygame.Vector2(0, -1),
        pygame.Vector2(0, 1),
        pygame.Vector2(-1, -1),
        pygame.Vector2(-1, 1),
        pygame.Vector2(1, -1),
        pygame.Vector2(1, 1),
    ]

    def __init__(self):
        self.movementDir: pygame.Vector2 = pygame.Vector2(0, 0)

        self.kick: bool = False
        self.kickPos: pygame.Vector2 = pygame.Vector2(0, 0)

        self.reset()

    def reset(self):
        self.movementDir: pygame.Vector2 = pygame.Vector2(0, 0)
        self.kick: bool = False
        self.kickPos: pygame.Vector2 = pygame.Vector2(0, 0)

    @staticmethod
    def getInputNumber():
        return len(AgentInput.movementDirTranslationList)

    def setInputByIndex(self, stateId: int) -> None:
        self.reset()

        # Set movement direction
        self.movementDir = self.movementDirTranslationList[
            stateId % len(self.movementDirTranslationList)
        ]
