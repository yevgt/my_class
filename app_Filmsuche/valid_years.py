import logging
from colorama import Fore, Back, Style, init

# Validierung des Jahres
def validate_year_input(year_str):
    try:
        year = int(year_str)
        if 1990 <= year <= 2025:
            return True
        else:
            print(Fore.LIGHTRED_EX + "Fehler: Das Jahr muss zwischen 1990 und 2025 liegen.")
            return False
    except ValueError:
        logging.exception(Fore.LIGHTRED_EX + "Fehler: Bitte geben Sie ein gültiges Jahr ein.")
        return False

# Validierungsjahre
def validate_year_range(year_parts):
    try:
        start_year = int(year_parts[0])
        end_year = int(year_parts[1])
        if start_year < 1990 or end_year > 2025 or start_year > end_year:
            print(Fore.RED + Style.BRIGHT + "Fehler: Startjahr muss mindestens 1990 sein, "
                                            "Das Endjahr muss mindestens 2025 sein und darf nicht vor dem Startjahr liegen.")
            return False
        return True
    except ValueError:
        logging.exception(Fore.RED + Style.BRIGHT + "Fehler: Bitte geben Sie gültige Jahre für den Bereich ein.")