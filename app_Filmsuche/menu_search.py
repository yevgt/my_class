from search import search_movies
from utils import print_results
from db import save_search_query, cursor_read
from valid_years import validate_year_input, validate_year_range
from db import get_genres
import logging
from colorama import Fore, Back, Style, init


# Suchfunktion nach Wort (Wortteil)
def search_by_keyword():
    while True:
        keyword = input(Fore.LIGHTYELLOW_EX + "Geben Sie einen Teil des Namens ein (oder '=' zum Beenden): ")
        if keyword.strip() == "=":
            return  # Zurück zum Hauptmenü
        save_search_query(f"Wort (Teil eines Wortes):'{keyword}'")
          # Speichern oder aktualisieren Sie die Abfrage in der Datenbank

        offset = 0  # Anfänglicher Verschiebungswert
        while True:
            # Suche nach Filmen
            movies, total_count = search_movies(keyword=keyword, limit=10, offset=offset)
            print_results(movies, total_count, f"Filme, die mit dem Schlüsselwort übereinstimmen: '{keyword}'", offset)

            # Wenn keine weiteren Filme mehr angezeigt werden können, beenden Sie
            if not movies:
                print("Es sind keine Filme zum Anzeigen vorhanden.")
                break

            # Aufforderung zum weiteren Vorgehen
            next_action = input(Fore.LIGHTYELLOW_EX + "Enter '-' für die nächsten 10 Filme, \n'=' um die Suche zu beenden \n'Space' für die neue Suche: ").strip().lower()
            if next_action == '=':
                return  # Zurück zum Hauptmenü
            elif next_action == '-':
                offset += 10  # Erhöhen Sie den Offset um 10
            else:
                break

# Funktion zur Bearbeitung einer Anfrage nach "Genre"
def search_by_genre():
    genres = get_genres()

    while True:
        # Genre-Auswahlblock (kann übersprungen werden)
        genre = None
        while True:
            genre_choice = input(Fore.LIGHTYELLOW_EX + "Wählen Sie die Genrenummer aus, \n'Eingabe' (um das Genre zu überspringen) \n '=' (zurück zum Hauptmenü): ").strip()
            if genre_choice == "=":
                return  # zurück zum Hauptmenü
            elif genre_choice == "":
                genre = None
                break
            try:
                genre_choice_int = int(genre_choice)
                if 1 <= genre_choice_int <= len(genres):
                    genre = genres[genre_choice_int - 1][1]
                    save_search_query(f"genre: {genre}")  # Ausgewähltes Genre speichern
                    break
                else:
                    print(Fore.RED + "Ungültige Nummer. Versuchen Sie es erneut.")
            except ValueError:
                logging.exception(Fore.LIGHTYELLOW_EX + "Bitte geben Sie eine Zahl ein oder drücken Sie „Eingabe“, um zu überspringen.")

        # Auswahlblock Jahr/Jahresbereich
        year_filter = None  # None - nicht nach Jahr filtern
        while True:
            year_input = input(Fore.LIGHTYELLOW_EX + "\nGeben Sie das Jahr (JJJJ) oder den Bereich mit 'Leertaste' (von 1990 bis 2025) (Zum Beispiel 1990 2025) "
                               "\n 'Eingabe' (Suche nach Jahr überspringen) "
                               "\n '=' (zurück zum Hauptmenü): ").strip()
            if year_input == "":
                break
            elif year_input == "=":
                return
            else:
                year_parts = year_input.split()
                if len(year_parts) == 1:
                    if validate_year_input(year_parts[0]):
                        year_filter = int(year_parts[0])
                        save_search_query(f"year: {year_filter}") # Speichern Sie das ausgewählte spezifische Jahr
                        break
                elif len(year_parts) == 2:
                    if validate_year_range(year_parts):
                        start_year, end_year = map(int, year_parts)
                        year_filter = (start_year, end_year)
                        save_search_query(f"years: {start_year}-{end_year}")
                        break
                else:
                    print(Fore.RED + Style.BRIGHT + "Falsche Eingabe. Versuchen Sie es erneut.")

        # Nun suchen wir nach Filmen nach den ausgewählten Filtern
        offset = 0
        while True:
            # Rufen Sie die Suchfunktion unter Berücksichtigung der ausgewählten Filter auf
            kwargs = {"limit": 10, "offset": offset}

            if genre:
                kwargs["genre"] = genre
            if isinstance(year_filter, int):
                kwargs["year"] = year_filter
            elif isinstance(year_filter, tuple):
                kwargs["year_range"] = year_filter

            movies, total_count = search_movies(**kwargs)
            description_parts = []
            if genre:
                description_parts.append(f"genre '{genre}'")
            if isinstance(year_filter, int):
                description_parts.append(f"year {year_filter}")
            elif isinstance(year_filter, tuple):
                description_parts.append(f"von {year_filter[0]} bis {year_filter[1]}")
            description = " und ".join(description_parts) if description_parts else "kein Filter nach Genre und Jahr"

            print_results(movies, total_count, f"Filme nach Filter: {description}", offset)

            if not movies or offset + 10 >= total_count:
                print("Keine weiteren Filme gefunden.")
                break

                # Weiter oder Zurück zum Hauptmenü
            cont = input(Fore.LIGHTYELLOW_EX +
                "Geben Sie '-' für die nächsten 10 Filme ein \n'Leertaste' - Suche beenden: " + Style.RESET_ALL).strip().lower()
            if cont == '-':
                offset += 10
            else:
                break


        user_choice = input(
            "Möchten Sie mit neuen Filtern weitersuchen? \n'-' -weiter or 'Leertaste' - Zurück zum Hauptmenü: ").strip().lower()
        if user_choice == '-':
            return search_by_genre()
        else:
            return

