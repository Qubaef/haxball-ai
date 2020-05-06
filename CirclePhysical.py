import pygame
import math
from abc import ABC

class CirclePhysical( ABC ):

    def __init__(self, game, px, py, number, weight, size, color):
        self.game = game
        self.number = number
        self.weight = weight
        self.size = size                                    # size used for drawing and collision detection
        self.hitbox = int(size * 3 / 2)                     # hitbox used for kicking the ball
        self.v_max = 6 / math.pow(self.weight, 2 / 3)       # maximum velocity is non-linear, cause ball was too fast
        self.friction = self.weight * 0.2
        self.color = color
        self.border_color = (0,0,0)
        self.p = pygame.math.Vector2(px,py)
        self.v = pygame.math.Vector2(0,0)
        self.ball_control = 1
        self.sector = (px)

    # methods

    def velocity_add(self, velocity):
        self.v += velocity

    def update(self):

        self.from_sector_remove()

        # update vectors values
        self.v += -self.v * self.friction
        self.p += self.v

        # check if velocity is not bigger than max allowed velocity
        if self.v.magnitude() > self.v_max:
            self.v = self.v.normalize() * self.v_max

        # fix object's position whith wall collsion detection
        self.game.walls_collision(self)

        self.to_sector_add()


    def from_sector_remove(self):
        # remove element from currently occupied sector
        if self in self.game.sectors[int(self.p.x / self.game.sector_size)][int(self.p.y / self.game.sector_size)]:
            self.game.sectors[int(self.p.x / self.game.sector_size)][int(self.p.y / self.game.sector_size)].remove(self)

    def to_sector_add(self):
        # add element to right sector
        self.game.sectors[int(self.p.x / self.game.sector_size)][int(self.p.y / self.game.sector_size)].append(self)


    def set_move(self, v, p):
        # set given veloctity and position
        # if given pos is less than 0, dont change it
        if p[0] >= 0 and p[1] >= 0:
            self.p.x = p[0]
            self.p.y = p[1]

        self.v.x = v[0]
        self.v.y = v[1]

    def set_p(self, px, py):
        # set p vector
        self.p.x = px
        self.p.y = py

    def get_nearby(self):
        # return list of objects located in nearby sectors

        # get number of nearby sectors (depends of object size)
        sector_num = int(self.size * 4 / self.game.sector_size)

        # iterate through sectors and gather all circles
        objects = []
        for i in range(int(self.p.x / self.game.sector_size) - sector_num, int(self.p.x / self.game.sector_size) + sector_num + 1):
            for j in range(int(self.p.y / self.game.sector_size) - sector_num, int(self.p.y / self.game.sector_size) + sector_num + 1):
                if i >= 0 and j >= 0 and i < len(self.game.sectors) and j < len(self.game.sectors[0]):
                    objects += self.game.sectors[i][j]

        return objects