import enum

from .base import Model

from .country import Country
from .grape import Grape


class Wine(Model):
    class Color(enum.IntEnum):
        RED = enum.auto()
        WHITE = enum.auto()
        ROSE = enum.auto()

    class Sugar(enum.IntEnum):
        DRY = enum.auto()
        SEMI_DRY = enum.auto()
        SEMI_SWEET = enum.auto()
        SWEET = enum.auto()

    name: str
    color: Color
    sugar: Sugar
    grape: Grape
    country: Country
