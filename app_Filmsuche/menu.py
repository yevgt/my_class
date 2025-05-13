from db import print_search_count
from menu_search import search_by_keyword, search_by_genre
import sys
from rich import print
from rich.console import Console
from colorama import Fore, Style

console = Console()

def main_menu():
    while True:
        print(Fore.LIGHTGREEN_EX +"\n   [bold green]Anfragenummer auswählen[/bold green]:  "+ Style.RESET_ALL)
        print("✅1." + Fore.BLUE + "Suche nach Namensteil (10+ Ergebnisse)")
        print("✅2." + Fore.BLUE + "Suche nach Genre und Jahr (10+ Ergebnisse)")
        print("✅3." + Fore.BLUE + "Beliebte Suchanfragen anzeigen")
        print("⚠️0." + Fore.MAGENTA + "Exit"+ Style.RESET_ALL)

        choice = input("\nIhre Wahl: ")
        if choice == "1":
            search_by_keyword()
        elif choice == "2":
            search_by_genre()
        elif choice == "3":
            print_search_count()
        elif choice == "0":
            print(Fore.GREEN + "Das Programm wird beendet... Auf Wiedersehen! ;)")
            exit()
        else:
            print(Fore.RED + Style.BRIGHT + "Falsche Auswahl. Versuchen Sie es erneut..")




