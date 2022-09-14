import logging
from typing import Tuple

from abstracts import Rotatable, Movable, Command as AbstractCommand
from exceptions import MoveParamsReadError, MoveParamsSetError, CommandException
from utils import Vector


logger = logging.getLogger(__name__)


class MoveCommand(AbstractCommand):
    """Команда движения объекта по прямой."""

    def __init__(self, m: Movable) -> None:
        self.m = m

    def _read_params(self) -> Tuple[Vector, Vector]:
        try:
            position = self.m.get_position()
            velocity = self.m.get_velocity()
        except Exception as e:
            raise MoveParamsReadError(f"Can't read params for moving object[{self.m}]") from e

        return position, velocity

    def execute(self) -> None:
        position, velocity = self._read_params()
        new_position = position + velocity

        try:
            self.m.set_position(new_position)
        except Exception as e:
            raise MoveParamsSetError(f"Can't set params for moving object[{self.m}]") from e


class RotateCommand(AbstractCommand):
    """Команда поворота объекта."""

    def __init__(self, r: Rotatable) -> None:
        self.r = r

    def execute(self):
        new_direction = (
            (self.r.get_direction() + self.r.get_angular_velocity())
            % self.r.get_directions_number()
        )
        self.r.set_direction(new_direction)


class CheckFuelCommand(AbstractCommand):
    """Команда для проверки наличия топлива."""

    def __init__(self, o):
        self.o = o

    def execute(self):
        if self.o.fuel <= 0:
            raise CommandException('run out of fuel')


class BurnFuelCommand(AbstractCommand):
    """Команда сжигания топлива при движении."""

    def __init__(self, o, burn_rate: int = 1):
        self.o = o
        self.burn_rate = burn_rate

    def execute(self):
        self.o.set_fuel(self.o.fuel - self.burn_rate)


class Move(AbstractCommand):
    """Макрокоманда движения по прямой с расходом топлива."""

    def __init__(self, o):
        self.subcommands = [
            CheckFuelCommand(o),
            MoveCommand(o),
            BurnFuelCommand(o),
        ]
        self.o = o

    def execute(self):
        raise CommandException('Somethin went wrong')
        for command in self.subcommands:
            command.execute()

    def __str__(self):
        return f'{type(self).__name__}'


class LogCommand(AbstractCommand):
    def __init__(self, cmd: AbstractCommand, exc: Exception):
        self.cmd = cmd
        self.exc = exc

    def execute(self) -> None:
        msg = f'Error occurred while executing command [{self.cmd}]'
        logger.error(msg)
        logger.exception(self.exc)


class RepeaterCommand(AbstractCommand):
    def __init__(self, cmd):
        self.cmd = cmd

    def execute(self) -> None:
        logger.debug(f'Retrying command {self.cmd}')
        self.cmd.execute()

    def __str__(self):
        return f'Repeater[{self.cmd}]'


def exception_log_handler(cmd, exc, q) -> None:
    log_cmd = LogCommand(cmd, exc)
    q.append(log_cmd)


def exception_repeater_handler(cmd, q) -> None:
    repeater_cmd = RepeaterCommand(cmd)
    q.append(repeater_cmd)


def handle_exception(cmd, exc, q) -> None:
    if isinstance(cmd, RepeaterCommand):
        exception_log_handler(cmd, exc, q)
        return

    exception_repeater_handler(cmd, q)
