import re
from datetime import datetime
from files_import import FileImport
from CONSTANTS_main import ConstantsTx
from CONSTANTS_url import url_json
from copy import deepcopy
from collections import defaultdict


# from var_test import raw_tx_test, unidentified_tx, cleaned_data_full_list, raw_data_list, pipeline_categories

class DataCleaner:
    def __init__(self, raw_tx):

        if not isinstance(raw_tx, dict):
            raise TypeError("raw_tx must be a dictionary")
        self.raw_tx = deepcopy(raw_tx)

    def convert_date_to_datetime(self):
        try:
            self.raw_tx["Date"] = datetime.strptime(self.raw_tx['Date'], "%d/%m/%Y")
            return True
        except TypeError:
            return False

    def clean_narrative(self):

        for words in ConstantsTx.TO_DELETE_IN_NARRATIVE:
            self.raw_tx["Narrative"] = re.sub(words, "", self.raw_tx["Narrative"], flags=re.IGNORECASE)

        self.raw_tx["Narrative"] = re.sub(r"\s{2,}", " ",self.raw_tx["Narrative"])
        self.raw_tx["Narrative"] = re.sub(r"\d{4,}", "",self.raw_tx["Narrative"])
        self.raw_tx["Narrative"] = self.raw_tx["Narrative"].strip().title()

    def categories_add(self):
        if not ConstantsTx.CATEGORIES_KEY_WORDS:
            return
        for key, value in ConstantsTx.CATEGORIES_KEY_WORDS.items():
            for key_word in value:
                if key_word.lower() in self.raw_tx["Narrative"].lower():
                    self.raw_tx["Narrative"] = key if key in ConstantsTx.CATEGORIES_AS_NARRATIVE else key_word
                    self.raw_tx["Categorie"] = key
                    return self.raw_tx
        self.raw_tx["Categorie"] = "Non identifiee"

    def convert_str_to_float(self):
        for key in ConstantsTx.FLOAT_KEYS:
            value = self.raw_tx.get(key, "")
            try:
                self.raw_tx[key] = float(value) if value else 0.0
            except ValueError:
                return False
        return True
    
    def __repr__(self):
        return str(self.raw_tx)

    def run_data_cleaning(self) -> dict:
        if not self.convert_date_to_datetime() or not self.convert_str_to_float():
            return {}
        self.categories_add()
        self.clean_narrative()
        return self.raw_tx
    

class TransactionFormater:
    def __init__(self, tx):

        if not isinstance(tx, dict):
            raise TypeError("raw_tx must be a dictionary")
        self.tx = tx
        self.formated_tx = {}

    def add_amount_column(self):
        self.tx["Amount"] = float(self.tx["Credit Amount"] - self.tx["Debit Amount"])

    def account_column(self):
        for key, value in ConstantsTx.ACCOUNTS.items():
            if self.tx["Bank Account"] == value:
                self.tx["Account"] = key
                return self.tx["Account"]
        self.tx["Account"] = "Compte non identifie"

    def columns_filter(self):
        self.formated_tx = {x:self.tx[x] for x in ConstantsTx.COLUMNS_TO_KEEP}
    
    def add_year_month_column(self):
        self.tx["Year"] = str(self.tx["Date"].year)
        self.tx["Month"] = str(self.tx["Date"].month)

    def run_transaction_formater(self) -> dict:
        self.account_column()
        self.add_amount_column()
        self.add_year_month_column()
        self.columns_filter()
        return self.formated_tx
    

