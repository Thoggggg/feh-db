import mysql.connector
from mysql.connector import errorcode
from src.db.sql_strings import create_tables
import logging


def delete_all(db, cursor):
    # List of tables to be deleted
    TABLES_TO_DELETE = create_tables.keys()

    # --- Connection setup ---
    try:
        # 1. Disable foreign key checks to avoid errors about table dependencies.
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        logging.debug("Disabled foreign key checks.")

        # 2. Loop through the tables and drop each one.
        for table_name in TABLES_TO_DELETE:
            try:
                logging.info(f"Dropping table `{table_name}`...", end='')
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
            except mysql.connector.Error as err:
                logging.warning(f"Failed to drop table : {err}")

        # 3. Re-enable foreign key checks. This is a very important step!
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        logging.debug("Re-enabled foreign key checks.")

        # Commit the changes to the database
        db.commit()
        logging.info("All specified tables have been deleted successfully.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with the username or the password")
        else:
            logging.error(str(err))
