from typing import Tuple

import pygame


class Properties:
    """
    Modifiable properties impacting runtime of a game.
    """

    USER_INPUTS_ENABLED: bool = True

    TEST_MODE: bool = False


class InternalProperties:
    """
    Internal properties which should be changed only with awareness.
    """

    # Display properties
    ASPECT_RATIO: float = 4 / 3

    SCREEN_WIDTH: int = 1100
    SCREEN_HEIGHT: int = int(SCREEN_WIDTH / ASPECT_RATIO)
    SCREEN_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)

    PITCH_SIZE_MUL: float = 0.8
    PITCH_WIDTH: int = int(SCREEN_WIDTH * PITCH_SIZE_MUL)
    PITCH_HEIGHT: int = int(SCREEN_HEIGHT * PITCH_SIZE_MUL)
    PITCH_SIZE: Tuple[int, int] = (PITCH_WIDTH, PITCH_HEIGHT)

    TARGET_FPS: int = 60

    BORDER_WIDTH: int = 2

    # Physics properties
    WALL_BOUNCE_FACTOR: float = 1.0

    COLLISION_SECTOR_SIZE: int = 50


class ColorPalette:
    """
    Color palette of various components in the game.
    """

    BACKGROUND: Tuple[int, int, int] = (164, 143, 91)

    PITCH_1: Tuple[int, int, int] = (113, 152, 63)
    PITCH_2: Tuple[int, int, int] = (134, 185, 80)

    BORDER: Tuple[int, int, int] = (174, 202, 137)

    TEAM_1 = (0, 0, 255)
    TEAM_2 = (255, 0, 0)
