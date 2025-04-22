from files_import import FileImport
from CONSTANTS_url import url_csv_5_months
from objects_transactions import Transactions_list

#------------CSV FILE IMPORTATION TO LIBRARIES LIST ----------------

csv_import = FileImport().init_import()
raw_data = csv_import.run_import()


test = Transactions_list(raw_data)
print(test.get_dict_transactions())




