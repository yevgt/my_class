from tabulate import tabulate
from colorama import Fore, Back, Style, init

# Funktion zur Ausgabe in eine Tabelle
def print_results(results, total_count, description, offset):
    # Tabellenüberschriften
    headers = ["#", "Title", "Erscheinungsjahr", "Kategorie", "Länge", "Bewertung", "MPA-Bewertungen",
               "Bewertungen \nBeschreibung", "Filmbeschreibung"]

    print(f"\n{description}:")
    if results:
        indexed_results = [(index, *movie) for index, movie in enumerate(results, start=offset + 1)]
        print(Fore.LIGHTCYAN_EX + tabulate(indexed_results, headers=headers, tablefmt="fancy_grid",
                       numalign="center",
                       stralign="center",
                       maxcolwidths=[10, 15, 10, 10, 10, 10, 10, 20, 25]) + Style.RESET_ALL)
        print(f"\nGesamtzahl der Filme: {total_count}\n")
    else:
        return



