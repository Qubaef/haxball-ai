from typing import List, Dict, Any

import pygame

from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.Pitch.Goal import Goal
from HaxballEngine.Properties import InternalProperties
from Utils.Types import Color


class Team:
    def __init__(self, engine: Any, color: Color, goal: Goal, attackDir: int):
        self.engine = engine
        self.color = color
        self.goal = goal
        self.attackDir = attackDir
        self.agents: List[Agent] = []
        self.score: int = 0

        # Dictionary of initial positions for the team agents
        # Integer stands for maximum number of agents in the team
        # First layout exceeding number of agents will be used
        self.PITCH_MARGIN_X = int(
            (InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2
        )
        self.PITCH_MARGIN_Y = int(
            (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2
        )

        self.layout: Dict[int, List[pygame.Vector2]] = {
            # 1 agent - center of the pitch
            1: [pygame.Vector2(0.5, 0.5)],
            # 3 agents - center in width, 1/3 and 2/3 of the pitch height
            3: [
                pygame.Vector2(0.5, 0.25),
                pygame.Vector2(0.5, 0.5),
                pygame.Vector2(0.5, 0.75),
            ],
            # 5 agents - 1/3 and 2/3 of the pitch width, 1/3 and 2/3 of the pitch height
            5: [
                pygame.Vector2(0.25, 0.25),
                pygame.Vector2(0.25, 0.75),
                pygame.Vector2(0.5, 0.5),
                pygame.Vector2(0.75, 0.25),
                pygame.Vector2(0.75, 0.75),
            ],
            # 11 agents - 1-4-4-2 formation
            11: [
                pygame.Vector2(0.05, 0.5),
                pygame.Vector2(0.20, 0.15),
                pygame.Vector2(0.20, 0.40),
                pygame.Vector2(0.20, 0.60),
                pygame.Vector2(0.20, 0.85),
                pygame.Vector2(0.60, 0.15),
                pygame.Vector2(0.60, 0.40),
                pygame.Vector2(0.60, 0.60),
                pygame.Vector2(0.60, 0.85),
                pygame.Vector2(0.90, 0.40),
                pygame.Vector2(0.90, 0.60),
            ],
        }

    def addAgent(self, agent):
        self.agents.append(agent)
        agent.color = self.color

    def removeAgent(self, player):
        self.agents.remove(player)

    def resetScore(self):
        self.score = 0

    def addPoint(self):
        self.score += 1

    def resetPositions(self):
        # Reset positions of all agents in the team
        agentsNum: int = len(self.agents)

        # Find layout best suited for the number of agents
        layoutAgentsNum = max(self.layout.keys())
        assert agentsNum <= layoutAgentsNum, "Too many agents for the team layout"

        for targetLayout in sorted(self.layout.keys()):
            if targetLayout >= agentsNum:
                layoutAgentsNum = targetLayout
                break

        # Set positions of agents
        pitchMargin: pygame.Vector2 = pygame.Vector2(
            self.PITCH_MARGIN_X, self.PITCH_MARGIN_Y
        )

        pitchHalfSize: pygame.Vector2 = pygame.Vector2(
            InternalProperties.PITCH_WIDTH / 2, InternalProperties.PITCH_HEIGHT
        )

        for i in range(agentsNum):
            posOnPitchHalf: pygame.Vector2 = (
                pitchHalfSize.elementwise()
                * self.layout[layoutAgentsNum][i].elementwise()
            )

            onHalfPosition: pygame.Vector2 = (
                pitchMargin + posOnPitchHalf
            ) + pygame.Vector2(InternalProperties.SCREEN_SIZE) * self.attackDir
            onHalfPosition = pygame.Vector2(
                abs(onHalfPosition.x), abs(onHalfPosition.y)
            )

            self.agents[i].setMovement(pygame.Vector2(0, 0), onHalfPosition)
