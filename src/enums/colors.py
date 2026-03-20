from enum import Enum


class WeaponColor(str, Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    COLORLESS = "Colorless"

    @staticmethod
    def get_from_str(string: str):
        """ Change a string into the enum

        Args:
            string (str): A string representing a color

        Returns:
            WeaponColor: the weapon color in enum
        """
        string = string.upper()

        for enum_type in WeaponColor:
            if enum_type.name == string:
                return enum_type
