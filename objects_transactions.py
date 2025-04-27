import re
from datetime import datetime
from collections import defaultdict
import pandas as pd
from colorama import Fore, Style
import time

from user_interface import TransactionsInterface
from utils_functions import InterfaceStyle, InterfaceTool
from files_import import FileSaving

from CONSTANTS_url import url_categories_json
from CONSTANTS_main import ConstantsTx





class Transaction:
    def __init__(self, raw_data:dict, category_instance):
        self.raw_data = raw_data
        self.cleaned_data = {}

        self.bank_account = raw_data.get("Bank Account", "")
        self.date = raw_data.get("Date", "")
        self.narrative = raw_data.get("Narrative", "")
        self.debit_amount = float(raw_data.get("Debit Amount", "") or 0)
        self.credit_amount = float(raw_data.get("Credit Amount") or 0)
        self.balance = raw_data.get("Balance", "")
        self.categories = raw_data.get("Categories", "")
        self.serial = raw_data.get("Serial", "")

        self.category = "Non identifiee"
        self.amount = 0.0
        self.account = "Compte non identifie"
        self.year = ""
        self.month = ""
        self.year_month = ""

        self.category_instance = category_instance

        self.format = {}

    def convert_date_to_datetime(self):
        if isinstance(self.date, str):
            try:
                self.date = datetime.strptime(self.date, "%d/%m/%Y")
            except TypeError:
                return None

    def compute_amount(self):
        try:
            self.amount = float(self.credit_amount) - float(self.debit_amount)
        except ValueError:
            self.amount = 0.0

    def categories_add(self, categorie_instance):
        self.category = categorie_instance.categorie_match(self.narrative)

    def clean_narrative(self):
        for words in ConstantsTx.TO_DELETE_IN_NARRATIVE:
            self.narrative = re.sub(words, "", self.narrative, flags=re.IGNORECASE)

        self.narrative = re.sub(r"\s{2,}", " ",self.narrative)
        self.narrative = re.sub(r"\d{4,}", "",self.narrative)
        self.narrative = self.narrative.strip().title()

    def account_column(self):
        for account_type, account_number in ConstantsTx.ACCOUNTS.items():
            if self.bank_account == account_number:
                self.account = account_type
                return self.account


    def add_year_month_column(self):
        self.year = str(self.date.year)
        self.month = str(self.date.month)
        self.year_month = self.date.strftime('%B %Y')

    def __repr__(self):
        return (
        f"{self.date.strftime('%d/%m/%Y')} | "
        f"{self.category:<20} | "
        f"{(self.credit_amount - self.debit_amount):>8.2f} € | "
        f"{self.narrative[:40]}"
    )

    def to_dict(self):
        return {
            "Account": self.account,
            "Date": self.date,
            "Narrative": self.narrative,
            "Amount": self.amount,
            "Category": self.category,
            "Balance": self.balance
        }
    
    def assign_category(self, category_choice):
        self.category = category_choice
        InterfaceStyle.pretty_print(f"✅ {category_choice} successfully assigned to {self.narrative}", style=Fore.GREEN)

    
    def run(self) -> dict:
        self.convert_date_to_datetime()
        self.compute_amount()
        self.categories_add(self.category_instance)
        self.clean_narrative()
        self.account_column()
        self.add_year_month_column()
        return self
    

class Transactions_list:
    def __init__(self, raw_data_list, categories_instance):
        self.categories_instance = categories_instance
        self.raw_data_list = [Transaction(raw, self.categories_instance) for raw in raw_data_list]
        self.transactions = [Transaction(cleaned_tx, self.categories_instance).run() for cleaned_tx in raw_data_list]
        self.sort_per_month = []


    def __iter__(self):
        return iter(self.transactions)
    
    def __len__(self):
        return len(self.transactions)
    
    def __getitem__(self, index):
        return self.transactions[index]
    
    def get_unidentified_tx_indexes(self):
        list = []
        for i, tx in enumerate(self.transactions):
            if tx.category == "Non identifiee":
                list.append(i)
        return list

    def sort_transactions(self):
        self.transactions.sort(key=lambda x:x.date)

    def get_dict_transactions(self):
        dict_transactions = []
        for tx in self.transactions:
            dict_transactions.append(tx.to_dict())
        return dict_transactions

    @property
    def categorize_per_month(self):
        categorized_tx = defaultdict(list)
        for tx in self.transactions:
            month = tx.year_month
            categorized_tx[month].append(tx)
        return categorized_tx

    
    def to_data_frame(self):
        return pd.DataFrame([tx.to_dict() for tx in self.transactions])
    
    def categorize_per_month_as_data_frames(self):
        new_dict = {}
        for month in self.categorize_per_month:
            new_dict[month] = pd.DataFrame([tx.to_dict() for tx in self.categorize_per_month[month]])
        
        return new_dict
    
    @property
    def get_unidentified_category_list(self):
        # return a list of transactions with "non identifiee" category
        return [tx for tx in self.transactions if tx.category == "Non identifiee"]


    def category_assign_unidentifed(self, categories_instance, keywords): 
        # category list is from CategoryManager().categories_keys()
        # user is asked to assign a categorie for transactions with "Non identifiee" category
        category_list = self.categories_instance.categories_keys
        already_identified = {}
        unidentified_tx_count = len(self.get_unidentified_category_list)


        len_tx = len(self.transactions)
        i = 0

        while i < len_tx:
            tx = self.transactions[i]
            narrative = tx.narrative
            raw_tx_narratine = self.raw_data_list[i].narrative

            if tx.category != "Non identifiee":
                i += 1
                continue
            
            if narrative in already_identified:
                tx.assign_category(already_identified[narrative])
                i += 1
                continue
            
            else:
                choice = TransactionsInterface.get_cat_to_assign(category_list, narrative, unidentified_tx_count)

                if choice == None:
                    return
                elif choice == "s":
                    self.categories_instance.save_changes(url_categories_json, self.categories_instance.categories_dict)
                    continue
                else:
                    category_choice = category_list[choice]
                    tx.assign_category(category_choice)
                    already_identified[narrative] = category_choice
                    self.categories_instance.categories_kws[category_choice].add_keywords(raw_tx_narratine)
                    i += 1
                
                    time.sleep(2)
                    continue
        
            self.categories_instance.save_changes(url_categories_json, self.categories_instance.categories_dict)


    def user_narrative_modification(self):
        month_list = [x for x in self.categorize_per_month]
        while True:
            tx, new_narrative = TransactionsInterface.ui_modify_tx_narrative(self.categorize_per_month, month_list)
            if not tx or not new_narrative:
                break

            else:
                tx.narrative = new_narrative



        
