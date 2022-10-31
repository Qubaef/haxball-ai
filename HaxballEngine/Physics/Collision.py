import math

from HaxballEngine.Physics.Post import Post
from HaxballEngine.Physics.Ball import Ball
from HaxballEngine.Physics.Agent import Agent
from HaxballEngine.Properties import InternalProperties


class Collision:

    # Check if circle collides with any other circle in the nearest sectors
    @staticmethod
    def collide(circ1):
        # Get objects from nearby sectors
        nearby = circ1.get_nearby()

        for circ2 in nearby:
            if circ2 != circ1:
                dist = math.sqrt((circ1.p.x - circ2.p.x) ** 2 + (circ2.p.y - circ1.p.y) ** 2)
                if dist <= circ1.size + circ2.size:

                    # Fix post speed
                    if isinstance(circ1, Post):
                        circ1.v.x = 0
                        circ1.v.y = 0

                    # Move colliding circles away
                    overlap = (dist - circ1.size - circ2.size) / 2

                    # Move circle1
                    circ1.from_sector_remove()
                    if dist != 0:
                        p_new = circ1.p - overlap * (circ2.weight / circ1.weight) * (circ1.p - circ2.p) / dist
                        circ1.set_p(p_new.x, p_new.y)
                    else:
                        p_new = circ1.p - overlap * (circ2.weight / circ1.weight) * circ1.p.normalize()
                        circ1.set_p(p_new.x, p_new.y)
                    Collision.walls_collision(circ1, circ1.engine)
                    circ1.to_sector_add()

                    # Move circle2
                    circ2.from_sector_remove()
                    if dist != 0:
                        p_new = circ2.p + overlap * (circ1.weight / circ2.weight) * (circ1.p - circ2.p) / dist
                        circ2.set_p(p_new.x, p_new.y)
                    else:
                        p_new = circ2.p + overlap * (circ1.weight / circ2.weight) * circ1.p.normalize()
                        circ2.set_p(p_new.x, p_new.y)
                    Collision.walls_collision(circ2, circ2.engine)
                    circ2.to_sector_add()

                    # Count velocities after collision
                    circ1.v, circ2.v = Collision.collision_calculator(circ1.v, circ2.v, circ1.weight, circ2.weight,
                                                                      circ1.p, circ2.p)

                    # Player ball control
                    circ2.v = circ2.v * circ1.ball_control

                    # Check if ball velocity is not bigger than max allowed velocity
                    if circ2.v.magnitude() > circ2.v_max:
                        circ2.v = circ2.v.normalize() * circ2.v_max

                    if circ1.v.magnitude() > circ1.v_max:
                        circ1.v = circ1.v.normalize() * circ1.v_max

    @staticmethod
    def collision_calculator(v1, v2, m1, m2, x1, x2) -> tuple[float, float]:
        mass = 2 * m1 / (m1 + m2)
        v11 = v1 - (mass * (v1 - v2).dot(x1 - x2) / pow((x1 - x2).length(), 2)) * (x1 - x2)
        v22 = v2 - (mass * (v2 - v1).dot(x2 - x1) / pow((x2 - x1).length(), 2)) * (x2 - x1)
        return v11, v22

    @staticmethod
    def walls_collision(obj, game):
        # check collision with pitch walls

        # Top wall
        if obj.p.y < int(obj.size + (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2):
            obj.set_p(obj.p.x, int(obj.size + (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2))
            obj.v.y *= -InternalProperties.WALL_BOUNCE_FACTOR

        # Bottom wall
        if obj.p.y > int(InternalProperties.PITCH_HEIGHT + ((InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2) - obj.size):
            obj.set_p(obj.p.x, int(InternalProperties.PITCH_HEIGHT + ((InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2) - obj.size))
            obj.v.y *= -InternalProperties.WALL_BOUNCE_FACTOR

        if isinstance(obj, Agent):
            # Left wall
            if obj.p.x < int(obj.size + (InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2):
                if game.pitch.goalLeft.post_down.p.y > obj.p.y > game.pitch.goalLeft.post_up.p.y:
                    if obj.p.x < game.pitch.goalLeft.x:
                        obj.set_p(game.pitch.goalLeft.x, obj.p.y)
                        obj.v *= 0
                else:
                    obj.set_p(int(obj.size + (InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2), obj.p.y)
                    obj.v.x *= -InternalProperties.WALL_BOUNCE_FACTOR

            # Right wall
            if obj.p.x > int(InternalProperties.PITCH_WIDTH + ((InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2) - obj.size):
                if game.pitch.goalRight.post_down.p.y > obj.p.y > game.pitch.goalRight.post_up.p.y:
                    if obj.p.x > game.pitch.goalRight.x:
                        obj.set_p(game.pitch.goalRight.x, obj.p.y)
                        obj.v *= 0
                else:
                    obj.set_p(int(InternalProperties.PITCH_WIDTH + ((InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2) - obj.size), obj.p.y)
                    obj.v.x *= -InternalProperties.WALL_BOUNCE_FACTOR

        elif isinstance(obj, Ball):
            # Left wall
            if obj.p.x < int(obj.size + (InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2):
                if game.pitch.goalLeft.post_down.p.y > obj.p.y > game.pitch.goalLeft.post_up.p.y:
                    if obj.p.x < game.pitch.goalLeft.x - obj.size:
                        game.goalScored(game.pitch.goalLeft)
                else:
                    obj.set_p(int(obj.size + (InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2), obj.p.y)
                    obj.v.x *= -InternalProperties.WALL_BOUNCE_FACTOR

            # Right wall
            if obj.p.x > int(InternalProperties.PITCH_WIDTH + ((InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2) - obj.size):
                if game.pitch.goalRight.post_down.p.y > obj.p.y > game.pitch.goalRight.post_up.p.y:
                    if obj.p.x > game.pitch.goalRight.x + obj.size:
                        game.goalScored(game.pitch.goalRight)
                else:
                    obj.set_p(int(InternalProperties.PITCH_WIDTH + ((InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2) - obj.size), obj.p.y)
                    obj.v.x *= -InternalProperties.WALL_BOUNCE_FACTOR
