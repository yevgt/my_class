from search import search_movies
from utils import print_results
from db import save_search_query, cursor_read
from valid_years import validate_year_input, validate_year_range
from db import get_genres
import logging
from colorama import Fore, Back, Style, init


def search_by_keyword():
    while True:
        keyword = input("Введите часть названия (или '=' для выхода): ")
        if keyword.strip() == "=":
            return  # Return to main menu
        save_search_query(f"Слово (часть слова):'{keyword}'")
          # Save or update the query in the database

        offset = 0  # Initial shift value
        while True:
            # Searching for movies
            movies, total_count = search_movies(keyword=keyword, limit=10, offset=offset)
            print_results(movies, total_count, f"Movies matching keyword '{keyword}'", offset)

            # If there are no more movies to display, exit
            if not movies:
                print("There are no movies to display.")
                break

            # Request for further action
            next_action = input("Enter '-' for the next 10 movies, \n'=' to exit the search \n'Space' for the new search: ").strip().lower()
            if next_action == '=':
                return  # Return to main menu
            elif next_action == '-':
                offset += 10  # Increase the offset by 10
            else:
                break

def search_by_genre():
    genres = get_genres()

    while True:
        # Genre selection block (can be skipped)
        genre = None
        while True:
            genre_choice = input("Select genre number, \n'Enter' (to skip the genre) \n '=' (return to main menu): ").strip()
            if genre_choice == "=":
                return  # Return to main menu
            elif genre_choice == "":
                genre = None
                break
            try:
                genre_choice_int = int(genre_choice)
                if 1 <= genre_choice_int <= len(genres):
                    genre = genres[genre_choice_int - 1][1]
                    save_search_query(f"genre: {genre}")  # Save the selected genre
                    break
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                logging.exception("Please enter a number or press 'Enter' to skip.")

        # Year/Year Range Selection Block
        year_filter = None  # None - not filter by year
        while True:
            year_input = input("Enter year (YYYY) or range whith 'Space' (from 1990 to 2025) (For example, 1990 2025) "
                               "\n 'Enter' (skip search by year) "
                               "\n '=' (return to main menu): ").strip()
            if year_input == "":
                break
            elif year_input == "=":
                return
            else:
                year_parts = year_input.split()
                if len(year_parts) == 1:
                    if validate_year_input(year_parts[0]):
                        year_filter = int(year_parts[0])
                        save_search_query(f"year: {year_filter}") # Remember that you chose a specific year
                        break
                elif len(year_parts) == 2:
                    if validate_year_range(year_parts):
                        start_year, end_year = map(int, year_parts)
                        year_filter = (start_year, end_year)
                        save_search_query(f"years: {start_year}-{end_year}")
                        break
                else:
                    print("Incorrect input. Try again.")

        # Now we search for films according to the selected filters
        offset = 0
        while True:
            # call the search function taking into account the selected filters
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
                description_parts.append(f"from {year_filter[0]} to {year_filter[1]}")
            description = " and ".join(description_parts) if description_parts else "no filter by genre and year"
            save_search_query(f"Genre and year(s): {description}")

            print_results(movies, total_count, f"Movies by filter: {description}", offset)

            if not movies or offset + 10 >= total_count:
                print("No more movies found.")
                break

                # continue or exit to main menu
            cont = input(
                "Enter '-' for the next 10 movies \n'Space' - exit to the main menu: ").strip().lower()
            if cont == '-':
                offset += 10
            else:
                break


        user_choice = input(
            "Do you want to continue searching with new filters? ('-' or 'Space' - exit to the main menu): ").strip().lower()
        if user_choice == '-':
            return search_by_genre()
        else:
            return

