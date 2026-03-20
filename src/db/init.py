from itertools import product

import mysql.connector
from mysql.connector.abstracts import MySQLCursorAbstract as SqlCursor
from src.db.sql_strings import create_tables
from src.enums.colors import WeaponColor
from src.enums.movements import MOVEMENTS_TYPE
from src.enums.weapons import SpecificWeaponType, WeaponType

DB_NAME = "feh_db"


def setup_db(cursor: SqlCursor):
    """Setup the database object

    Args:
        cursor (MySQLCursorAbstract): cursor not connected to the db
    """
    cursor.execute("SHOW DATABASES")
    db_list = cursor.fetchall()

    # Fetch all give a list of tuples of size 1
    db_list = [db[0] for db in db_list]

    if DB_NAME not in db_list:
        print(f"[INFO] db not found, creating {DB_NAME}")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")


def setup_tables(cursor: SqlCursor):
    """Create the tables for the project
    NOTE : doesn't fill the tables

    Args:
        cursor (SqlCursor):
    """
    cursor.execute(f"USE {DB_NAME}")
    cursor.execute("SHOW TABLES")

    table_list = cursor.fetchall()
    table_list = [table[0] for table in table_list]

    for table, create_str in create_tables.items():
        if table.lower() not in table_list:
            print(f"[INFO] table not found, creating {table}")
            try:
                cursor.execute(f"CREATE TABLE {create_str}")
            except mysql.connector.Error as err:
                print("Something went wrong:")
                print(f"Error Code: {err.errno}")
                print(f"Message: {err.msg}")


def fill_movements(db, cursor: SqlCursor):
    """ Fill the movements table with all the data

    Args:
        db () : Connector to the db
        cursor (SqlCursor): cursor of the db
    """
    sql = """INSERT INTO movements (id, movement_type, static_image_path)\
             VALUES (%s, %s, %s)"""
    val = [(i, mov, "") for i, mov in enumerate(MOVEMENTS_TYPE)]

    cursor.executemany(sql, val)

    db.commit()


def fill_weapons(db, cursor: SqlCursor):
    """ Fill the weapons table with all the data

    Args:
        db () : Connector to the db
        cursor (SqlCursor): cursor of the db
    """

    sql = """INSERT INTO weapons (id, weapon_type, color, static_img)\
             VALUES (%s, %s, %s, %s)"""

    # colors = ["Red", "Blue", "Green", "Colorless"]
    # weapon = ["Bow", "Dagger", "Tome", "Breath", "Beast"]

    val = [(i, weapon[0], weapon[1], "") for i, weapon in enumerate(zip(SpecificWeaponType, WeaponColor))]
    val += [(i + 4, weapon[0], weapon[1], "") for i, weapon in enumerate(product(WeaponType, WeaponColor))]

    # val = [(0, "Sword", "Red", ""),
    #        (1, "Axe",   "Green", ""),
    #        (2, "Lance", "Blue", ""),
    #        (3, "Staff", "Colorless", "")]

    # cpt = 4
    # for w in weapon:
    #     for c in colors:
    #         val.append((cpt, w, c, ""))
    #         cpt += 1

    cursor.executemany(sql, val)

    db.commit()
