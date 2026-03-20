from enum import Enum


class STATS_TYPE(str, Enum):
    HEALTH_POINT = "hp"
    ATTACK = "atk"
    SPEED = "spd"
    DEFENSE = "dfs"
    RESISTANCE = "res"

    @staticmethod
    def get_from_str(string: str):
        """ Change a string into the enum

        Args:
            string (str): A string representing a color

        Returns:
            WeaponColor: the weapon color in enum
        """
        string = string.upper()

        for enum_type in STATS_TYPE:
            if enum_type.name == string:
                return enum_type
