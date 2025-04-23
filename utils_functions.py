import os
import time
import shutil
from colorama import Fore, Style


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def type_writer(text, delay=0.02, style='', clear=False):
    if clear:
        clear_console()

    for char in text:
        print(f"{style}{char}", end = '', flush=True)
        time.sleep(delay)
    print()
  

def pretty_print(text: str, top_padding: int = 3, left_padding: int = 5, style: str = '', clear=False):
    if clear:
        clear_console()

    lines = text.strip().split('\n')

    # Add vertical padding
    print('\n' * top_padding, end='')

    # Add horizontal padding and apply style
    for line in lines:
        print(' ' * left_padding + f"{style}{line}")

def press_enter_to_continue(top_padding: int = 3, left_padding: int = 10, clear = False):
    if clear:
        clear_console()
    print()
    print()
    press_enter = "PRESS ENTER TO CONTINUE"

    lines = press_enter.strip().split('\n')

    print('\n' * top_padding, end='')

    for line in lines:
        print(' ' * left_padding + f"{Fore.CYAN}{Style.BRIGHT}{line}")
    input()


def check_user_choice(user_choice, max_answer):
    try:
        user_choice = int(user_choice)
    except ValueError:
        pretty_print("❌Not a valid choice - please try again", style=Fore.RED)
        input()
    else:
        if not 1 <= user_choice <= max_answer:
            pretty_print("❌Not a valid choice - please try again", style=Fore.RED)
            input()
        else:
            return True
    return False