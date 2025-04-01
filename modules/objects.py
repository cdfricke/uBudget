# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: miniBudget.py
# Latest Revision: 10-July-2024
# Desc: Main script for uBudget budgeting program.

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

    def loadValues(self, type: str, title: str, desc: str, freq: str, amount: float):
        """
        Assigns all class data members without checking for overwrites.
        """
        self.type = type.upper()
        self.title = title
        self.desc = desc
        self.freq = freq.upper()
        self.amount = amount

    def print(self) -> None:
        print(f"({self.type}) {self.title} occurring {self.freq} -> ${self.amount}")

    
# *** ACCEPTABLE VALUES FOR CASHFLOW TYPE AND FREQUENCY ***
cfTypes = ["INCOME", "EXPENSE"]
cfFreqs = ["DAILY", "WEEKLY", "BIWEEKLY", "MONTHLY", "YEARLY"]
        