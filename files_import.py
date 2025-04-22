import os
from abc import ABC, abstractmethod
from colorama import init, Fore, Style
init(autoreset=True)

import csv
import json

from CONSTANTS_main import ConstantsTx



class BaseFileImporter(ABC):
    def __init__(self, url:str):
        self.url = url
        self.data = []


    @abstractmethod
    def import_file(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    def file_exists(self):
        return os.path.isfile(self.url)
    
    def run_import(self):
        if not self.file_exists:
            print(f"{Fore.RED}❌ The path file is incorrect or file inexistent")
            return []
        
        self.import_file()

        if not self.validate():
            print(f"{Fore.RED}❌ The file imported is not valid")
            return[]
        
        print(f"{Fore.GREEN}✅ File Imported Successfully")
        return self.data


class CSVImporter(BaseFileImporter):
    def import_file(self):
        with open(self.url, newline="", encoding="utf-8", mode ="r") as csv_file:
            self.data = list(csv.DictReader(csv_file))
            return self.data
        
    def validate(self):
        return all(all(k in tx for k in ConstantsTx.TX_RAW_HEADER) for tx in self.data)


class JSONImporter(BaseFileImporter):
    def import_file(self):
        with open(self.url, encoding="utf-8", mode="r", newline="") as json_file:
            self.data =  json.load(json_file)
        
    def validate(self):
        return True if self.data else False
    

class FileImport:
    def __init__(self, url:str="", type:str="csv"):
        self.url = url
        self.type = type

    @staticmethod
    def request_file_path_from_user():
        print("=" * 50)
        print()
        return input("💾 Drag and drop your file: ").strip("'")

    def init_import(self):
        while True:
            if not self.url:
                self.url = FileImport.request_file_path_from_user()
            if self.url.endswith("json") and self.type == "json":
                return JSONImporter(self.url)
            if self.url.endswith("csv") and self.type == "csv":
                return CSVImporter(self.url)
            else:
                print(f"{Fore.RED}❌ Not a valid file type")
                self.url = ""
        


class FileSaving:
    @staticmethod
    def json_saving(file_path, data):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        






        
