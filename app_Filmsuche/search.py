from db import cursor_read
import logging
from colorama import Fore, Back, Style, init

def search_movies(keyword=None, genre=None, year=None, year_range=None, limit=10, offset=0):
    try:
        base_query = """
                     SELECT title,
                            release_year,
                            name AS category,
                            length,
                            rental_rate,
                            rating,
                            CASE
                                WHEN rating = 'G' THEN 'General Audience'
                                WHEN rating = 'PG' THEN 'Parental Guidance Suggested'
                                WHEN rating = 'PG-13' THEN 'Parents Strongly Cautioned'
                                WHEN rating = 'R' THEN 'Restricted'
                                WHEN rating = 'NC-17' THEN 'Adults Only'
                            END AS rating_description, description
                     FROM film_category t2
                     INNER JOIN film t1 ON t1.film_id = t2.film_id
                     INNER JOIN category t3 ON t2.category_id = t3.category_id
                     WHERE 1 = 1
                     """
        if keyword:
            base_query += f" AND UPPER(title) LIKE UPPER('%{keyword}%')"
        if genre:
            base_query += f" AND UPPER(name) LIKE UPPER('%{genre}%')"
        if year:
            base_query += f" AND release_year = {year}"
        if year_range:
            start_year, end_year = year_range
            base_query += f" AND release_year BETWEEN {start_year} AND {end_year}"


        base_query += f" LIMIT {limit} OFFSET {offset}"

        cursor_read.execute(base_query)
        results = cursor_read.fetchall()

        count_query = """
                      SELECT COUNT(*)
                      FROM film_category t2
                      INNER JOIN film t1 ON t1.film_id = t2.film_id
                      INNER JOIN category t3 ON t2.category_id = t3.category_id
                      WHERE 1 = 1
                      """
        if keyword:
            count_query += f" AND UPPER(title) LIKE UPPER('%{keyword}%')"
        if genre:
            count_query += f" AND UPPER(name) LIKE UPPER('%{genre}%')"
        if year:
            count_query += f" AND release_year = {year}"
        if year_range:
            count_query += f" AND release_year BETWEEN {start_year} AND {end_year}"

        cursor_read.execute(count_query)
        total_movies = cursor_read.fetchone()[0]
        return results, total_movies
    except Exception:
        logging.exception(Fore.RED + Style.BRIGHT + "Error while searching for movies!")

