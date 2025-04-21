from files_import import FileImport
from CONSTANTS_url import url_csv_5_months


#------------CSV FILE IMPORTATION TO LIBRARIES LIST ----------------

csv_import = FileImport().init_import()
raw_data = csv_import.run_import()







