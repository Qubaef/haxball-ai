import pygame

from HaxballEngine.Physics.Post import Post
from HaxballEngine.Physics.Collision import Collision
from Utils.Types import Color


class Goal:
    def __init__(self, engine, color: Color, p_post_x: int, p_post_y_up: int, p_post_y_down: int, width: int, direction):
        self.engine = engine
        self.color: Color = color
        self.x: int = p_post_x
        self.y_up: int = p_post_y_up
        self.y_down: int = p_post_y_down
        self.width: int = width
        self.direction = direction

        # initialize Posts
        self.post_up: Post = Post(self.engine, self.x, self.y_up)
        self.post_down: Post = Post(self.engine, self.x, self.y_down)

    def goal_collide(self):
        Collision.collide(self.post_up)
        Collision.collide(self.post_down)

    def get_px(self):
        return self.x + self.direction * self.width

    def get_py(self):
        return self.y_up

    def get_width(self):
        return self.width

    def get_height(self):
        return self.y_down - self.y_up

    def draw(self):
        pygame.draw.rect(self.engine.screen, self.color,
            (
                self.get_px(), self.get_py(),
                self.get_width(), self.get_height()
            )
        )

        self.post_up.draw()
        self.post_down.draw()
