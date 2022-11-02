from typing import List

import pygame

from pygame.locals import *

from GameController import GameController
from HaxballEngine.AgentInput import AgentInput
from HaxballEngine.DataStory import DataStory
from InputManager import InputManager


def startUserGameplay():
    agentsInTeam: int = 5

    # Initialize game
    gameController: GameController = GameController(agentsInTeam)

    # Initialize inputs
    agentsInputs: List[AgentInput] = [AgentInput() for _ in range(agentsInTeam * 2)]

    shouldClose = False
    framesToPlay: int = 3600

    # DataStory
    dataStory: DataStory = DataStory("dataStory")
    frameId: int = 0

    # Main loop of the game
    while not shouldClose:
        # # Move every player towards the ball
        # ballPos = gameController.engine.balls[0].p
        # for i in range(len(agentsInputs)):
        #     agentsInputs[i].movementDirection = ballPos - gameController.engine.agents[i].p

        # dataStory.storeVal("ballPos", frameId,  [ballPos[0], ballPos[1]])

        # if frameId % 100 == 0:
        #     dataStory.plot()

        # Update game state
        shouldClose = InputManager.parseUserInputs(gameController, agentsInputs[0])
        # gameController.engine.balls[0].set_move((0, 0), pygame.mouse.get_pos())

        gameController.nextFrame(agentsInputs)
        frameId += 1

        if frameId > framesToPlay:
            shouldClose = True


if __name__ == "__main__":
    startUserGameplay()
