import mysql.connector

# from db.init import DB_NAME
DB_NAME = "feh_db"


def get_heroes(cursor, filters: dict[str, str] = {}):
    keys = filters.keys()

    sql_variable_names = """ \
characters.ID, Name, Title, Date, weapon_type, \
weapons.color, movement_type, game_name as gamename, \
resplendent, refresher, harmonized, emblem, attuned, ghb, \
regular_5, regular_4_3_2_1, ascended, specialRate, duo, aided, \
rearmed, mythic, entwined, legendary, special, story, tempest, \
Ranged, Magical, Melee, Magic, Dragon, Multicolor, Missile, \
Close, Physical \
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
            if name == "FALSE":
                continue
            elif name in ["TRUE", "True", "1"]:
                query += f" AND {filter} = TRUE"
            else:
                query += f" AND {filter} LIKE \"%{name}%\""

    try:
        print(query)
        cursor.execute(query, "")
        return cursor.fetchall()
    except mysql.connector.errors.ProgrammingError as err:
        print(f"[ERROR] This query wasn't succesful : {' '.join(query.split())}")
        print(err)
        return []


def get_my_heroes(cursor):
    pass
    # try:
    #     query = "FR"
    #     print(query)
    #     cursor.execute(query, "")
    #     return cursor.fetchall()
    # except mysql.connector.errors.ProgrammingError as err:
    #     print(f"[ERROR] This query wasn't succesful : {' '.join(query.split())}")
    #     print(err)
    #     return []


    

if __name__ == "__main__":
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YDoIN33dApwd ?",
        database=f"{DB_NAME}"
    )

    cursor = db.cursor()

    heroes = get_heroes(cursor, {"name": "Lyn", "movement_type": "Infantry"})
    print(heroes)
