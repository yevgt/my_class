from db import print_search_count
from menu_search import search_by_keyword, search_by_genre
import sys
from rich import print
from rich.console import Console
from colorama import Fore, Style

console = Console()

def main_menu():
    while True:
        print(Fore.LIGHTGREEN_EX +"\n   [bold green]Select request number[/bold green]:  "+ Style.RESET_ALL)
        print("1. Search by part of the name (10+ results)")
        print("2. Search by genre (10+ results)")
        print("3. Display popular queries")
        print("0. Exit")

        choice = input("Your choice: ")
        if choice == "1":
            search_by_keyword()
        elif choice == "2":
            search_by_genre()
        elif choice == "3":
            print_search_count()
        elif choice == "0":
            print("Exiting the program... Goodbye! ;)")
            exit()
        else:
            print("Incorrect choice. Try again.")




