import pygame
from pygame.locals import *

from HaxballEngine.AgentInput import AgentInput
from HaxballEngine.Properties import Properties


class InputManager:
    KEY_EXIT = K_ESCAPE

    KEY_UP = K_w
    KEY_DOWN = K_s
    KEY_LEFT = K_a
    KEY_RIGHT = K_d

    KEY_TEST_MODE = K_t

    @staticmethod
    def parseUserInputs(userInput: AgentInput) -> bool:
        """
        Parses user inputs and returns true if the game should be closed.
        """

        shouldClose = False
        userInput.reset()

        # Parse event inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shouldClose = True
            elif event.type == pygame.KEYDOWN:
                if event.key == InputManager.KEY_TEST_MODE:
                    Properties.TEST_MODE = not Properties.TEST_MODE
            # elif event.type == pygame.KEYUP:
            #     if event.key == pygame.K_SPACE:
            #         player.mode_normal()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                userInput.kick = True
                userInput.kickPos = pygame.Vector2(pygame.mouse.get_pos())

        # Parse keyboard inputs
        pygameKeys = pygame.key.get_pressed()
        if pygameKeys[InputManager.KEY_UP]:
            userInput.movementDirection += (0, -1)
        if pygameKeys[InputManager.KEY_DOWN]:
            userInput.movementDirection += (0, 1)
        if pygameKeys[InputManager.KEY_RIGHT]:
            userInput.movementDirection += (1, 0)
        if pygameKeys[InputManager.KEY_LEFT]:
            userInput.movementDirection += (-1, 0)
        # if input[K_r]:
        #     # cross ball from left top corner position
        #     ball.set_move((15, 15), (0, 0))
        # if input[K_SPACE]:
        #     # turn on better ball control
        #     player.mode_ball_control()
        if pygameKeys[InputManager.KEY_EXIT]:
            shouldClose = True

        return shouldClose
