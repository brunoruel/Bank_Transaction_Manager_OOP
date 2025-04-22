from copy import copy, deepcopy
import re
from datetime import datetime
from collections import defaultdict
import pandas as pd

from objects_categories_keywords import CategoriesManager
from CONSTANTS_main import ConstantsTx
from files_import import FileImport

# Test import:
from CONSTANTS_url import url_json, url_csv_5_months
from var_test import raw_tx_test
import_json = FileImport(url_json, "json").init_import()
CATEGORIES_KEY_WORDS = import_json.run_import()
raw_data_test_importer = FileImport(url_csv_5_months, "csv").init_import().run_import()

test = CategoriesManager(CATEGORIES_KEY_WORDS).categories_keys


class Transaction:
    def __init__(self, raw_data:dict):
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

    def categories_add(self):
        self.category = CategoriesManager(CATEGORIES_KEY_WORDS).categorie_match(self.narrative)

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
        print(f"{category_choice} successfully assigned to {self.narrative}")

    
    def run(self) -> dict:
        self.convert_date_to_datetime()
        self.compute_amount()
        self.categories_add()
        self.clean_narrative()
        self.account_column()
        self.add_year_month_column()
        return self
    

class Transactions_list:
    def __init__(self, raw_data_list):
        self.raw_data_list = [Transaction(raw) for raw in raw_data_list]
        self.transactions = [Transaction(cleaned_tx).run() for cleaned_tx in raw_data_list]
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

    def categorize_per_month(self):
        categorized_tx = defaultdict(list)
        for tx in self.transactions:
            month = tx.year_month
            categorized_tx[month].append(tx.to_dict())

        return categorized_tx
    
    def to_data_frame(self):
        return pd.DataFrame([tx.to_dict() for tx in self.transactions])
    
    def get_unidentified_category_list(self):
        # return a list of transactions with "non identifiee" category
        return [tx for tx in self.transactions if tx.category == "Non identifiee"]

# ================  TO FINISH ==========        TOP     ===================

    def category_assign_unidentifed(self, category_list): # category list is from CategoryManager().categories_keys()
        # user is asked to assign a categorie for transactions with "Non identifiee" category
        unidentified_tx = self.get_unidentified_category_list()
        print("Choose a categorie to assign to the transactions")
        for i, value in enumerate(category_list):
            print(f"{i + 1} - {value}")
        for tx in unidentified_tx:
            print(f"{tx.narrative}")
            choice = input("Your choice: ")
            choice = int(choice) - 1
            category_choice = category_list[choice]
            tx.assign_category(category_choice)

# ================  TO FINISH ==========        BOTTOM     ===================




