# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: objects.py
# Latest Revision: 1-April-2025
# Desc: Necessary global objects and classes for uBudget program

MAINMENU =  """
            ------------------(\u03BCBUDGET)------------------

            1. Create
            2. Load
            3. Edit
            4. Show Details
            5. Save
            6. Quit

            ---------------------------------------------
            """
    
# *** ACCEPTABLE VALUES FOR CASHFLOW TYPE AND FREQUENCY ***
cfTypes = ["INCOME", "EXPENSE"]
cfFreqs = ["DAILY", "WEEKLY", "BIWEEKLY", "MONTHLY", "YEARLY"]

# ** ANSI escape sequences (FOR COLOR OUTPUT)
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[0m' # Reset to default color

# *** MAIN OBJECT OF PROGRAM FOR DESCRIBING CASH FLOW ***
class CashFlow:
    """
    CashFlow object. Either Income type or expense type. Includes a title, description, frequency, and amount.
    """
    def __init__(self) -> None:
        self.type = ""
        self.title = ""
        self.desc = ""
        self.frequency = ""
        self.amount = 0.00

    def __init__(self, type: str, title: str, desc: str, freq: str, amount: float) -> None:
        """
        Assigns all class data members without checking for overwrites.
        """
        self.type = type.upper()
        self.title = title
        self.desc = desc
        self.freq = freq.upper()
        self.amount = amount

    def __str__(self) -> str:
        COLOR = GREEN if self.type == "INCOME" else RED
        return f"{COLOR}({self.type}){RESET} {self.title} occurring {self.freq} -> {COLOR}${self.amount}{RESET}"

    def giveType(self, type: str) -> None:
        if (self.type != ""):
            if (input("Are you sure you want to overwrite cashflow type? Y/N\n>>> ") == "Y"):
                self.type = type
            else:
                print("Cashflow type was not changed.")
        else:
            self.type = type.upper()

    def giveTitle(self, title: str) -> None:
        if (self.title != ""):
            if (input(f"Are you sure you want to overwrite {self.type} title? Y/N\n>>> ") == "Y"):
                self.title = title
            else:
                print(f"{self.type} title was not changed.")
        else:
            self.title = title.upper()

    def giveDesc(self, desc: str) -> None:
        if (self.desc != ""):
            if (input(f"Are you sure you want to overwrite {self.type} description? Y/N\n>>> ") == "Y"):
                self.desc = desc
            else:
                print(f"{self.type} description was not changed.")
        else:
            self.desc = desc.upper()

    def giveFreq(self, freq: str) -> None:
        if (self.desc != ""):
            if (input(f"Are you sure you want to overwrite {self.type} frequency? Y/N\n>>> ") == "Y"):
                self.freq = freq
            else:
                print(f"{self.type} frequency was not changed.")
        else:
            self.freq = freq.upper()

    def giveAmount(self, amount: float) -> None:
        if (self.cost != 0.00):
            if (input(f"Are you sure you want to overwrite {self.type} amount? Y/N\n>>> ") == "Y"):
                self.amount = amount
            else:
                print(f"{self.type} amount was not changed.")
        else:
            self.amount = amount
        