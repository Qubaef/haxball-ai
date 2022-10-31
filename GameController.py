from typing import List

from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.GameEngine import GameEngine
from HaxballEngine.Physics.Ball import Ball

from HaxballEngine.AgentInput import AgentInput
from HaxballEngine.Properties import InternalProperties


class GameController(object):

    def __init__(self, playersInTeam: int):
        # Initialize game, ball, and players
        self.engine = GameEngine()

        self.engine.addBall()

        for i in range(playersInTeam):
            self.engine.addAgent(InternalProperties.TEAM_1_ID)
            self.engine.addAgent(InternalProperties.TEAM_2_ID)

    def nextFrame(self, inputs: List[AgentInput]):
        assert len(inputs) == len(self.engine.agents)

        # Update agents movements
        for i in range(len(inputs)):
            if inputs[i].movementDirection.length() > 0:
                self.engine.agents[i].velocity_add(inputs[i].movementDirection.normalize())

        # Update ball kicks
        for i in range(len(inputs)):
            if inputs[i].kick > 0:
                self.engine.agents[i].kick(inputs[i].kickPos)

        # Render next frame
        self.engine.update()

    def generate_current_reward(self):
        # TODO
        raise NotImplementedError

        reward_player1 = -(self.player1.p - self.ball.p).length()
        return reward_player1

    def game_quit(self):
        self.engine.quit()
