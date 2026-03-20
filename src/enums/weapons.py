from enum import Enum
from itertools import chain
from typing import Union


class WeaponType(str, Enum):
    BOW = "Bow"
    DAGGER = "Dagger"
    TOME = "Tome"
    BREATH = "Breath"
    BEAST = "Beast"

    @staticmethod
    def get_from_str(string: str):
        """ Change a string into the enum

        Args:
            string (str): A string representing a color

        Returns:
            WeaponColor: the weapon color in enum
        """
        string = string.upper()

        for enum_type in WeaponType:
            if enum_type.name == string:
                return enum_type


class SpecificWeaponType(str, Enum):
    SWORD = "Sword"
    AXE = "Axe"
    LANCE = "Lance"
    STAFF = "Staff"

    @staticmethod
    def get_from_str(string: str):
        """ Change a string into the enum

        Args:
            string (str): A string representing a color

        Returns:
            WeaponColor: the weapon color in enum
        """
        string = string.upper()

        for enum_type in WeaponType:
            if enum_type.name == string:
                return enum_type


Weapons = Union[WeaponType, SpecificWeaponType]
