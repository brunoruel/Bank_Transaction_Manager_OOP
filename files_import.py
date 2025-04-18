import os

import csv
import json

TX_RAW_HEADER = ['Bank Account', 'Date', 'Narrative', 'Debit Amount', 'Credit Amount', 'Balance', 'Categories', 'Serial']

class FileImport:
# class for importation of json and cvs files
# checking correct file type
    def __init__(self, url="",format = "csv"):
        self.url = url
        self.data = []
        self.format = format
        self.accepted_format = ["json", "csv"]

    def file_test(self):
        if not os.path.isfile(self.url):
            print("\u274C The file does not exist!")
            return False
        elif not self.format in self.accepted_format or not self.url.lower().endswith(f".{self.format}"):
            print(f"\u274C Please upload a file in a {self.format} format!")
            self.url = ""
            return False
        else:
            return True

    def import_file(self):
        try:
            with open(self.url, mode="r", encoding="UTF-8", newline="") as file:
                if self.format == "csv":
                    self.data = list(csv.DictReader(file))
                elif self.format == "json":
                    self.data = json.load(file)
                return self.data
        except PermissionError:
            print("\U0001F4DB - Error: Access to the file not permited")
        except FileNotFoundError:
            print("\U0001F6A8 - Error: The file was not found")
        except Exception as e:
            print(f"\U0001F6A8 - Error Unknown: {e}")
        return []
    
    def is_valid_csv_structure(self):
            return all(all(keys in tx.keys() for keys in TX_RAW_HEADER) for tx in self.data)

    @staticmethod
    def request_file_from_user():
        return input("📎 Drag and drop your transactions file: ").strip("'")

    def run_import(self, max_attempt = 3) -> list[dict[str, any]]:
        attempt = 0
        while not self.data and attempt < max_attempt:
            if not self.url:
                self.url = self.request_file_from_user()

            if not self.file_test():
                attempt += 1
                self.url = ""
                continue

            self.import_file()

            if self.format == "csv" and not self.is_valid_csv_structure():
                print("\U0001F4DB - The cvs file do not have the correct informations!")
                attempt += 1
                self.url = ""
                continue

            if self.data:
                print(f"\u2705 - {self.format} file uploaded successfully")
                return self.data
            
            attempt += 1
        print("\U0001F4DB - You have reached the maximum attempt, plese retry later!")

