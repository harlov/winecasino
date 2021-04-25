import enum

from .base import Model


class Country(Model):
    class PartOfWorld(enum.IntEnum):
        OLD_WORLD = enum.auto()
        NEW_WORLD = enum.auto()
        EX_USSR = enum.auto()

    name: str
    part_of_world: PartOfWorld
