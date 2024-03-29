from math import sqrt, cos, radians
from typing import List

import numpy as np
from pygame.math import Vector2

from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.GameEngine import GameEngine, GameState
from HaxballEngine.Physics.Ball import Ball

from AgentInput import AgentInput
from HaxballEngine.Properties import InternalProperties


class GameController:
    def __init__(self, playersInTeam: int, screen: bool = False):
        # Initialize game, ball, and players
        self.playersInTeam = playersInTeam

        self.engine = GameEngine(screen)
        self.engine.addBall()

        for i in range(playersInTeam):
            self.engine.addAgent(InternalProperties.TEAM_1_ID)
            self.engine.addAgent(InternalProperties.TEAM_2_ID)

    def nextFrame(self, inputs: List[AgentInput]) -> None:
        assert len(inputs) == len(self.engine.agents)

        # Update agents movements
        for i in range(len(inputs)):
            if inputs[i].movementDir.length() > 0:
                if self.engine.agents[i].teamId == InternalProperties.TEAM_1_ID:
                    self.engine.agents[i].addVel(inputs[i].movementDir.normalize())
                else:
                    self.engine.agents[i].addVel(-inputs[i].movementDir.normalize())

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

    def generateCurrentReward(self, targetAgentId: int, phase: int = 0) -> float:
        # Return distance to ball
        agent: Agent = self.engine.agents[targetAgentId]
        ball: Ball = self.engine.balls[0]

        angleBetweenPosAndV = (ball.p - agent.p).angle_to(agent.v)
        speedToBall = agent.v.length() * cos(radians(angleBetweenPosAndV))

        # speed Ball to goal, g
        margin = (InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2
        goal = Vector2(
            InternalProperties.SCREEN_WIDTH
            - margin
            - InternalProperties.PITCH_WIDTH
            * InternalProperties.TEAM_DIRS[agent.teamId],
            InternalProperties.SCREEN_HEIGHT / 2,
        )
        angleBetweenBallAndGoal = (goal - ball.p).angle_to(ball.v)
        speedBallToGoal = ball.v.length() * cos(radians(angleBetweenBallAndGoal))
        # TODO: to improve chance to kick ball
        if speedBallToGoal < 0:
            speedBallToGoal = 0
        # Calculate distance to ball
        distToBall = (ball.p - agent.p).length()
        # Calculate distance of boal to goal
        distToGoal = sqrt(
            pow(
                abs(
                    ball.p.x
                    + InternalProperties.SCREEN_WIDTH
                    * InternalProperties.TEAM_DIRS[agent.teamId]
                )
                - margin,
                2,
            )
            + pow(ball.p.y - InternalProperties.SCREEN_HEIGHT / 2, 2)
        )
        # distance of closest opponent to ball
        distToClosestOpponent = min(
            [
                (ball.p - opponent.p).length()
                for opponent in self.engine.agents
                if opponent.teamId != agent.teamId
            ]
        )
        # distance of closest teammate to ball
        distToClosestTeammate = min(
            [
                (ball.p - teammate.p).length()
                for teammate in self.engine.agents
                if teammate.teamId == agent.teamId
            ]
        )
        # TODO: if goal is scored - ???
        goal = 0
        if self.engine.gameState == GameState.GOAL_SCORED and distToGoal < 250:
            goal = 1000000
            print("GOAL SCORED by team: ", agent.teamId)
        elif self.engine.gameState == GameState.GOAL_SCORED and distToGoal > 250:
            goal = -1000000

        # Calculate reward for different phases
        if phase == 0:
            return (
                speedToBall
                - (int(distToBall / 50) - 4)
                + ((InternalProperties.PITCH_WIDTH / 2 - int(distToGoal)) / 25)
                + goal
                + speedBallToGoal * 20
            )
        elif phase == 1:
            return -(distToGoal + distToBall)
        elif phase == 2:
            return -(distToGoal + distToBall) + goal
        elif phase == 3:
            return -(distToGoal + distToBall + distToClosestOpponent) + goal
        elif phase == 4:
            return (
                -(
                    distToGoal
                    + distToBall
                    + distToClosestOpponent
                    + distToClosestTeammate
                )
                + goal
            )
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
