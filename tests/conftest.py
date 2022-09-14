import pytest
from main import SpaceShip
from utils import Vector


@pytest.fixture(scope='module')
def spaceship():
    return SpaceShip(pos=Vector([12, 5]), vel=Vector([-7, 3]), ang_vel=3, dir=3, dir_num=8, fuel=10)
