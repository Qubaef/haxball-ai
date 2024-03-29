from typing import Dict

import pygame
import pygame.gfxdraw

from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.Physics.Ball import Ball
from HaxballEngine.Physics.CirclePhysical import CirclePhysical
from Utils.Types import TeamId, Color

from HaxballEngine.Properties import InternalProperties, ColorPalette
from HaxballEngine.Pitch.Team import Team
from HaxballEngine.Pitch.Goal import Goal
from HaxballEngine.Physics.SphereCollider import SphereCollider


class Pitch(SphereCollider):
    PITCH_MARGIN_X: int = int(
        (InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2
    )
    PITCH_MARGIN_Y: int = int(
        (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2
    )

    PITCH_FIELD_SEGMENTS: int = 10
    PITCH_FIELD_SEGMENT_WIDTH: int = (
        InternalProperties.PITCH_WIDTH / PITCH_FIELD_SEGMENTS
    )

    PITCH_MIDDLE_CIRCLE_RADIUS: int = int(InternalProperties.PITCH_WIDTH / 10)
    PITCH_MIDDLE_CIRCLE_DRAW_ITERS: int = 3

    PITCH_PENALTY_AREA_WIDTH: int = int(InternalProperties.PITCH_WIDTH * 0.18)
    PITCH_PENALTY_AREA_HEIGHT: int = int(InternalProperties.PITCH_WIDTH * 0.44)

    PITCH_PENALTY_SPOT_MARGIN: int = int(PITCH_PENALTY_AREA_WIDTH * 0.75)

    PITCH_PENALTY_ARC_RADIUS: int = int(PITCH_PENALTY_AREA_WIDTH / 2)
    PITCH_PENALTY_ARC_DRAW_ITERS: int = 3

    def __init__(self, engine):
        self.engine = engine

        # Initialize goals
        goalYTop: int = int(
            self.PITCH_MARGIN_Y + InternalProperties.PITCH_HEIGHT * 6 / 16
        )
        goalYBot: int = int(
            self.PITCH_MARGIN_Y + InternalProperties.PITCH_HEIGHT * 10 / 16
        )

        self.goals: Dict[TeamId, Goal] = {
            InternalProperties.TEAM_1_ID: Goal(
                self.engine,
                ColorPalette.TEAM_1,
                self.PITCH_MARGIN_X,
                goalYTop,
                goalYBot,
                50,
                InternalProperties.TEAM_1_DIR,
            ),
            InternalProperties.TEAM_2_ID: Goal(
                self.engine,
                ColorPalette.TEAM_2,
                self.PITCH_MARGIN_X + InternalProperties.PITCH_WIDTH,
                goalYTop,
                goalYBot,
                50,
                InternalProperties.TEAM_2_DIR,
            ),
        }
        self.goalLeft = self.goals[InternalProperties.TEAM_1_ID]
        self.goalRight = self.goals[InternalProperties.TEAM_2_ID]

        # Initialize teams
        self.teams: Dict[TeamId, Team] = {
            InternalProperties.TEAM_1_ID: Team(
                self.engine,
                ColorPalette.TEAM_1,
                self.goalLeft,
                InternalProperties.TEAM_2_DIR,
            ),
            InternalProperties.TEAM_2_ID: Team(
                self.engine,
                ColorPalette.TEAM_2,
                self.goalRight,
                InternalProperties.TEAM_1_DIR,
            ),
        }
        self.teamLeft: Team = self.teams[InternalProperties.TEAM_1_ID]
        self.teamRight: Team = self.teams[InternalProperties.TEAM_2_ID]

    def draw(self):
        # Draw pitch

        # Draw pitch border
        pygame.draw.rect(
            self.engine.screen,
            ColorPalette.BORDER,
            (
                self.PITCH_MARGIN_X - InternalProperties.BORDER_WIDTH,
                self.PITCH_MARGIN_Y - InternalProperties.BORDER_WIDTH,
                InternalProperties.PITCH_WIDTH
                + InternalProperties.BORDER_WIDTH * 2
                - 1,
                InternalProperties.PITCH_HEIGHT
                + InternalProperties.BORDER_WIDTH * 2
                - 1,
            ),
            InternalProperties.BORDER_WIDTH,
        )

        # Draw pitch field out of vertical segments
        for i in range(0, self.PITCH_FIELD_SEGMENTS):
            segmentColor: Color = (
                ColorPalette.PITCH_1 if i % 2 == 0 else ColorPalette.PITCH_2
            )
            pygame.draw.rect(
                self.engine.screen,
                segmentColor,
                (
                    self.PITCH_MARGIN_X + i * self.PITCH_FIELD_SEGMENT_WIDTH,
                    self.PITCH_MARGIN_Y,
                    self.PITCH_FIELD_SEGMENT_WIDTH,
                    InternalProperties.PITCH_HEIGHT,
                ),
            )

        # Draw pitch lines
        # Middle line
        pygame.draw.rect(
            self.engine.screen,
            ColorPalette.BORDER,
            (
                InternalProperties.PITCH_CENTER_X - InternalProperties.BORDER_WIDTH + 1,
                self.PITCH_MARGIN_Y,
                InternalProperties.BORDER_WIDTH * 2,
                InternalProperties.PITCH_HEIGHT,
            ),
        )

        # Middle circle
        for i in range(0, self.PITCH_MIDDLE_CIRCLE_DRAW_ITERS):
            pygame.gfxdraw.aacircle(
                self.engine.screen,
                InternalProperties.PITCH_CENTER_X,
                InternalProperties.PITCH_CENTER_Y,
                self.PITCH_MIDDLE_CIRCLE_RADIUS - i,
                ColorPalette.BORDER,
            )

        # Middle dot
        pygame.gfxdraw.filled_circle(
            self.engine.screen,
            InternalProperties.PITCH_CENTER_X,
            InternalProperties.PITCH_CENTER_Y,
            InternalProperties.BORDER_WIDTH * 3,
            ColorPalette.BORDER,
        )

        # Penalty areas
        pygame.draw.rect(
            self.engine.screen,
            ColorPalette.BORDER,
            (
                self.PITCH_MARGIN_X - InternalProperties.BORDER_WIDTH,
                InternalProperties.PITCH_CENTER_Y - self.PITCH_PENALTY_AREA_HEIGHT / 2,
                self.PITCH_PENALTY_AREA_WIDTH + InternalProperties.BORDER_WIDTH,
                self.PITCH_PENALTY_AREA_HEIGHT,
            ),
            InternalProperties.BORDER_WIDTH,
        )

        pygame.draw.rect(
            self.engine.screen,
            ColorPalette.BORDER,
            (
                self.PITCH_MARGIN_X
                + InternalProperties.PITCH_WIDTH
                - self.PITCH_PENALTY_AREA_WIDTH,
                InternalProperties.PITCH_CENTER_Y - self.PITCH_PENALTY_AREA_HEIGHT / 2,
                self.PITCH_PENALTY_AREA_WIDTH + InternalProperties.BORDER_WIDTH,
                self.PITCH_PENALTY_AREA_HEIGHT,
            ),
            InternalProperties.BORDER_WIDTH,
        )

        # Penalty spots
        pygame.gfxdraw.filled_circle(
            self.engine.screen,
            self.PITCH_MARGIN_X + self.PITCH_PENALTY_SPOT_MARGIN,
            InternalProperties.PITCH_CENTER_Y,
            InternalProperties.BORDER_WIDTH * 3,
            ColorPalette.BORDER,
        )

        pygame.gfxdraw.filled_circle(
            self.engine.screen,
            self.PITCH_MARGIN_X
            + InternalProperties.PITCH_WIDTH
            - self.PITCH_PENALTY_SPOT_MARGIN,
            InternalProperties.PITCH_CENTER_Y,
            InternalProperties.BORDER_WIDTH * 3,
            ColorPalette.BORDER,
        )

        # Penalty arcs
        for i in range(0, self.PITCH_PENALTY_ARC_DRAW_ITERS):
            pygame.gfxdraw.arc(
                self.engine.screen,
                self.PITCH_MARGIN_X + self.PITCH_PENALTY_AREA_WIDTH,
                InternalProperties.PITCH_CENTER_Y,
                self.PITCH_PENALTY_ARC_RADIUS - i,
                270,
                90,
                ColorPalette.BORDER,
            )

            pygame.gfxdraw.arc(
                self.engine.screen,
                self.PITCH_MARGIN_X
                + InternalProperties.PITCH_WIDTH
                - self.PITCH_PENALTY_AREA_WIDTH,
                InternalProperties.PITCH_CENTER_Y,
                self.PITCH_PENALTY_ARC_RADIUS - i,
                90,
                270,
                ColorPalette.BORDER,
            )

    def resetPositions(self):
        self.teamLeft.resetPositions()
        self.teamRight.resetPositions()

    def collide(self, sphere: CirclePhysical) -> None:
        # Check collision with pitch walls

        # Top wall
        topWallY: float = sphere.size + Pitch.PITCH_MARGIN_Y
        if sphere.p.y < topWallY:
            sphere.setPos(pygame.Vector2(sphere.p.x, topWallY))
            sphere.v.y *= -InternalProperties.WALL_BOUNCE_FACTOR

        # Bottom wall
        bottomWallY: float = InternalProperties.PITCH_HEIGHT + (
            Pitch.PITCH_MARGIN_Y - sphere.size
        )
        if sphere.p.y > bottomWallY:
            sphere.setPos(pygame.Vector2(sphere.p.x, bottomWallY))
            sphere.v.y *= -InternalProperties.WALL_BOUNCE_FACTOR

        if isinstance(sphere, Agent):
            # Left wall
            leftWallX = sphere.size + Pitch.PITCH_MARGIN_X
            if sphere.p.x < leftWallX:
                if self.goalLeft.postDown.p.y > sphere.p.y > self.goalLeft.postUp.p.y:
                    if sphere.p.x < self.goalLeft.x:
                        sphere.setPos(pygame.Vector2(self.goalLeft.x, sphere.p.y))
                        sphere.v *= 0
                else:
                    sphere.setPos(pygame.Vector2(leftWallX, sphere.p.y))
                    sphere.v.x *= -InternalProperties.WALL_BOUNCE_FACTOR

            # Right wall
            rightWallX = InternalProperties.PITCH_WIDTH + (
                Pitch.PITCH_MARGIN_X - sphere.size
            )
            if sphere.p.x > rightWallX:
                if self.goalRight.postDown.p.y > sphere.p.y > self.goalRight.postUp.p.y:
                    if sphere.p.x > self.goalRight.x:
                        sphere.setPos(pygame.Vector2(self.goalRight.x, sphere.p.y))
                        sphere.v *= 0
                else:
                    sphere.setPos(pygame.Vector2(rightWallX, sphere.p.y))
                    sphere.v.x *= -InternalProperties.WALL_BOUNCE_FACTOR

        elif isinstance(sphere, Ball):
            # Left wall
            leftWallX = sphere.size + Pitch.PITCH_MARGIN_X
            if sphere.p.x < leftWallX:
                if self.goalLeft.postDown.p.y > sphere.p.y > self.goalLeft.postUp.p.y:
                    if sphere.p.x < self.goalLeft.x - sphere.size:
                        self.engine.goalScored(self.goalLeft)
                else:
                    sphere.setPos(pygame.Vector2(leftWallX, sphere.p.y))
                    sphere.v.x *= -InternalProperties.WALL_BOUNCE_FACTOR

            # Right wall
            rightWallX = InternalProperties.PITCH_WIDTH + (
                Pitch.PITCH_MARGIN_X - sphere.size
            )
            if sphere.p.x > rightWallX:
                if self.goalRight.postDown.p.y > sphere.p.y > self.goalRight.postUp.p.y:
                    if sphere.p.x > self.goalRight.x + sphere.size:
                        self.engine.goalScored(self.goalRight)
                else:
                    sphere.setPos(pygame.Vector2(rightWallX, sphere.p.y))
                    sphere.v.x *= -InternalProperties.WALL_BOUNCE_FACTOR
