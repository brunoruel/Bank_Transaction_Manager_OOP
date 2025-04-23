import time

from colorama import Fore, Style

from utils_functions import clear_console, type_writer, pretty_print, press_enter_to_continue, check_user_choice
from files_import import FileImport, FileSaving
from CONSTANTS_url import url_categories_json

from objects_transactions import Transactions_list
from objects_categories_keywords import CategoriesManager


class MenuInterface:


    def check_user_choice(self, max_answer):
        try:
            user_choice = int(user_choice)
        except ValueError:
            pretty_print("❌Not a valid choice - please try again", style=Fore.RED)
            input()
        else:
            if not 1 <= user_choice <=4:
                pretty_print("❌Not a valid choice - please try again", style=Fore.RED)
                input()
            else:
                return user_choice
            
    def show_welcome_menu(self):
        lines = [
        "=" * 60,
        "💸  Welcome to Bank Transaction Manager  💸".center(60),
        "=" * 60]
        lines2 = [
        "🔍  This tool helps you manage and categorize your banking transactions.",
        "📁  Load your transaction file, review unidentified entries,",
        "🧠  assign categories, tweak keywords, and export your data like a pro!"]
        lines3 = [
        f"⚙️  Ready to take control of your finances? Let’s get started!{Style.RESET_ALL}" 
        ]

        for line in lines:
            type_writer(line, style=Fore.CYAN)
            time.sleep(0.1)
        print()
        for line in lines2:
            type_writer(line)
            time.sleep(0.1)
        print()
        for line in lines3:
            type_writer(line, style=Fore.YELLOW)
            time.sleep(0.1)

        input("""                 
              
                    PRESS ENTER TO START""")

        clear_console()

    def upload_transactions_file(self):
        print()
        pretty_print(f"Upload here your WESTPAK transaction file", style=Fore.CYAN + Style.BRIGHT, clear=True)
        pretty_print("Please make sure it's a CSV file from your bank account",left_padding=0, style=Fore.CYAN + Style.BRIGHT)
        print()
        print()
        file_path = input()
        clear_console()
        print(f"""{Fore.CYAN}{Style.BRIGHT}FILE UPLOADED""")
        clear_console()
        
        return file_path

    def main_menu_interface(self):
        while True:
            pretty_print("MAIN MENU", top_padding=1, left_padding= 3,clear=True, style=Fore.CYAN)
            print()
            print("Please select an option:")
            print()
            print("1 - Review Categories for unidentified transactions")
            print()
            print("2 - Transactions modifications")
            print()
            print("3 - Categories / Keywords modifications")
            print()
            print("4 - Upload the transactions to Excel")
            print()
            user_choice = input("Your choice: ")
            print()
            if check_user_choice(user_choice, 4):
                return int(user_choice)
                
    def categories_menu_interface(self):
        while True:
            pretty_print("CATEGORIES/KEYWORDS MENU", top_padding=1, left_padding= 3,clear=True, style=Fore.CYAN)
            print()
            print("Please select an option:")
            print()
            print("1 - Add a keyword to a category")
            print()
            print("2 - Remove a keyword from a category")
            print()
            print("3 - Add a categorie")
            print()
            print("4 - Save changes")
            print()
            print("5 - Main Menu")
            print()
            user_choice = input("Your choice: ")
            if check_user_choice(user_choice, 5):
                return int(user_choice)


class AppStart:
    def __init__(self):
        self.interface = MenuInterface()
        self.importer = None
        self.transactions = None
        self.keywords = FileImport(url_categories_json, "json").init_import().run_import()
        self.categorie = CategoriesManager(self.keywords)

    def initiate_startup(self):
        # self.interface.show_welcome_menu()
        file_path = MenuInterface().upload_transactions_file().strip("'")
        self.importer = FileImport(file_path, "csv").init_import().run_import()
        self.transactions = Transactions_list(self.importer, self.categorie)
        pretty_print(" ✅ File Imported Successfully", style=Fore.GREEN)
        press_enter_to_continue()


    def categories_menu(self):
        while True:
            saved_changes = False
            user_choice = self.interface.categories_menu_interface()
            if user_choice == 1:
                self.categorie.add_kw_from_user()
                continue
            if user_choice == 2:
                self.categorie.remove_kw_from_categorie()
            if user_choice == 3:
                self.categorie.add_category()
                continue
            if user_choice == 4:
                FileSaving().json_saving(url_categories_json, self.keywords)
                pretty_print("📁Categories modifications saved successfully", style=Fore.GREEN, clear=True)
                saved_changes = True
                continue
            if user_choice == 5:
                if not saved_changes:
                    pretty_print("📁Categories modifications has not been saved, are you sur you want to proceed?", style=Fore.RED, clear=True)
                    danger = input("'y' for YES or press enter to cancel: ")
                    if danger == "y":
                        return
    

    def main_menu(self):
        while True:
            user_choice = self.interface.main_menu_interface()
            if user_choice == 1:
                pass
            if user_choice == 2:
                pass
            if user_choice == 3:
                self.categories_menu()
            if user_choice == 4:
                pass



test = AppStart()
test.initiate_startup()
test.main_menu()