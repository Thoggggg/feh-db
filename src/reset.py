import mysql.connector
from mysql.connector import errorcode
from db.init import DB_NAME
from db.sql_strings import create_tables


def delete_all(db, cursor):
    # List of tables to be deleted
    TABLES_TO_DELETE = create_tables.keys()

    # --- Connection setup ---
    try:
        print(f"[INFO] Connected to database '{DB_NAME}'.")

        # 1. Disable foreign key checks to avoid errors about table dependencies.
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        print("[INFO] Disabled foreign key checks.")

        # 2. Loop through the tables and drop each one.
        for table_name in TABLES_TO_DELETE:
            try:
                print(f"[INFO] Dropping table `{table_name}`...", end='')
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                print("[INFO] SUCCESS")
            except mysql.connector.Error as err:
                print(f"[INFO] FAILED: {err}")

        # 3. Re-enable foreign key checks. This is a very important step!
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("[INFO] Re-enabled foreign key checks.")

        # Commit the changes to the database
        db.commit()
        print("[INFO] All specified tables have been deleted successfully.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[ERROR] Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"[ERROR] Database '{DB_NAME}' does not exist")
        else:
            print(err)
