from typing import List

import pygame

from pygame.locals import *

from GameController import GameController
from HaxballEngine.AgentInput import AgentInput
from HaxballEngine.DataStory import DataStory
from InputManager import InputManager


def startUserGameplay():
    agentsInTeam: int = 3

    # Initialize game
    gameController: GameController = GameController(agentsInTeam)

    # Initialize inputs
    agentsInputs: List[AgentInput] = [AgentInput() for _ in range(agentsInTeam * 2)]

    shouldClose = False

    # DataStory
    dataStory: DataStory = DataStory("dataStory", 10000)
    frameId: int = 0

    # Main loop of the game
    while not shouldClose:
        # Move every player towards the ball
        ballPos = gameController.ball.p
        for i in range(len(agentsInputs)):
            agentsInputs[i].movementDirection = ballPos - gameController.engine.agents[i].p

        dataStory.storeVal("ballPosX", frameId,  ballPos[0])

        if frameId % 10000 == 0:
            dataStory.plot()

        # Update game state
        shouldClose = InputManager.parseUserInputs(agentsInputs[0])

        gameController.nextFrame(agentsInputs)
        frameId += 1


if __name__ == "__main__":
    startUserGameplay()
