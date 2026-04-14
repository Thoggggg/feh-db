"""Representation of a hero as a class
"""

from src.scraper.generic_class import GenericDataConverterToDb


class Hero(GenericDataConverterToDb):
    """ Representation of a hero """
    def __init__(self, name: str, title: str, game: str, move: str, weapon: str, attributes: list, release: str):
        self.name, self.title = name.strip(), title.strip()
        self.game: str = game
        self.move = move
        self.weapon = weapon
        self.release = release
        self.attributes: list[str] = []

        if len(game) == 1:
            self.game.append("")

        self.title = self.title.replace("\"", "\\\"")

        for attr in attributes:
            self.attributes.append(attr.lower())

    def __str__(self):
        return f"{self.name}:{self.title}"

    def is_valid(self):
        """ Check if a hero has valid data """
        return self.name != "" and self.title != ""
