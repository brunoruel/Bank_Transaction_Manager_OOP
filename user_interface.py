import time

from colorama import Fore, Style

from utils_functions import InterfaceTool, InterfaceStyle
from files_import import FileImport, FileSaving
from CONSTANTS_url import url_categories_json




class MenuInterface:

            
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
            InterfaceStyle.type_writer(line, style=Fore.CYAN)
            time.sleep(0.1)
        print()
        for line in lines2:
            InterfaceStyle.type_writer(line)
            time.sleep(0.1)
        print()
        for line in lines3:
            InterfaceStyle.type_writer(line, style=Fore.YELLOW)
            time.sleep(0.1)

        input("""                 
              
                    PRESS ENTER TO START""")

        InterfaceStyle.clear_console()

    def upload_transactions_file(self):
        print()
        InterfaceStyle.pretty_print(f"Upload here your WESTPAK transaction file", style=Fore.CYAN + Style.BRIGHT, clear=True)
        InterfaceStyle.pretty_print("Please make sure it's a CSV file from your bank account",left_padding=0, style=Fore.CYAN + Style.BRIGHT)
        print()
        print()
        file_path = input()
        print(f"""{Fore.CYAN}{Style.BRIGHT}FILE UPLOADED""")
        
        return file_path


    def main_menu_interface(self):
        while True:
            InterfaceStyle.pretty_print("MAIN MENU", top_padding=1, left_padding= 3,clear=True, style=Fore.CYAN)
            print()
            print("Please select an option:")
            print()
            print("1 - Review Categories for unidentified transactions")
            print()
            print("2 - Narrative modification")
            print()
            print("3 - Categories / Keywords modifications")
            print()
            print("4 - Upload the transactions to Excel")
            print()
            user_choice = input("Your choice: ")
            print()
            if InterfaceTool.check_user_choice(user_choice, 4):
                return int(user_choice)
                

    def categories_menu_interface(self):
        while True:
            InterfaceStyle.pretty_print("CATEGORIES/KEYWORDS MENU", top_padding=1, left_padding= 3,clear=True, style=Fore.CYAN)
            print()
            print("Please select an option:")
            print()
            print("1 - Add a keyword to a category")
            print()
            print("2 - Remove a keyword from a category")
            print()
            print("3 - Add a categorie")
            print()
            print("4 - Remove a category")
            print()
            print("5 - Save changes")
            print()
            print("6 - Main Menu")
            print()
            user_choice = input("Your choice: ")
            if InterfaceTool.check_user_choice(user_choice, 6):
                return int(user_choice)


class CategorieInterface:

    @staticmethod
    def get_confirmation(to_remove):
        print()
        print(f"🔴 Are you sure you want to remove {to_remove}?")
        print()
        danger = input("'y' for YES or press enter to cancel: ")
        if danger == "y":
            return True
        else:
            return False


    # ===============REMOVE KEY WORDS ============

    @staticmethod
    def get_cat_from_user(categories_keys):
        InterfaceStyle.clear_console()
        print("Which categorie would you like to modify: ")
        print()

        for i, cat in enumerate(categories_keys):
            print(f"{i+1} - {cat}")
        print("q - Cancel")

        while True: 
            print()
            user_choice = input("Your choice: ")
            if user_choice == "q":
                return None
            try:
                user_choice = int(user_choice)
            except ValueError:
                print(f"🔴 Not a valide entry")
            else:
                try:
                    user_choice = categories_keys[user_choice - 1]
                except IndexError:
                    print(f"🔴 Not a valide entry")
                    continue
                else:
                    return user_choice
                
    @staticmethod
    def get_kw_from_user(kws_list):

        print()
        InterfaceStyle.clear_console()
        print(f"Which keyword would you like to remove?")
        print()
        for i, kw in enumerate(kws_list):
            print(f"{i+1} - {kw}")
        print("q - Cancel")
        while True:
            print()
            kw_choice = input("Your choice: ")
            if kw_choice == "q":
                return ""
            try:
                kw_choice = int(kw_choice)
            except ValueError:
                print(f"🔴 Not a valide entry")
            else:
                if 1 <= kw_choice <= len(kws_list):
                    return kws_list[kw_choice -1]
                else:
                    print(f"🔴 Not a valide entry")

    

    #==============   ADD NEW KEW WORDS ==============================

    @staticmethod
    def get_new_key_word_single(cat):
        print()
        kw_to_add = input(f"Enter the key word you want to add to the {cat} category: ")
        print()
        print(f"🟢 {kw_to_add} added to {cat}")
        return kw_to_add

    #================  ADD CATEGORIES ======================

    @staticmethod
    def get_new_categorie(categories_keys):
        while True:
            InterfaceStyle.clear_console()
            new_category = input("Enter the name of the new categorie (enter to cancel): ")

            if new_category and new_category in categories_keys:
                print()
                print("Category already created, find another name.")
            elif not new_category:
                return None
            else:
                return new_category
            
    @staticmethod
    def get_new_key_word(new_kws, new_cat):
        InterfaceStyle.clear_console()
        new_keyword = input("Enter the name of a new keyword (enter to cancel): ")

        if new_keyword and new_keyword in new_kws:
            print("🔴 Keyword already added, find another name.")
        elif not new_keyword:
            return None
        else:
            add_print = f"{len(new_kws)} key words added" if new_kws else "no keywords added"
            print(f"The {new_cat} has been added, {add_print}")
            return new_keyword
        
    #====================  REMOVE CATEGORIE ======================

    @staticmethod
    def get_category_to_remove(categories_keys):
        while True:
            InterfaceStyle.clear_console()
            for i, cat in enumerate(categories_keys):
                print(f"{i+1} - {cat}")
            print("q - Cancel")

            print("Which category would you like to delete: ")
            print()

            user_choice = input("Your choice: ")

            if user_choice == "q":
                return None
            
            if  InterfaceTool.check_user_choice(user_choice, len(categories_keys) + 1):
                user_choice = int(user_choice)
                cat_to_delete = categories_keys[user_choice - 1]
                return cat_to_delete
            else:
                print(f"🔴 Not a valide entry")

    #=====================  SAVE CATEGORIES CHANGES ================

    @staticmethod
    def get_saving_confirmation(modifications_count):
        while True:
            InterfaceStyle.pretty_print(f"📁 {modifications_count} categories modifications were not saved, are you sur you want to proceed?", style=Fore.RED, clear=True)
            print()
            danger = input("'y' for YES or 's' to save the modifications and exit")
            if danger == "y":
                return False
            elif danger == "s":
                return True
            else:
                print(f"🔴 Not a valide entry")


