from math import ceil
from typing import List

from GameController import GameController
from AgentInput import AgentInput
from HaxballEngine.Properties import InternalProperties
from InputManager import InputManager
from Utils.Plots.HeatmapPlot import HeatmapPlot
from Utils.Plots.LinePlot import LinePlot


def startUserGameplay():
    agentsInTeam: int = 11

    # Initialize game
    gameController: GameController = GameController(agentsInTeam)

    # Initialize inputs
    agentsInputs: List[AgentInput] = [AgentInput() for _ in range(agentsInTeam * 2)]

    shouldClose = False
    framesToPlay: int = 3600

    # Plots data
    frameId: int = 0
    ballPosPlot: LinePlot = LinePlot("Ball-pos", "Frame", ["X", "Y"])

    heatmapTileSize: int = 100
    ballPosHeatmap: HeatmapPlot = HeatmapPlot(
        "Ball-pos-heatmap",
        ceil(InternalProperties.SCREEN_WIDTH / heatmapTileSize),
        ceil(InternalProperties.SCREEN_HEIGHT / heatmapTileSize),
    )

    player1PosHeatmap: HeatmapPlot = HeatmapPlot(
        "Player1-pos-heatmap",
        ceil(InternalProperties.SCREEN_WIDTH / heatmapTileSize),
        ceil(InternalProperties.SCREEN_HEIGHT / heatmapTileSize),
    )

    # Main loop of the game
    while not shouldClose:
        # state0 = gameController.getState(0)
        # state1 = gameController.getState(1)
        #
        # reward = gameController.generateCurrentReward(0)

        # Move every player towards the ball
        ballPos = gameController.engine.balls[0].p
        for i in range(len(agentsInputs)):
            agentsInputs[i].movementDir = ballPos - gameController.engine.agents[i].p

        ballPosPlot.storeVal(frameId, [ballPos[0], ballPos[1]])
        ballPosHeatmap.storeVal(
            int(ballPos[0] / heatmapTileSize), int(ballPos[1] / heatmapTileSize), 1
        )
        player1PosHeatmap.storeVal(
            int(gameController.engine.agents[0].p[0] / heatmapTileSize),
            int(gameController.engine.agents[0].p[1] / heatmapTileSize),
            1,
        )

        # Update game state
        shouldClose = InputManager.parseUserInputs(gameController, agentsInputs[0])
        # gameController.engine.balls[0].set_move((0, 0), pygame.mouse.get_pos())

        gameController.nextFrame(agentsInputs)
        frameId += 1

        if frameId > framesToPlay:
            shouldClose = True

    ballPosPlot.show(True)
    ballPosHeatmap.show(True)
    player1PosHeatmap.show(True)


if __name__ == "__main__":
    startUserGameplay()
