from typing import Tuple, List, Dict

import pygame

from Utils.Types import Color


class Properties:
    """
    Modifiable properties impacting runtime of a game.
    """

    USER_INPUTS_ENABLED: bool = True

    DEBUG_MODE: bool = False

    HEADLESS_MODE: bool = False


class InternalProperties:
    """
    Internal properties which should be changed only with awareness.
    """

    # Display properties
    ASPECT_RATIO: float = 4 / 3

    SCREEN_WIDTH: int = 1600
    SCREEN_HEIGHT: int = int(SCREEN_WIDTH / ASPECT_RATIO)
    SCREEN_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)

    PITCH_SIZE_MUL: float = 0.8

    PITCH_WIDTH: int = int(SCREEN_WIDTH * PITCH_SIZE_MUL)
    PITCH_HEIGHT: int = int(SCREEN_HEIGHT * PITCH_SIZE_MUL)
    PITCH_SIZE: Tuple[int, int] = (PITCH_WIDTH, PITCH_HEIGHT)

    PITCH_CENTER_X: int = int(SCREEN_WIDTH / 2)
    PITCH_CENTER_Y: int = int(SCREEN_HEIGHT / 2)
    PITCH_CENTER: Tuple[int, int] = (PITCH_CENTER_X, PITCH_CENTER_Y)

    TARGET_FPS: int = 60
    LOCK_FPS: bool = False

    BORDER_WIDTH: int = 2

    # Physics properties
    WALL_BOUNCE_FACTOR: float = 1.0

    COLLISION_SECTOR_SIZE: int = 50

    # Game logic properties
    TEAM_1_ID: int = 0
    TEAM_2_ID: int = 1

    TEAM_1_DIR: int = -1
    TEAM_2_DIR: int = 0
    TEAM_DIRS: Dict[int, int] = {TEAM_1_ID: TEAM_1_DIR, TEAM_2_ID: TEAM_2_DIR}

    COUNTDOWN_TIME: int = 0  # in ms
    GOAL_SCORE_TIME: int = 0  # in ms


class ColorPalette:
    """
    Color palette of various components in the game.
    """

    BACKGROUND: Color = (164, 143, 91)

    PITCH_1: Color = Color(113, 152, 63)
    PITCH_2: Color = Color(134, 185, 80)

    BORDER: Color = Color(174, 202, 137)

    TEAM_1: Color = Color(0, 0, 255)
    TEAM_2: Color = Color(255, 0, 0)
    TEAM: Dict[int, Color] = {
        InternalProperties.TEAM_1_ID: TEAM_1,
        InternalProperties.TEAM_2_ID: TEAM_2,
    }
