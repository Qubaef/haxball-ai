from typing import List, Tuple

import pygame
import math
from abc import ABC

import pygame.gfxdraw

from HaxballEngine.Properties import InternalProperties
from Utils.Types import Color


class CirclePhysical(ABC):

    def __init__(self, engine, pos: pygame.Vector2, number: int, weight: float, size: float, color: Color):
        self.engine = engine
        self.number: int = number
        self.weight: float = weight
        self.size: float = size  # size used for drawing and collision detection
        self.hitbox: float = int(size * 3 / 2)  # radius of hitbox used for kicking the ball
        self.v_max = 8 / math.pow(self.weight, 2 / 3)  # maximum velocity is non-linear, cause ball was too fast
        self.friction = self.weight * 0.2
        self.color: Color = color
        self.border_color: Color = Color(0, 0, 0)

        self.ball_control = 1

        self.v: pygame.Vector2 = pygame.math.Vector2(0, 0)
        self.p: pygame.Vector2 = pos

    def setPos(self, pos: pygame.Vector2):
        self.p = pos

    def setVel(self, vel: pygame.Vector2):
        self.v = vel

    def addVel(self, vel: pygame.Vector2):
        self.v += vel * self.weight

    def setMovement(self, vel: pygame.Vector2, pos: pygame.Vector2):
        # Set given velocity and position
        # If given pos is less than 0, don't change it
        if pos.x >= 0 and pos.y >= 0:
            self.setPos(pos)

        self.setVel(vel)

    def update(self, dt: float):
        self.fromSectorRemove()

        dt: float = dt * InternalProperties.TARGET_FPS

        # Update vectors values
        self.v += -self.v * self.friction * dt
        self.p += self.v * dt

        # Check if velocity is not bigger than max allowed velocity
        if self.v.magnitude() > self.v_max:
            self.v = self.v.normalize() * self.v_max

        # Fix object's position with wall collision detection
        self.engine.wallsCollision(self)

        self.toSectorAdd()

    def fromSectorRemove(self):
        # Remove element from currently occupied sector
        if self in self.engine.collisionSectors[int(self.p.x / InternalProperties.COLLISION_SECTOR_SIZE)][
            int(self.p.y / InternalProperties.COLLISION_SECTOR_SIZE)]:
            self.engine.collisionSectors[int(self.p.x / InternalProperties.COLLISION_SECTOR_SIZE)][
                int(self.p.y / InternalProperties.COLLISION_SECTOR_SIZE)].remove(self)

    def toSectorAdd(self):
        # Add element to right sector
        self.engine.collisionSectors[int(self.p.x / InternalProperties.COLLISION_SECTOR_SIZE)][
            int(self.p.y / InternalProperties.COLLISION_SECTOR_SIZE)].append(self)

    def getCollisionCandidates(self):
        # Return list of objects located in nearby sectors

        # Get number of nearby sectors (depends on object size)
        sectorNum = int(self.size / InternalProperties.COLLISION_SECTOR_SIZE) + 1

        # Get list of candidates from nearby sectors
        candidates: List[CirclePhysical] = []
        for i in range(int(self.p.x / InternalProperties.COLLISION_SECTOR_SIZE) - sectorNum,
                int(self.p.x / InternalProperties.COLLISION_SECTOR_SIZE) + sectorNum + 1):
            for j in range(int(self.p.y / InternalProperties.COLLISION_SECTOR_SIZE) - sectorNum,
                    int(self.p.y / InternalProperties.COLLISION_SECTOR_SIZE) + sectorNum + 1):
                if 0 <= i < len(self.engine.collisionSectors) and 0 <= j < len(self.engine.collisionSectors[0]):
                    candidates += self.engine.collisionSectors[i][j]

        return candidates

