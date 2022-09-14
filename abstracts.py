from abc import ABC, abstractmethod

from utils import Vector


class Command(ABC):
    """Абстракция класса команды."""

    def execute(self) -> None:
        raise NotImplementedError


class Rotatable(ABC):
    """Абстракция вращающегося объекта"""

    @abstractmethod
    def get_direction(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_directions_number(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_angular_velocity(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_direction(self, new_dir: int) -> None:
        raise NotImplementedError


class Movable(ABC):
    """Абстракция движущегося объекта"""

    @abstractmethod
    def get_position(self) -> Vector:
        raise NotImplementedError

    @abstractmethod
    def get_velocity(self) -> Vector:
        raise NotImplementedError

    @abstractmethod
    def set_position(self, new_pos: Vector) -> None:
        raise NotImplementedError
