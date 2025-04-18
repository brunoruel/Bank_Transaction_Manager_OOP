import re
from datetime import datetime
from CONSTANTS_main import TO_DELETE_IN_NARRATIVE, CATEGORIES_KEY_WORDS, FLOAT_KEYS, CATEGORIES_AS_NARRATIVE, COLUMNS_TO_KEEP, ACCOUNTS
from copy import deepcopy
from collections import defaultdict

from var_test import raw_tx_test

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

        for words in TO_DELETE_IN_NARRATIVE:
            self.raw_tx["Narrative"] = re.sub(words, "", self.raw_tx["Narrative"], flags=re.IGNORECASE)

        self.raw_tx["Narrative"] = re.sub(r"\s{2,}", " ",self.raw_tx["Narrative"])
        self.raw_tx["Narrative"] = re.sub(r"\d{4,}", "",self.raw_tx["Narrative"])
        self.raw_tx["Narrative"] = self.raw_tx["Narrative"].strip().title()

    def categories_add(self):
        if not CATEGORIES_KEY_WORDS:
            return
        for key, value in CATEGORIES_KEY_WORDS.items():
            for key_word in value:
                if key_word.lower() in self.raw_tx["Narrative"].lower():
                    self.raw_tx["Narrative"] = key if key in CATEGORIES_AS_NARRATIVE else key_word
                    self.raw_tx["Categorie"] = key
                    return self.raw_tx
        self.raw_tx["Categorie"] = "Non identifiee"

    def convert_str_to_float(self):
        for key in FLOAT_KEYS:
            value = self.raw_tx.get(key, "")
            try:
                self.raw_tx[key] = float(value) if value else 0.0
            except ValueError:
                return False
        return True
    
    def __repr__(self):
        return self.raw_tx

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
        self.formated_tx = []

    def add_amount_column(self):
        self.tx["Amount"] = float(self.tx["Credit Amount"] - self.tx["Debit Amount"])

    def account_column(self):
        for key, value in ACCOUNTS.items():
            if self.tx["Bank Account"] == value:
                self.tx["Account"] = key
                return self.tx["Account"]
        self.tx["Account"] = "Compte non identifie"

    def columns_filter(self):
        self.formated_tx = {x:self.tx[x] for x in COLUMNS_TO_KEEP}
    
    def add_year_month_column(self):
        self.tx["Year"] = str(self.tx["Date"].year)
        self.tx["Month"] = str(self.tx["Date"].month)

    def run_transaction_formater(self) -> dict:
        self.account_column()
        self.add_amount_column()
        self.add_year_month_column()
        self.columns_filter()
        return self.formated_tx


class DataPipeLine:
    processed_transactions = 0
    month_year_keys = []

    def __init__(self, data):

        if not isinstance(data, list):
            raise TypeError("raw_tx must be a list")
        
        self.data = deepcopy(data)
        self.categorized_transactions = defaultdict(list)

    @staticmethod
    def sort_transactions(tx_list):
        tx_list.sort(key=lambda x:x["Date"])

    def categorize_tx(self, tx):
        tx_month_year = tx["Date"].strftime('%B %Y')
        self.categorized_transactions[tx_month_year].append(tx)
        DataPipeLine.month_year_keys.append(tx_month_year) if tx_month_year not in DataPipeLine.month_year_keys else None

    def run_pipeline(self):
        DataPipeLine.sort_transactions(self.data)

        for i in range(len(self.data)):
            tx_cleaning = DataCleaner(self.data[i])
            DataCleaner.run_data_cleaning(tx_cleaning)
            cleaned_tx = tx_cleaning.raw_tx

            if not cleaned_tx:
                continue

            tx_formatage = TransactionFormater(cleaned_tx)
            TransactionFormater.run_transaction_formater(tx_formatage)
            formated_transaction = tx_formatage.formated_tx

            self.data[i] = formated_transaction
            DataPipeLine.processed_transactions += 1

        for tx in self.data:
            self.categorize_tx(tx)

        print(f"\u2705 - {DataPipeLine.processed_transactions} transactions successfully modified")

        return self.categorized_transactions
    






