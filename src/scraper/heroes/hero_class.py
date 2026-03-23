"""Representation of a hero as a class
"""

from src.scraper.generic_class import GenericDataConverterToDb


class Hero(GenericDataConverterToDb):
    """ Representation of a hero """
    def __init__(self, name, title, game, entry,
                 move, weapon, attributes, release):
        self.name, self.title = name, title
        self.game: str = game
        self.entry = entry
        self.move = move
        self.weapon = weapon
        self.release = release
        self.attributes: list[str] = []

        for attr in attributes:
            self.attributes.append(attr.lower())

    def __str__(self):
        return f"{self.name}:{self.title}"

    def is_valid(self):
        """ Check if a hero has valid data """
        return self.name != "" and self.title != ""
