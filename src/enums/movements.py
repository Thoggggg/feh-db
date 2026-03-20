from enum import Enum


class MOVEMENTS_TYPE(str, Enum):
    INFANTRY = "Infantry"
    CAVALRY = "Cavalry"
    ARMORED = "Armored"
    FLYING = "Flying"

    @staticmethod
    def get_from_str(string: str):
        """ Change a string into the enum

        Args:
            string (str): A string representing a color

        Returns:
            WeaponColor: the weapon color in enum
        """
        string = string.upper()

        for enum_type in MOVEMENTS_TYPE:
            if enum_type.name == string:
                return enum_type
