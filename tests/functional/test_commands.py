import pytest

from commands import CheckFuelCommand, BurnFuelCommand, Move
from exceptions import CommandException
from utils import Vector


def test_check_fuel(spaceship, monkeypatch):
    monkeypatch.setattr(spaceship, 'fuel', 0)

    command = CheckFuelCommand(spaceship)
    with pytest.raises(CommandException):
        command.execute()


def test_burn_fuel(spaceship):
    expected = spaceship.fuel - 1

    command = BurnFuelCommand(spaceship)
    command.execute()

    assert expected == spaceship.fuel


def test_move_correct(spaceship):
    Move(spaceship).execute()
    position_after = spaceship.position

    assert position_after == Vector([5, 8])


def test_move_error(spaceship, monkeypatch):
    monkeypatch.setattr(spaceship, 'fuel', 0)
    with pytest.raises(CommandException):
        Move(spaceship).execute()
