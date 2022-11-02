import math

from HaxballEngine.Physics.Post import Post
from HaxballEngine.Physics.Ball import Ball
from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.Properties import InternalProperties


class Collision:
    pass

    # # Check if circle collides with any other circle in the nearest sectors
    # @staticmethod
    # def collide(circ1):
    #     # Get objects from nearby sectors
    #     nearby = circ1.getCollisionCandidates()
    #
    #     for circ2 in nearby:
    #         if circ2 != circ1:
    #             dist = math.sqrt((circ1.p.x - circ2.p.x) ** 2 + (circ2.p.y - circ1.p.y) ** 2)
    #             if dist <= circ1.size + circ2.size:
    #
    #                 # Fix post speed
    #                 if isinstance(circ1, Post):
    #                     circ1.v.x = 0
    #                     circ1.v.y = 0
    #
    #                 # Move colliding circles away
    #                 overlap = (dist - circ1.size - circ2.size) / 2
    #
    #                 # Move circle1
    #                 circ1.from_sector_remove()
    #                 if dist != 0:
    #                     p_new = circ1.p - overlap * (circ2.weight / circ1.weight) * (circ1.p - circ2.p) / dist
    #                     circ1.set_p(p_new.x, p_new.y)
    #                 else:
    #                     p_new = circ1.p - overlap * (circ2.weight / circ1.weight) * circ1.p.normalize()
    #                     circ1.set_p(p_new.x, p_new.y)
    #                 # Collision.walls_collision(circ1, circ1.engine)
    #                 circ1.to_sector_add()
    #
    #                 # Move circle2
    #                 circ2.from_sector_remove()
    #                 if dist != 0:
    #                     p_new = circ2.p + overlap * (circ1.weight / circ2.weight) * (circ1.p - circ2.p) / dist
    #                     circ2.set_p(p_new.x, p_new.y)
    #                 else:
    #                     p_new = circ2.p + overlap * (circ1.weight / circ2.weight) * circ1.p.normalize()
    #                     circ2.set_p(p_new.x, p_new.y)
    #                 # Collision.walls_collision(circ2, circ2.engine)
    #                 circ2.to_sector_add()
    #
    #                 # Count velocities after collision
    #                 circ1.v, circ2.v = Collision.collision_calculator(circ1.v, circ2.v, circ1.weight, circ2.weight,
    #                                                                   circ1.p, circ2.p)
    #
    #                 # Player ball control
    #                 circ2.v = circ2.v * circ1.ball_control
    #
    #                 # Check if ball velocity is not bigger than max allowed velocity
    #                 if circ2.v.magnitude() > circ2.v_max:
    #                     circ2.v = circ2.v.normalize() * circ2.v_max
    #
    #                 if circ1.v.magnitude() > circ1.v_max:
    #                     circ1.v = circ1.v.normalize() * circ1.v_max
    #

