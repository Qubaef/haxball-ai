from HaxballEngine.Post import Post
from HaxballEngine.Collision import Collision


class Goal:
    def __init__(self, game, color, p_post_x, p_post_y_up, p_post_y_down, width, direction):
        self.game = game
        self.color = color
        self.x = p_post_x
        self.y_up = p_post_y_up
        self.y_down = p_post_y_down
        self.width = width
        self.direction = direction

        # initialize Posts
        self.post_up = Post(self.game, self.x, self.y_up)
        self.post_down = Post(self.game, self.x, self.y_down)

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
