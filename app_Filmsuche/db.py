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

# Konfiguration zum Verbinden von READ mit der Datenbank
db_config_read = {
    'host': os.environ.get('host_read'),
    'user': os.environ.get('user_read'),
    'password': os.environ.get('password_read'),
    'database': "sakila"
}

# Konfiguration für die Verbindung von WRITE mit der Datenbank
db_config_write = {
    'host': os.environ.get('host_write'),
    'user': os.environ.get('user_write'),
    'password': os.environ.get('password_write'),
    'database': "group_111124_fp_Yevgeniy_Guta"
}
# Verbindung zur Datenbank zum Lesen mit Fehlerbehandlung bei Verbindungsabbruch
try:
    conn_read = mysql.connector.connect(**db_config_read)
    cursor_read = conn_read.cursor()
except mysql.connector.Error as err:
    logging.exception(Fore.RED + Style.BRIGHT + f"Connection error READ:: {err}")
    sys.exit(1) # Beenden des Programms mit einem Fehlercode
else:
    print(Fore.LIGHTBLACK_EX + "Connection READ successful!")

def connect_to_db_write():
    try:
        conn_write = mysql.connector.connect(**db_config_write)
        return conn_write
    except mysql.connector.Error as err:
        logging.exception(Fore.RED + Style.BRIGHT + f"Error connecting to recording: {err}")
        return None

# Initialisieren der Datenbank und Erstellen einer Tabelle
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
            print(Fore.LIGHTBLACK_EX + "Datenbank und Tabelle erfolgreich initialisiert!")
        except mysql.connector.Error as err:
            logging.exception(Fore.RED + Style.BRIGHT + f"Fehler beim Initialisieren der Datenbank: {err}")
        finally:
            conn.close()


# Speichern oder Aktualisieren einer Abfrage
def save_search_query(query):
    conn = connect_to_db_write()
    if conn:
        try:
            cursor = conn.cursor()
            # Prüfung: Wenn ein Leerzeichen oder eine leere Zeichenfolge eingegeben wird, schreiben Sie den Wert NULL
            if isinstance(query, str) and query.strip() == "":
                query = None

            # Überprüfen, ob eine Anfrage vorhanden ist
            cursor.execute("SELECT * FROM search_queries WHERE query = %s", (query,))
            result = cursor.fetchone()

            if result:
                # Erhöhen Sie den Nutzungszähler, wenn der Eintrag vorhanden ist
                search_count = result[2] if len(result) > 2 else 0  # Schutz vor falscher Datenmenge
                cursor.execute("UPDATE search_queries SET search_count = search_count + 1 WHERE query = %s", (query,))
            else:
                # Hinzufügen einer neuen Anfrage, wenn der Datensatz nicht vorhanden ist
                cursor.execute("INSERT INTO search_queries (query) VALUES (%s)", (query,))

            conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            logging.exception(Fore.RED + Style.BRIGHT + f"Fehler beim Speichern der Anfrage: {err}")
        finally:
            conn.close()

# Ausgabefunktion für beliebte Abfragen
def print_search_count():
    try:
        conn = connect_to_db_write()
        cursor = conn.cursor()

        # Abrufen des Inhalts der Spalte „search_count“
        cursor.execute('''SELECT query, search_count
                          FROM search_queries
                          ORDER BY search_count DESC LIMIT 5''')
        results = cursor.fetchall()

        # Ausgeben der Werte der Spalte search_count
        print(Fore.LIGHTBLUE_EX + "\n === Beliebte Suchanfragen: === " + Style.RESET_ALL)
        for row in results:
            print(f"' {row[0]} --- gesamt: {row[1]} mal")
        cursor.close()
        conn.close()

        while True:
            user_choice = input(
                Fore.LIGHTYELLOW_EX + "Möchten Sie mit neuen Filtern weitersuchen?"
                + Fore.LIGHTYELLOW_EX + "\n'-' Zurück zum Hauptmenü \n '=' Ausstieg aus dem Programm:").strip().lower()
            if user_choice == '-':
                return   # Anzeige im Hauptmenü
            elif user_choice == '=':
                print(Fore.LIGHTGREEN_EX +"Das Programm wird beendet. Auf Wiedersehen!  ;) ")
                exit()  # Sicherheitsfunktionen
            else:
                print("Falsche Eingabe. Bitte versuchen Sie es erneut.")

    except mysql.connector.Error as err:
        print(f"Fehler beim Ausführen der Anfrage: {err}")

init_db()  # Initialisieren der Datenbank


# Die Funktion gibt eine Liste von Genres zur Auswahl zurück
def get_genres():
    query = "SELECT category_id, name FROM category;"
    cursor_read.execute(query)
    genres = cursor_read.fetchall()
    print("\n=== Verfügbare Genres: ===")
    for num, genre in enumerate(genres, start=1):
        print(f"{num}. {genre[1]}")
    return genres