import os
import logging
from menu import main_menu
from colorama import Fore, Back, Style, init

# Create a folder for logs if it does not exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Setting up error logging
logging.basicConfig(
    filename='logs/error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    try:
        menu = main_menu()
        menu.run()
    except Exception:
        logging.exception("Critical error in main file.")

if __name__ == "__main__":
    main()