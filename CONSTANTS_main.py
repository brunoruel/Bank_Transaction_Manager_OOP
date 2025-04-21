

class ConstantsTx:
    
    TX_RAW_HEADER = ['Bank Account', 'Date', 'Narrative', 'Debit Amount', 'Credit Amount', 'Balance', 'Categories', 'Serial']

    TO_DELETE_IN_NARRATIVE = [
        "DEBIT CARD PURCHASE ",
        "PAYMENT BY AUTHORITY TO ",
        "Withdrawal Mobile ",
        "Eftpos Debit",
        "Withdrawal Online"
    ]

    FLOAT_KEYS = ["Debit Amount", "Credit Amount", "Balance"]

    CATEGORIES_AS_NARRATIVE = ["Loyer", "Creche", "Interets banquaire", "Virement intra compte"]

    CATEGORIES_CHOICES = {"1": "Divers",  "2": "Sorties", "3": "Courses", "4": "Vacances", "5": "Plongee", "6": "Abonnements", "7": "Factures", "8": "Transport", "9": "Sante"}


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