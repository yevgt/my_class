from tabulate import tabulate
from colorama import Fore, Back, Style, init

def print_results(results, total_count, description, offset):
    # Table Headers
    headers = ["#", "Title", "Release Year", "Category", "Length", "Rental Rate", "Rating", "Rating Description", "Description"]

    print(f"\n{description}:")
    if results:
        indexed_results = [(index, *movie) for index, movie in enumerate(results, start=offset + 1)]
        print(tabulate(indexed_results, headers=headers, tablefmt="fancy_grid",
                       numalign="center",
                       stralign="center",
                       maxcolwidths=[10, 15, 10, 10, 10, 10, 10, 20, 30]))
        print(f"\nTotal count of movies: {total_count}\n")
    else:
        return



