import logging

from abstracts import Rotatable, Movable
from commands import Move, handle_exception
from utils import Vector
from collections import deque


class SpaceShip(Movable, Rotatable):
    """Класс космического корабля."""

    def __init__(self, pos: Vector, vel: Vector, ang_vel: int, dir: int, dir_num: int, fuel: int):
        self.position = pos
        self.velocity = vel
        self.direction = dir
        self.directions_number = dir_num
        self.angular_velocity = ang_vel
        self.fuel = fuel

    def get_direction(self) -> int:
        return self.direction

    def get_directions_number(self) -> int:
        return self.directions_number

    def get_position(self) -> Vector:
        return self.position

    def get_velocity(self) -> Vector:
        return self.velocity

    def get_angular_velocity(self) -> int:
        return self.angular_velocity

    def set_direction(self, new_dir: int) -> None:
        self.direction = new_dir

    def set_position(self, new_pos: Vector) -> None:
        self.position = new_pos

    def set_fuel(self, val: int) -> None:
        self.fuel = val


if __name__ == '__main__':
    logging.basicConfig(
        format='%(filename)s: %(message)s',
        level=logging.DEBUG
    )
    space_ship = SpaceShip(pos=Vector([12, 5]), vel=Vector([-7, 3]), ang_vel=3, dir=3, dir_num=8, fuel=0)
    move = Move(o=space_ship)

    cmd_queue = deque()
    cmd_queue.append(move)

    while cmd_queue:
        command = cmd_queue.popleft()
        try:
            command.execute()
        except Exception as e:
            handle_exception(cmd=command, exc=e, q=cmd_queue)
