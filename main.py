
from files_import import FileImport
from CONSTANTS_url import url_csv_5_months
from data_pipeline import DataPipeLine

#------------CSV FILE IMPORTATION TO LIBRARIES LIST ----------------

start = FileImport(url_csv_5_months, "csv")
raw_data_list = start.run_import()

#-------------FORMAT DATA FOR EXCEL EXPORT ------------------------

data_pipeline = DataPipeLine(raw_data_list)
data_ready = data_pipeline.run_pipeline()




