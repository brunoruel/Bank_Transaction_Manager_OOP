from files_import import FileImport
from CONSTANTS_url import url_json

TX_RAW_HEADER = ['Bank Account', 'Date', 'Narrative', 'Debit Amount', 'Credit Amount', 'Balance', 'Categories', 'Serial']

TO_DELETE_IN_NARRATIVE = [
    "DEBIT CARD PURCHASE ",
    "PAYMENT BY AUTHORITY TO ",
    "Withdrawal Mobile "
]

CATEGORIES_KEY_WORDS = FileImport(url_json, "json").run_import()

FLOAT_KEYS = ["Debit Amount", "Credit Amount", "Balance"]

CATEGORIES_AS_NARRATIVE = ["Loyer", "Creche", "Interets banquaire", "Virement intra compte"]

COLUMNS_TO_KEEP = [
    "Account",
    "Date",
    "Narrative",
    "Categorie",
    'Amount',
    "Balance",
    "Month",
    "Year"
]

ACCOUNTS = {"Saving Account": "032066031826","Cheque Account": "732051678691"}