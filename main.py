
from files_import import FileImport
from CONSTANTS_url import url_csv_5_months
from data_pipeline import DataPipeLine

#------------CSV FILE IMPORTATION TO LIBRARIES LIST ----------------

start = FileImport(url_csv_5_months, "csv")
FileImport.run_import(start)
raw_data_list = start.data


#-------------FORMAT DATA FOR EXCEL EXPORT ------------------------

data_pipeline = DataPipeLine(raw_data_list)
data_pipeline.run_pipeline()
data_ready = data_pipeline.categorized_transactions


