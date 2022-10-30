import pygame

from pygame.locals import *

from GameController import GameController
from HaxballEngine.AgentInput import AgentInput
from InputManager import InputManager


def startUserGameplay():
    # Initialize game
    gameController = GameController()

    shouldClose = False
    playerInput: AgentInput = AgentInput()

    # Main loop of the game
    while not shouldClose:
        # Parse user inputs
        shouldClose = InputManager.parseUserInputs(playerInput)

        # Update game state
        gameController.next_frame(playerInput)


if __name__ == "__main__":
    startUserGameplay()
