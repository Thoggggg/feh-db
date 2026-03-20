import mysql.connector
import logging

# from db.init import DB_NAME
DB_NAME = "feh_db"


def get_heroes(cursor, filters: dict[str, str] = {}):
    """ fetch heroes from the db """

    keys = filters.keys()

    sql_variable_names = """ \
characters.ID, Name, Title, Date, weapon_type, \
weapons.color, movement_type, game_name as gamename, \
resplendent, refresher, harmonized, emblem, attuned, ghb, \
regular_5, regular_4_3_2_1, ascended, specialRate, duo, aided, \
rearmed, mythic, entwined, legendary, special, story, tempest, \
ranged, magical, melee, magic, dragon, multicolor, missile, \
close, physical \
"""

    query = f"SELECT {sql_variable_names} FROM characters \
            INNER JOIN movements ON movements.ID=Movement_ID \
            INNER JOIN weapons ON weapons.ID=Weapon_ID \
            INNER JOIN games ON games.id=Game_ID \
            INNER JOIN attributes ON characters.id=Character_ID "

    if filters["end_date"] is None:
        query += f"WHERE Date BETWEEN '{filters["start_date"]}' AND NOW()"
    else:
        query += f"WHERE Date BETWEEN '{filters["start_date"]}' AND {filters["end_date"]}"

    # Dates have already been added to the query
    filters.pop("start_date")
    filters.pop("end_date")

    if len(keys) != 0:
        for filter, name in filters.items():
            if name is None:
                continue
            elif isinstance(name, bool):
                query += f" AND {filter} = {name}"
            else:
                query += f" AND {filter} LIKE \"%{name}%\""

    try:
        logging.debug(query)
        cursor.execute(query, "")
        return cursor.fetchall()
    except mysql.connector.errors.ProgrammingError as err:
        logging.error(f"This query wasn't succesful : {' '.join(query.split())}. {err}")
        return -1
