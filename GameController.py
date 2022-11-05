from typing import List

import numpy as np

from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.GameEngine import GameEngine
from HaxballEngine.Physics.Ball import Ball

from AgentInput import AgentInput
from HaxballEngine.Properties import InternalProperties


class GameController:
    def __init__(self, playersInTeam: int):
        # Initialize game, ball, and players
        self.playersInTeam = playersInTeam
        self.engine = GameEngine()

        self.engine.addBall()

        for i in range(playersInTeam):
            self.engine.addAgent(InternalProperties.TEAM_1_ID)
            self.engine.addAgent(InternalProperties.TEAM_2_ID)

    def nextFrame(self, inputs: List[AgentInput]) -> None:
        assert len(inputs) == len(self.engine.agents)

        # Update agents movements
        for i in range(len(inputs)):
            if inputs[i].movementDir.length() > 0:
                self.engine.agents[i].addVel(inputs[i].movementDir.normalize())

        # Update ball kicks
        for i in range(len(inputs)):
            if inputs[i].kick > 0:
                self.engine.agents[i].kick(inputs[i].kickPos)

        # Render next frame
        self.engine.update()

    def getState(self, targetAgentId: int) -> np.ndarray:
        # Get target agent
        agent: Agent = self.engine.agents[targetAgentId]

        # Get teammates list
        teammates: List[Agent] = []
        for i in range(len(self.engine.agents)):
            if self.engine.agents[i].teamId == agent.teamId and i != targetAgentId:
                teammates.append(self.engine.agents[i])

        # Get opponents list
        opponents: List[Agent] = []
        for i in range(len(self.engine.agents)):
            if self.engine.agents[i].teamId != agent.teamId:
                opponents.append(self.engine.agents[i])

        # Get ball (assuming there is only one ball)
        ball: Ball = self.engine.balls[0]

        # Calculate state values
        agentState = agent.getState(InternalProperties.TEAM_DIRS[agent.teamId])

        teammatesState = np.array(
            [
                teammate.getState(InternalProperties.TEAM_DIRS[agent.teamId])
                for teammate in teammates
            ]
        )
        opponentsState = np.array(
            [
                opponent.getState(InternalProperties.TEAM_DIRS[agent.teamId])
                for opponent in opponents
            ]
        )
        ballState = ball.getState(InternalProperties.TEAM_DIRS[agent.teamId])

        state: np.array = np.array(
            [
                ballState[0],
                ballState[1],
                ballState[2],
                ballState[3],
                agentState[0],
                agentState[1],
                agentState[2],
                agentState[3],
                *teammatesState.flatten(),
                *opponentsState.flatten(),
            ]
        )

        return state

    def generateCurrentReward(self, targetAgentId: int) -> float:
        # Return distance to ball
        agent: Agent = self.engine.agents[targetAgentId]
        ball: Ball = self.engine.balls[0]

        # Vector length
        return InternalProperties.SCREEN_WIDTH / (ball.p - agent.p).length()

    def reset(self) -> None:
        self.engine = GameEngine()
        self.engine.addBall()

        for i in range(self.playersInTeam):
            self.engine.addAgent(InternalProperties.TEAM_1_ID)
            self.engine.addAgent(InternalProperties.TEAM_2_ID)

    def game_quit(self) -> None:
        self.engine.quit()
