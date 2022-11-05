from typing import List, Tuple

import pygame

from HaxballEngine.Physics.CirclePhysical import CirclePhysical
from HaxballEngine.Physics.Post import Post


class SphereCollider:
    @staticmethod
    def sphereCollisionVelocities(
        v1: pygame.Vector2,
        v2: pygame.Vector2,
        m1: float,
        m2: float,
        x1: pygame.Vector2,
        x2: pygame.Vector2,
    ) -> Tuple[pygame.Vector2, pygame.Vector2]:

        # Calculate new velocities after collision
        mass: float = 2 * m1 / (m1 + m2)
        v1_new: pygame.Vector2 = v1 - (
            mass * (v1 - v2).dot(x1 - x2) / pow((x1 - x2).length(), 2)
        ) * (x1 - x2)
        v2_new: pygame.Vector2 = v2 - (
            mass * (v2 - v1).dot(x2 - x1) / pow((x2 - x1).length(), 2)
        ) * (x2 - x1)
        return v1_new, v2_new

    @staticmethod
    def collide(circle1: CirclePhysical) -> None:
        # Check collision with another sphere

        # Get candidate collision objects
        candidates: List[CirclePhysical] = circle1.getCollisionCandidates()

        # Check collision with each candidate
        for candidate in candidates:
            if candidate != circle1:
                # Check if distance between objects is less than sum of their sizes
                dist: float = (circle1.p - candidate.p).magnitude()

                if dist < circle1.size + candidate.size:
                    # If collision with Post, zero its velocity
                    if isinstance(circle1, Post):
                        circle1.v = pygame.math.Vector2(0, 0)
                    # If collision with Post, zero its velocity
                    if isinstance(candidate, Post):
                        candidate.v = pygame.math.Vector2(0, 0)

                    # Remove spheres from sectors
                    circle1.fromSectorRemove()
                    candidate.fromSectorRemove()

                    # Check if spheres are not in the same position
                    # If so, move them a little from each other along inverted velocity vector
                    if dist == 0:
                        circle1.p += -circle1.v.normalize() * 0.01
                        candidate.p += candidate.v.normalize() * 0.01

                    # If collision, calculate new velocities
                    circle1.v, candidate.v = SphereCollider.sphereCollisionVelocities(
                        circle1.v,
                        candidate.v,
                        circle1.weight,
                        candidate.weight,
                        circle1.p,
                        candidate.p,
                    )

                    # Fix positions
                    if not isinstance(circle1, Post):
                        circle1.p = candidate.p + (
                            circle1.p - candidate.p
                        ).normalize() * (circle1.size + candidate.size)

                    if not isinstance(candidate, Post):
                        candidate.p = circle1.p + (
                            candidate.p - circle1.p
                        ).normalize() * (circle1.size + candidate.size)

                    # Add spheres to sectors
                    circle1.toSectorAdd()
                    candidate.toSectorAdd()
