"""Representation of a hero as a class
"""

from enum import Enum

from scraper.generic_class import GenericDataConverterToDb


class Move_type(Enum):
    INFANTRY = 1
    CAVALRIES = 2
    TANK = 3
    FLYING = 4


class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    GRAY = 4


class Weapon(Enum):
    DEFAULT = 1
    BOW = 2
    DAGGER = 3
    BOOK = 4
    MONSTER = 5
    ANIMALS = 6


class Hero(GenericDataConverterToDb):
    def __init__(self, picture, name, title, game, entry,
                 move, weapon, rarity, attributes, release):
        self.picture = picture
        self.name, self.title = name, title
        self.game: str = game
        self.entry = entry
        self.move = move
        self.weapon = weapon
        self.rarity = rarity
        self.release = release
        self.attributes: list[str] = attributes

    def __str__(self):
        return f"{self.name}:{self.title}"

    def is_valid(self):
        return self.name != "" and self.title != ""
