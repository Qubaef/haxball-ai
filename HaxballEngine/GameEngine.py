from typing import List, Tuple, Any

import pygame
import pygame.gfxdraw
from math import ceil

from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.Physics.Ball import Ball
from HaxballEngine.Physics.SphereCollider import SphereCollider
from HaxballEngine.Pitch.Pitch import Pitch
from HaxballEngine.Properties import Properties, InternalProperties, ColorPalette

from Utils.Types import TeamId


class GameState:
    COUNTDOWN = 0  # Game frozen, countdown to start
    RUNNING = 1  # Game running
    PAUSED = 2  # Game frozen, waiting to resume
    GOAL_SCORED = 3  # Game frozen, countdown to restart
    FINISHED = 4  # Game frozen, waiting to restart

    def __init__(self, value: int):
        self.value = value
        self._clock: int = 0

    def update(self, engine: Any, dt: int) -> None:
        if self == GameState.COUNTDOWN:
            # Update the clock
            self._clock += dt

            if self._clock >= InternalProperties.COUNTDOWN_TIME:
                self._clock = 0
                self.value = GameState.RUNNING

        elif self == GameState.GOAL_SCORED:
            # Update the clock
            self._clock += dt

            if self._clock >= InternalProperties.GOAL_SCORE_TIME:
                self._clock = 0
                self.value = GameState.COUNTDOWN
                engine.resetPositions()

    def __eq__(self, other):
        if isinstance(other, GameState):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return False


