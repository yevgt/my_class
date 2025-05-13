import logging
from colorama import Fore, Back, Style, init

def validate_year_input(year_str):
    try:
        year = int(year_str)
        if 1990 <= year <= 2025:
            return True
        else:
            print("Error: year must be between 1990 and 2025.")
            return False
    except ValueError:
        logging.exception("Error: Please enter a valid year.")
        return False

def validate_year_range(year_parts):
    try:
        start_year = int(year_parts[0])
        end_year = int(year_parts[1])
        if start_year < 1990 or end_year > 2025 or start_year > end_year:
            print("Error: Start year must be at least 1990, end year must be at least 2025 and cannot be less than start year.")
            return False
        return True
    except ValueError:
        logging.exception("Error: Please enter valid years for the range.")