class CategoriesByUser:

    def __init__(self, data, tx_indexes, unmodified_data):
        self.data = data
        self.tx_indexes = tx_indexes
        self.unidentified_tx_amount = len(self.tx_indexes)
        self.identified_tx_by_user = {}
        self.unmodified_data = unmodified_data

    def ask_user_if_categories_modification(self):
        
        if self.unidentified_tx_amount > 0:
            print(f"\n{self.unidentified_tx_amount} non identified transactions\n")
            print("Do you want to adjust the categories y for yes, any keys for no\n")
            user_choice = input("Your choice: ")
            return True if user_choice == "y" else False

    def ask_user_input(self, narrative, index, counter):

        other_options = ["q"]
        print("Choose a categorie:" )
        for key, value in ConstantsTx.CATEGORIES_CHOICES.items():
            print(f"{key} : {value}")
        print("q - End categories modifications")
        if self.identified_tx_by_user:
            print("u - undo last entry")
            
            other_options.append("u")

        while True:
            user_choice = input(f"{counter} / {self.unidentified_tx_amount} - {narrative} ${self.data[index]["Amount"]}: ")
            if user_choice in list(ConstantsTx.CATEGORIES_CHOICES.keys()) or user_choice in other_options:
                return user_choice
            else:
                print("Incorrect input, please enter a valid entry!")

    def delete_previous_entry(self, index):
        last_entry = list(self.identified_tx_by_user.keys())[-1]
        print(f"Last entry deleted - {last_entry}")
        del self.identified_tx_by_user[last_entry]
        
    def modify_categories_with_user_input(self):
        choice_counter = 1
        index = 0
        while index < len(self.tx_indexes):
            i = self.tx_indexes[index]
        
            narrative = self.data[i]["Narrative"]

            if self.identified_tx_by_user and narrative in list(self.identified_tx_by_user.keys()):
                category = self.identified_tx_by_user[narrative]

            else:
                user_choice = self.ask_user_input(narrative, i, choice_counter)

                if user_choice == "q":
                    FileImport.save_json_data(ConstantsTx.CATEGORIES_KEY_WORDS, url_json)
                    return self.data
                
                elif user_choice == "u":
                    self.delete_previous_entry(index)
                    index -= 1
                    choice_counter -= 1
                    continue
                
                else:
                    category = ConstantsTx.CATEGORIES_CHOICES[user_choice]             
                    ConstantsTx.CATEGORIES_KEY_WORDS[category].append(self.unmodified_data[i]["Narrative"])
                    self.identified_tx_by_user[narrative] = category
    
            self.data[i]["Categorie"] = category
            index +=1
            choice_counter += 1

        FileImport.save_json_data(ConstantsTx.CATEGORIES_KEY_WORDS, url_json)
        return self.data

    def run_categories_by_user(self):
        if self.ask_user_if_categories_modification():
            self.modify_categories_with_user_input()

        return self.data
        

class DataPipeLine:
    month_year_keys = []

    def __init__(self, data):

        if not isinstance(data, list):
            raise TypeError("raw_tx must be a list")
        self.processed_transactions = 0
        self.data = deepcopy(data)
        self.categorized_transactions = defaultdict(list)
        self.non_identified_tx_index = []
        self.unmodified_data = deepcopy(data)

    @staticmethod
    def sort_transactions(tx_list):
        tx_list.sort(key=lambda x:x["Date"])

    def categorize_tx(self, tx):
        tx_month_year = tx["Date"].strftime('%B %Y')
        self.categorized_transactions[tx_month_year].append(tx)
        DataPipeLine.month_year_keys.append(tx_month_year) if tx_month_year not in DataPipeLine.month_year_keys else None

    def run_pipeline(self):

        # DataPipeLine.sort_transactions(self.data)

        for i in range(len(self.data)):
            tx_cleaning = DataCleaner(self.data[i])     
            cleaned_tx = tx_cleaning.run_data_cleaning()
            if cleaned_tx == {}:
                continue

            tx_formatage = TransactionFormater(cleaned_tx)
            formated_transaction = tx_formatage.run_transaction_formater()

            self.data[i] = formated_transaction
            self.processed_transactions += 1

            if self.data[i]["Categorie"] == "Non identifiee":
                self.non_identified_tx_index.append(i)


        if self.non_identified_tx_index:
            categorise_non_identified_tx = CategoriesByUser(self.data, self.non_identified_tx_index, self.unmodified_data)
            self.data = categorise_non_identified_tx.run_categories_by_user()

        self.sort_transactions(self.data)

        for tx in self.data:
            self.categorize_tx(tx)

        print(f"\u2705 - {self.processed_transactions} transactions successfully processed")

        return self.categorized_transactions             
        
        