class GameEngine:
    def __init__(self):
        pygame.init()

        if not Properties.HEADLESS_MODE:
            self.screen = pygame.display.set_mode(
                InternalProperties.SCREEN_SIZE, pygame.SRCALPHA
            )

        self.gameState: GameState = GameState(GameState.COUNTDOWN)
        self.fpsClock: pygame.time.Clock = pygame.time.Clock()
        self.clock: int = 0  # in ms

        self.mousePos: pygame.Vector2 = pygame.Vector2(0, 0)

        # 2D array containing arrays, to store object in the sectors and optimise collisions
        sectorsNumY = ceil(
            InternalProperties.SCREEN_HEIGHT / InternalProperties.COLLISION_SECTOR_SIZE
        )
        sectorsNumX = ceil(
            InternalProperties.SCREEN_WIDTH / InternalProperties.COLLISION_SECTOR_SIZE
        )
        self.collisionSectors = [
            [[] for j in range(sectorsNumY)] for i in range(sectorsNumX)
        ]

        # Initialize pitch
        self.pitch: Pitch = Pitch(self)

        # List of objects and agents
        self.balls: List[Ball] = []
        self.agents: List[Agent] = []

    def drawBackground(self):
        # Draw background
        self.screen.fill(ColorPalette.BACKGROUND)

        # Draw fps
        font: pygame.font.Font = pygame.font.Font(pygame.font.get_default_font(), 13)
        fpsText: pygame.Surface = font.render(
            str(int(self.fpsClock.get_fps())), False, [0, 0, 0]
        )
        self.screen.blit(fpsText, (0, 0))

        # Draw score
        font: pygame.font.Font = pygame.font.Font(pygame.font.get_default_font(), 30)
        scoreLeft: pygame.Surface = font.render(
            str(self.pitch.teamLeft.score), False, self.pitch.teamLeft.color
        )
        scoreRight: pygame.Surface = font.render(
            str(self.pitch.teamRight.score), False, self.pitch.teamRight.color
        )

        self.screen.blit(
            scoreLeft,
            (
                InternalProperties.SCREEN_WIDTH / 10,
                InternalProperties.SCREEN_HEIGHT / 20,
            ),
        )
        self.screen.blit(
            scoreRight,
            (
                InternalProperties.SCREEN_WIDTH * 9 / 10,
                InternalProperties.SCREEN_HEIGHT / 20,
            ),
        )

        if self.gameState == GameState.GOAL_SCORED:
            status_message = font.render("GOAL!", False, (0, 0, 0))
            self.screen.blit(
                status_message,
                (
                    InternalProperties.SCREEN_WIDTH * 3 / 10,
                    InternalProperties.SCREEN_HEIGHT / 20,
                ),
            )
        elif self.gameState == GameState.RUNNING and self.clock < 500:
            status_message = font.render("PLAY!", False, (0, 0, 0))
            self.screen.blit(
                status_message,
                (
                    InternalProperties.SCREEN_WIDTH * 3 / 10,
                    InternalProperties.SCREEN_HEIGHT / 20,
                ),
            )

        # Draw pitch
        self.pitch.draw()

    def addAgent(self, teamId: TeamId = None) -> None:
        if teamId is None:
            if len(self.pitch.teamLeft.agents) >= len(self.pitch.teamRight.agents):
                teamId = InternalProperties.TEAM_1_ID
            else:
                teamId = InternalProperties.TEAM_2_ID

        if teamId in self.pitch.teams:
            agent: Agent = Agent(self, pygame.Vector2(0, 0), len(self.agents), teamId)

            # Add new agent to the game and team
            self.agents.append(agent)
            self.pitch.teams[teamId].addAgent(agent)

            self.resetPositions()

    def addBall(self):
        ball = Ball(self, pygame.Vector2(0, 0))

        # Add new ball to the game
        self.balls.append(ball)
        self.resetPositions()

    def update(self):
        # dt is time since last tick
        if InternalProperties.LOCK_FPS:
            dt: float = self.fpsClock.tick(InternalProperties.TARGET_FPS) / 1000
        else:
            self.fpsClock.tick()
            dt: float = 1 / InternalProperties.TARGET_FPS

        # Update game states
        self.clock += dt
        self.gameState.update(self, int(dt * 1000))

        # Update mouse position
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        if self.gameState == GameState.RUNNING:
            # Update objects positions and redraw players
            for agent in self.agents:
                agent.update(dt)
            for ball in self.balls:
                ball.update(dt)

            # Check collisions
            for agent in self.agents:
                SphereCollider.collide(agent)
            for ball in self.balls:
                SphereCollider.collide(ball)

            # Update walls collisions
            for agent in self.agents:
                self.wallsCollision(agent)
            for ball in self.balls:
                self.wallsCollision(ball)

            # Check collisions with posts
            self.pitch.goalLeft.goal_collide()
            self.pitch.goalRight.goal_collide()

        if not Properties.HEADLESS_MODE:
            # Redraw whole board
            self.redraw()

            # Update the screen
            pygame.display.update()

    def redraw(self):
        # Redraw board and players

        # Draw static background
        self.drawBackground()

        # If test mode is on, draw additional markers on screen
        if Properties.DEBUG_MODE:
            # Draw sectors around ball and players
            for agent in self.agents:
                sector_num = int(
                    agent.size * 4 / InternalProperties.COLLISION_SECTOR_SIZE
                )
                for i in range(
                    int(agent.p.x / InternalProperties.COLLISION_SECTOR_SIZE)
                    - sector_num,
                    int(agent.p.x / InternalProperties.COLLISION_SECTOR_SIZE)
                    + sector_num
                    + 1,
                ):
                    for j in range(
                        int(agent.p.y / InternalProperties.COLLISION_SECTOR_SIZE)
                        - sector_num,
                        int(agent.p.y / InternalProperties.COLLISION_SECTOR_SIZE)
                        + sector_num
                        + 1,
                    ):
                        pygame.draw.rect(
                            self.screen,
                            (0, 255 - ((i + j) % 2) * 50, 0),
                            (
                                int(
                                    agent.p.x / InternalProperties.COLLISION_SECTOR_SIZE
                                )
                                * InternalProperties.COLLISION_SECTOR_SIZE,
                                int(
                                    agent.p.y / InternalProperties.COLLISION_SECTOR_SIZE
                                )
                                * InternalProperties.COLLISION_SECTOR_SIZE,
                                int(InternalProperties.COLLISION_SECTOR_SIZE),
                                int(InternalProperties.COLLISION_SECTOR_SIZE),
                            ),
                        )
            for ball in self.balls:
                sector_num = int(
                    ball.size * 4 / InternalProperties.COLLISION_SECTOR_SIZE
                )
                for i in range(
                    int(ball.p.x / InternalProperties.COLLISION_SECTOR_SIZE)
                    - sector_num,
                    int(ball.p.x / InternalProperties.COLLISION_SECTOR_SIZE)
                    + sector_num
                    + 1,
                ):
                    for j in range(
                        int(ball.p.y / InternalProperties.COLLISION_SECTOR_SIZE)
                        - sector_num,
                        int(ball.p.y / InternalProperties.COLLISION_SECTOR_SIZE)
                        + sector_num
                        + 1,
                    ):
                        pygame.draw.rect(
                            self.screen,
                            (0, 255 - ((i + j) % 2) * 50, 0),
                            (
                                int(ball.p.x / InternalProperties.COLLISION_SECTOR_SIZE)
                                * InternalProperties.COLLISION_SECTOR_SIZE,
                                int(ball.p.y / InternalProperties.COLLISION_SECTOR_SIZE)
                                * InternalProperties.COLLISION_SECTOR_SIZE,
                                int(InternalProperties.COLLISION_SECTOR_SIZE),
                                int(InternalProperties.COLLISION_SECTOR_SIZE),
                            ),
                        )

        # Redraw agents
        for agent in self.agents:
            agent.draw()

        # Redraw balls
        for ball in self.balls:
            ball.draw()

        self.pitch.goalLeft.draw()
        self.pitch.goalRight.draw()

    # fix objects position, to prevent walls collisions
    def wallsCollision(self, obj):
        self.pitch.collide(obj)

    def goalScored(self, goal):
        if self.gameState.value == GameState.RUNNING:
            if goal == self.pitch.goalLeft:
                self.pitch.teamRight.addPoint()
            else:
                self.pitch.teamLeft.addPoint()

            self.gameState.value = GameState.GOAL_SCORED

    def resetPositions(self):
        self.pitch.resetPositions()

        for ball in self.balls:
            ball.setMovement(
                pygame.Vector2(0, 0),
                pygame.Vector2(
                    InternalProperties.PITCH_CENTER_X, InternalProperties.PITCH_CENTER_Y
                ),
            )

    def quit(self):
        self.agents.clear()
        self.balls.clear()
        self.collisionSectors.clear()
        pygame.quit()
