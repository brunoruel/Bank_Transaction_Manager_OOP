from colorama import init, Fore, Style
init(autoreset=True)
import time

from files_import import FileSaving
from utils_functions import InterfaceStyle, InterfaceTool
from user_interface import CategorieInterface

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


    @property
    def categories_keys(self):
        return list(self.categories_dict.keys())


    def categorie_match(self, narrative):
        for key, value in self.categories_kws.items():
            if value.narrative_kw_match(narrative):
                return key
        return "Non identifiee"


    def remove_kw_from_categorie(self):
        cat_choice = CategorieInterface.get_cat_from_user(self.categories_keys)

        if not cat_choice:
            return None
        
        kws_list = self.categories_dict[cat_choice]
        kw_to_remove = CategorieInterface.get_kw_from_user(kws_list)

        if kw_to_remove == "":
            return None


        if CategorieInterface.get_confirmation(kw_to_remove):
            return self.categories_kws[cat_choice].remove_kw(kw_to_remove)
        else:
            return None
        
    def add_kw_from_user(self):
        cat = CategorieInterface.get_cat_from_user(self.categories_keys)
        if not cat:
            return
        while True:
            kw_to_add = CategorieInterface.get_new_key_word_single(cat)
            return self.categories_kws[cat].add_keywords(kw_to_add)
        
        
    def add_category(self):
        new_keywords = []
        new_category = ""

        new_category = CategorieInterface.get_new_categorie(self.categories_keys)
        if not new_category:
            return

        while True:
            new_keyword = CategorieInterface.get_new_key_word(new_keywords, new_category)

            if new_keyword:
                new_keywords.append(new_keyword)
            else:
                break

        
        self.categories_kws[new_category] = CategorieKeywords(new_category, new_keywords)
        self.categories_dict[new_category] = self.categories_kws[new_category].kws_list


    def remove_category(self):
        cat_to_delete = CategorieInterface.get_category_to_remove(self.categories_keys)

        if CategorieInterface.get_confirmation(cat_to_delete):
            del self.categories_kws[cat_to_delete]
            del self.categories_dict[cat_to_delete]
            return
        else:
            return
        
        
    def save_changes(self, url, cat_dict):
        FileSaving.json_saving(url, cat_dict)
        print(f"🟢 Changes saved")
        time.sleep(2)



