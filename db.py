import sys
import mysql.connector
import os
from dotenv import load_dotenv
import dotenv
from pathlib import Path
import logging
from rich import print
from colorama import Fore, Back, Style, init

dotenv.load_dotenv(Path('.env'))

# Configuration for connecting READ to the database
db_config_read = {
    'host': os.environ.get('host_read'),
    'user': os.environ.get('user_read'),
    'password': os.environ.get('password_read'),
    'database': "sakila"
}

# Configuration for connecting WRITE to the database
db_config_write = {
    'host': os.environ.get('host_write'),
    'user': os.environ.get('user_write'),
    'password': os.environ.get('password_write'),
    'database': "group_111124_fp_Yevgeniy_Guta"
}

try:
    conn_read = mysql.connector.connect(**db_config_read)
    cursor_read = conn_read.cursor()
except mysql.connector.Error as err:
    logging.exception(f"Connection error READ:: {err}")
    sys.exit(1) # Terminating the program with an error code
else:
    print("Connection READ successful!")

def connect_to_db_write():
    try:
        conn_write = mysql.connector.connect(**db_config_write)
        return conn_write
    except mysql.connector.Error as err:
        logging.exception(f"Error connecting to recording: {err}")
        return None

# Initializing the database and creating a table
def init_db():
    conn = connect_to_db_write()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS search_queries
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               query
                               TEXT
                               NOT
                               NULL,
                               search_count
                               INT
                               DEFAULT
                               1
                           )
                           """)
            conn.commit()
            print("Database and table initialized successfully!")
        except mysql.connector.Error as err:
            logging.exception(f"Error initializing database: {err}")
        finally:
            conn.close()


# Saving or updating a query
def save_search_query(query):
    conn = connect_to_db_write()
    if conn:
        try:
            cursor = conn.cursor()
            # Check: if a space or empty string is entered, write the value NULL
            if isinstance(query, str) and query.strip() == "":
                query = None

            # Checking for the existence of a request
            cursor.execute("SELECT * FROM search_queries WHERE query = %s", (query,))
            result = cursor.fetchone()

            if result:
                # Increment the usage counter if the entry exists
                search_count = result[2] if len(result) > 2 else 0  # Protection against incorrect amount of data
                cursor.execute("UPDATE search_queries SET search_count = search_count + 1 WHERE query = %s", (query,))
            else:
                # Adding a new request if the record does not exist
                cursor.execute("INSERT INTO search_queries (query) VALUES (%s)", (query,))

            conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            logging.exception(f"Error saving request: {err}")
        finally:
            conn.close()

def print_search_count():
    try:
        conn = connect_to_db_write()
        cursor = conn.cursor()

        # Getting the contents of the search_count column
        cursor.execute('''SELECT query, search_count
                          FROM search_queries
                          ORDER BY search_count DESC LIMIT 5''')
        results = cursor.fetchall()

        # Outputting the search_count column values
        print("\nPopular queries:")
        for row in results:
            print(f"'{row[0]}' total: {row[1]} ")
        cursor.close()
        conn.close()

        while True:
            user_choice = input(
                "Would you like to continue your search with a new query? "
                "\n'-' exit to main menu \n '=' exit the program:").strip().lower()
            if user_choice == '-':
                return #  Return to main menu
            elif user_choice == '=':
                print("Exiting the program. Goodbye!")
                exit()
            else:
                print("Incorrect input. Try again.")

    except mysql.connector.Error as err:
        logging.exception(f"Error while executing popularity query: {err}")

init_db()  # Initializing the database

def get_genres():
    query = "SELECT category_id, name FROM category;"
    cursor_read.execute(query)
    genres = cursor_read.fetchall()
    print("\nAvailable genres:")
    for num, genre in enumerate(genres, start=1):
        print(f"{num}. {genre[1]}")
    return genres