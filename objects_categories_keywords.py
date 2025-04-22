from colorama import init, Fore, Style
init(autoreset=True)

from files_import import FileSaving, FileImport
from CONSTANTS_url import url_json
from var_test import cat_single_test

import_json = FileImport(url_json, "json").init_import()
CATEGORIES_KEY_WORDS = import_json.run_import()


class CategorieKeywords:
    def __init__(self, categorie_name: str, kws_list: list):
        self.categorie_name = categorie_name
        self.kws_list = kws_list

    def add_keywords(self, new_kw):
        if not new_kw in self.kws_list:
            return self.kws_list.append(new_kw)
        else:
            print(f"{new_kw} is already listed as a keyword for the {self.categorie_name} categorie")
            return None

    def remove_kw(self, kw_to_remove):
        lower_kw_to_remove = kw_to_remove.lower()
 
        for i, value in enumerate(self.kws_list):
            if lower_kw_to_remove == value.lower():
                print(f"{Fore.GREEN}✔️ {self.kws_list[i]} deleted from {self.categorie_name}")
                del self.kws_list[i]               
                return
            
        print(f"{Fore.RED}❌ Not a keyword for the '{self.cat}' category")

    def narrative_kw_match(self, narrative):
        return any(kw.lower() in narrative.lower() for kw in self.kws_list)
    
    def list_kw(self):
        print(f"{Fore.CYAN}🔎 Keywords in '{self.categorie_name}': {', '.join(self.kws_list)}")

    def to_dict(self) -> dict[str, list]:
        return {self.categorie_name: self.kws_list}
    


class CategoriesManager:
    def __init__(self, categories_dict):
        self.categories_kws = {key: CategorieKeywords(key, value) for key, value in categories_dict.items()}
        self.categories_dict = categories_dict
        self.categories_keys = list(categories_dict.keys())
        self.index_cat_dict = {i+1:cat for i, cat in enumerate(categories_dict)}


    def categorie_match(self, narrative):
        for key, value in self.categories_kws.items():
            if value.narrative_kw_match(narrative):
                print(f"🟢 Match found: '{narrative}' → '{key}'")
                return key
        print(f"🔴 No match found for: '{narrative}'")
        return "Non identifiee"

    def get_cat_from_user(self):
        print("Which categorie would you like to modify: ")
        print()

        for key, value in self.index_cat_dict.items():
            print(f"{key} - {value}")

        while True: 
            print()
            user_choice = input("Your choice: ")
            try:
                user_choice = int(user_choice)
            except ValueError:
                print(f"🔴 Not a valide entry")
            else:
                if user_choice in list((self.index_cat_dict.keys())):
                    break
                else:
                    print(f"🔴 Not a valide entry")
        return self.index_cat_dict[user_choice]

    def get_kw_from_user(self, kws_list):
        print()
        print(f"Which keyword would you like to remove?")
        print()
        for i, kw in enumerate(kws_list):
            print(f"{i+1} - {kw}")
        while True:
            print()
            kw_choice = input("Your choice: ")
            try:
                kw_choice = int(kw_choice)
            except ValueError:
                print(f"🔴 Not a valide entry")
            else:
                if 1 <= kw_choice <= len(kws_list):
                    return kws_list[kw_choice -1]
                else:
                    print(f"🔴 Not a valide entry")


    def remove_kw_from_categorie(self):
        cat_choice = self.get_cat_from_user()
        kws_list = self.categories_dict[cat_choice]
        kw_to_remove = self.get_kw_from_user(kws_list)
        print()
        print(f"🔴 Are you sure you want to remove {kw_to_remove} from the {cat_choice} category?")
        print()
        danger = input("'y' for YES or press enter to cancel: ")
        if danger == "y":
            return self.categories_kws[cat_choice].remove_kw(kw_to_remove)
        else:
            return None
        
    def add_kw_from_user(self):
        cat = self.get_cat_from_user()
        while True:
            print()
            kw_to_add = input(f"Enter the kew work you wante to add to the {cat} category: ")
            print()
            print(f"🟢 {kw_to_add} added to {cat}")
            print()
            return self.categories_kws[cat].add_keywords(kw_to_add)
        
    def save_changes(self):
        FileSaving.json_saving(url_json, self.categories_dict)
        print(f"🟢 Changes saved")


