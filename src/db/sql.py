from mysql.connector.errors import ProgrammingError as SqlProgrammingError
import mysql.connector
import logging
from pydantic_settings import BaseSettings
from pydantic import Field

from src.db.init import fill_movements, fill_weapons
from src.db.init import setup_db, setup_tables
from src.scraper.stats.stat_class import Stat

import os
from dotenv import load_dotenv

# Must be executed before launching the app
load_dotenv()


class Settings(BaseSettings):
    db_password: str = Field(validation_alias='my_auth_key')
    db_name: str = Field()


class SQL:
    def __init__(self):
        self.default_setup()

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ["db_password"],
            database=os.environ["db_name"]
        )

        self.cursor = self.db.cursor()

    def execute_insert(self, query, verbose=False):
        """ Execute an insert query

        Args:
            query (str): The sql query
            verbose (bool, optional): if we want to see the query in the
                stdout. Defaults to False.
        """
        if verbose:
            logging.debug(query)
        self.cursor.execute(query, "")
        self.db.commit()

    def execute_select(self, query):
        """ Execute a sql select query

        Args:
            query (str): The sql query

        Returns:
            _type_: What the select was selecting
        """
        self.cursor.execute(query, "")
        return self.cursor.fetchall()

    def default_setup(self):
        """ Create the database if needed """

        # Connect to the db
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ["DB_PASSWORD"])

        mycursor = mydb.cursor()

        # Create a database
        db_name = os.environ["db_name"]
        setup_db(mycursor, os.environdb_name)

        # Get the list of all the existing tables
        mycursor.execute(f"USE {db_name}")
        mycursor.execute("SHOW TABLES")

        table_list = mycursor.fetchall()
        table_list = [table[0] for table in table_list]

        # Init if there is no tables
        if len(table_list) == 0:
            setup_tables(mycursor, db_name)
            fill_movements(mydb, mycursor)
            fill_weapons(mydb, mycursor)
            logging.info("Tables have been initialized")
        elif len(table_list) < 7:  # Arbitrary value below the actual number
            logging.warning("The tables has not been erased efficiently")
        else:
            logging.info(f"{len(table_list)} tables were already initialized")

    def is_character_existing(self, hero):
        try:
            query = f"""
                SELECT * FROM characters
                WHERE name="{hero.name}"
                AND title="{hero.title}"
            """
            hero_list = self.execute_select(query)

        except SqlProgrammingError:
            logging.error(f"There is likely no Characters table. QQuery was : {query}")
            exit(1)

        return len(hero_list) != 0

    def add_game(self, game_name: str):
        """Add a game if it doesn't already exists

        Args:
            game_name (str): The name of a FE Game
        """
        # Get all the existing games
        # TODO : Create a list instead of reading each time ?
        self.cursor.execute("SELECT * from Games")
        all_games = self.cursor.fetchall()
        all_games = [game[1] for game in all_games]

        # Add the game to the db if not existing
        if game_name not in all_games:
            logging.info(f"{game_name} was not found in the database")
            query = f"INSERT INTO games (game_name, static_img_path)\
                    VALUES (\"{game_name}\", \"\")"
            self.execute_insert(query)

    def add_characters(self, hero) -> int:
        # add the game to the db if not existing
        self.add_game(hero.game)

        # Get weapon data
        weapon = hero.weapon.split(" ")
        if len(weapon) == 2:
            weapon_color = weapon[0]
            weapon_type = weapon[1]
        else:
            weapon_color = ""
            weapon_type = ""

        # Create the query with all the data
        query = f"""
            INSERT INTO characters (Name, Title, Game_ID, Movement_ID, \
                Weapon_ID, Date, Static_img_path) VALUES ( \
            \"{hero.name}\",
            \"{hero.title}\",
            (SELECT ID FROM games WHERE game_name = \"{hero.game}\"),
            (SELECT ID FROM movements WHERE movement_type = \"{hero.move}\"),
            (SELECT ID FROM weapons WHERE weapon_type = \"{weapon_type}\" \
                                        and color = \"{weapon_color}\"),
            \"{hero.release}\",
            \"{hero.picture}\"
        );"""

        self.execute_insert(query, True)

        # Add the abilities in the other table
        query = f""" INSERT INTO attributes ({', '.join(hero.attributes)})\
            VALUES ({', '.join(["1"] * len(hero.attributes))});
        """

        self.execute_insert(query, False)

        return self.cursor.lastrowid

    def add_stats(self, latest_id: int, lvl1: Stat, lvl40: Stat, growth_rate: Stat):
        query = f"""
INSERT INTO characterstats ( character_id, \
    hp_lvl1, atk_lvl1, spd_lvl1, def_lvl1, res_lvl1, \
    hp_growth, atk_growth, spd_growth, def_growth, res_growth, \
    hp_lvl40, atk_lvl40, spd_lvl40, def_lvl40, res_lvl40 \
) VALUES ( {latest_id}, \
    {lvl1.hp}, {lvl1.atk}, {lvl1.spd}, {lvl1.dfs}, {lvl1.res}, \
    {growth_rate.hp}, {growth_rate.atk}, {growth_rate.spd}, {growth_rate.dfs}, {growth_rate.res}, \
    {lvl40.hp}, {lvl40.atk}, {lvl40.spd}, {lvl40.dfs}, {lvl40.res}
);"""

        self.execute_insert(query, True)


if __name__ == "__main__":
    sql = SQL()
