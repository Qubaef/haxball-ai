import pygame
from Post import Post
from Collision import Collision

class Goal( object ):
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


    def get_dist(self, position_vector):
        if position_vector.y > self.y_up:
            return (position_vector - self.post_up.p).length()
        elif position_vector.y < self.y_down:
            return (position_vector - self.post_down.p).length()
        else:
            return (position_vector - pygame.math.Vector2(self.x,self.y_up + int(width/2))).length()

    def get_angle(self, ball_p, ball_v):
       # if ball is going towards this goal (with v > 0.5), return 1
       # if ball is going somewhere else, return number based on angle (min is -1)

       # ball_v = pygame.math.Vector2(-2, 0)
       # ball_p = pygame.math.Vector2(self.game.screen_w / 2, self.game.screen_h / 2)

       normal = pygame.math.Vector2(0, 1)

       vec_post_1 = self.post_up.p - ball_p
       vec_post_2 = self.post_down.p - ball_p

       if ball_v.length() < 0.1:
           return -1

       a1 = normal.angle_to(vec_post_1)
       if a1 < 0:
           a1 += 360

       a2 = normal.angle_to(vec_post_2)
       if a2 < 0:
           a2 += 360

       b = pygame.math.Vector2(0,1).angle_to(ball_v)
       if b < 0:
           b += 360

       if self.direction == -1:
           # if left goal
           if a2 < b < a1:
               return 1
           else:
               # return (abs(a1 - b) + abs(a2 - b)) / 360
               return -1
       elif self.direction == 0:
           # if right goal
           if a1 < b < a2:
               return 1
           else:
               # return (abs(a1 - b) + abs(a2 - b)) / 360
               return -1