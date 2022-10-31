from typing import Tuple

import pygame

from HaxballEngine.Physics.Drawable import Drawable
from HaxballEngine.Physics.Post import Post
from HaxballEngine.Physics.Collision import Collision
from HaxballEngine.Properties import Properties
from Utils.Types import Color


class Goal(Drawable):
    def __init__(self, engine, color: Color, p_post_x: int, p_post_y_up: int, p_post_y_down: int, width: int,
            direction: int):
        self.engine = engine
        self.color: Color = color
        self.x: int = p_post_x
        self.y_up: int = p_post_y_up
        self.y_down: int = p_post_y_down
        self.width: int = width
        self.direction: int = direction

        # Load goal image
        if not Properties.HEADLESS_MODE:
            if direction == -1:
                self.goalImage = pygame.image.load("Assets/goal_left.png").convert_alpha()
            elif direction == 0:
                self.goalImage = pygame.image.load("Assets/goal_right.png").convert_alpha()

            imageSize: Tuple[int, int] = (self.width, self.y_down - self.y_up)
            self.goalImage = pygame.transform.scale(self.goalImage, imageSize)

        # Initialize Posts
        self.postUp: Post = Post(self.engine, self.x, self.y_up, self.color)
        self.postDown: Post = Post(self.engine, self.x, self.y_down, self.color)

    def goal_collide(self):
        Collision.collide(self.postUp)
        Collision.collide(self.postDown)

    def get_px(self):
        return self.x + self.direction * self.width

    def get_py(self):
        return self.y_up

    def get_width(self):
        return self.width

    def get_height(self):
        return self.y_down - self.y_up

    def draw(self):
        self.engine.screen.blit(self.goalImage,
            pygame.rect.Rect(
                self.get_px(), self.get_py() - 3,
                self.get_width(), self.get_height()
            )
        )

        self.postUp.draw()
        self.postDown.draw()