class TransactionsInterface:

    #=======  USER TO ASSIGN CATEGORY FOR UNIDENTIFIED TRANSACTION  ===
    
    @staticmethod
    def get_cat_to_assign(categories_list, narrative, tx_count):
        while True:
            InterfaceStyle.pretty_print(f"{tx_count} Unidentified Transactions", style=Fore.BLUE, clear=True)
            InterfaceStyle.pretty_print("Choose a categorie to assign to the transactions", style=Fore.BLUE)
            print()

            for j, value in enumerate(categories_list):
                print(f"{j + 1} - {value}")
            print("'q' - Exit without saving")
            print("'s' - Save Modification")
            print()
            InterfaceStyle.pretty_print(f"{narrative}", style=Fore.LIGHTYELLOW_EX)
            print()

            choice = input("Your choice: ")
            if choice == "q":
                return None
            
            elif choice == "s":
                return choice
            
            elif  InterfaceTool.check_user_choice(choice, len(categories_list)):
                    return int(choice) - 1
            
            else:
                    InterfaceStyle.pretty_print("❌ Incorrect choice, please try again", style=Fore.RED)


    #==============  USER TO MODIFY NARRATIVE ==========================



    def ui_modify_tx_narrative(tx_by_month, month_list):
        if len(month_list) > 1 :
            for i, month in enumerate(month_list):
                print(f"{i + 1} - {month}")

            print("'q' - Cancel")
            print()
            while True:
                month_choice = input(f"Choose a month for the transaction you wish to modify: ")
                if month_choice == "q":
                    tx = ""
                    narrative_choice = ""
                    return tx, narrative_choice
                elif InterfaceTool.check_user_choice(month_choice, len(month_list)):
                    month_choice = month_list[int(month_choice) - 1]
                    break
        else:
                month_choice = month_list[0]

        tx_list_to_modify = tx_by_month[month_choice]

        for i, tx in enumerate(tx_list_to_modify):
            print(f"{i + 1} - {str(tx.date.strftime("%d/%m/%Y"))} - {tx.narrative} - {tx.amount} - {tx.category}")
        print("'q' - Cancel")

        print()
        while True:
            tx_choice = input("Which Transaction would you like to modify: ")
            if tx_choice == "q":
                tx = ""
                narrative_choice = ""
                return tx, narrative_choice
            elif InterfaceTool.check_user_choice(tx_choice, len(tx_list_to_modify)):
                break

        tx = tx_list_to_modify[int(tx_choice) - 1]
        narrative_choice = input(f"What narrative would you like to replace {tx.narrative} with: ")

        return tx, narrative_choice