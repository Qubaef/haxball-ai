from typing import List

from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.Pitch.Goal import Goal
from HaxballEngine.Properties import InternalProperties
from Utils.Types import Color


class Team:

    def __init__(self, engine, color: Color, goal: Goal, pitchHalf):
        self.engine = engine
        self.color: Color = color
        self.goal: Goal = goal
        self.pitchHalf: int = pitchHalf
        self.agents: List[Agent] = []
        self.score: int = 0

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
        i = 1
        for player in self.agents:
            pos_x = InternalProperties.SCREEN_WIDTH / 2 + self.pitchHalf * InternalProperties.PITCH_WIDTH / 4
            pos_y = (
                                InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2 + i * InternalProperties.PITCH_HEIGHT / 4
            player.set_move((0, 0), (pos_x, pos_y))
            i += 1
