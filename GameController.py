from typing import List

from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.GameEngine import GameEngine
from HaxballEngine.Physics.Ball import Ball

from HaxballEngine.AgentInput import AgentInput
from HaxballEngine.Properties import InternalProperties


class GameController(object):

    def __init__(self, playersInTeam: int):
        # initialize game, ball, and player
        self.engine = GameEngine()

        self.ball = Ball(self.engine, 500, 300, 0)
        self.engine.addBall(self.ball)

        for i in range(playersInTeam):
            self.engine.addAgent(Agent(self.engine, 100 + i * 50, 100, i, 0), InternalProperties.TEAM_1_ID)
            self.engine.addAgent(Agent(self.engine, 100 + i * 50, 500, i, 1), InternalProperties.TEAM_2_ID)

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

        # self.player1.mode_normal()

        # # set ball control
        # if input_player1[1] == 0:
        #     self.player1.mode_normal()
        # else:
        #     self.player1.mode_ball_control()

        # if input_player2[1] == 0:
        #     self.player2.mode_normal()
        # else:
        #     self.player2.mode_ball_control()

        # if input_player1[2] == 1:
        #     # self.player2.kick(input_player2[3])

        # Render next frame
        self.engine.update()

    def generate_current_reward(self):
        # TODO
        raise NotImplementedError

        reward_player1 = -(self.player1.p - self.ball.p).length()
        return reward_player1

    def game_quit(self):
        self.engine.quit()
