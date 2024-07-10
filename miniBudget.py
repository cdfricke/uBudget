# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: miniBudget.py
# Latest Revision: 10-July-2024
# Desc: Main script for miniBudget budgeting program.

## FREQUENCIES ##
DAILY = 1
WEEKLY = 2
BIWEEKLY = 3
MONTHLY = 4
YEARLY = 5
## CASHFLOW TYPES
INCOME = "Income"
EXPENSE = "Expense"

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
            self.type = type

    def giveTitle(self, title: str) -> None:
        if (self.title != ""):
            if (input(f"Are you sure you want to overwrite {self.type} title? Y/N\n>>> ") == "Y"):
                self.title = title
            else:
                print(f"{self.type} title was not changed.")
        else:
            self.title = title

    def giveDesc(self, desc: str) -> None:
        if (self.desc != ""):
            if (input(f"Are you sure you want to overwrite {self.type} description? Y/N\n>>> ") == "Y"):
                self.desc = desc
            else:
                print(f"{self.type} description was not changed.")
        else:
            self.desc = desc

    def giveFreq(self, freq: str) -> None:
        if (self.desc != ""):
            if (input(f"Are you sure you want to overwrite {self.type} frequency? Y/N\n>>> ") == "Y"):
                self.freq = freq
            else:
                print(f"{self.type} frequency was not changed.")
        else:
            self.freq = freq

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
        self.type = type
        self.title = title
        self.desc = desc
        self.freq = freq
        self.amount = amount

    def print(self) -> None:
        print(f"({self.type}) {self.title} occurring {self.freq} -> ${self.amount}")

    def xmlType(self) -> str:
        return f"\t<type>{self.type}</type>\n"
    def xmlTitle(self) -> str:
        return f"\t<title>{self.title}</title>\n"
    def xmlDesc(self) -> str:
        return f"\t<desc>{self.desc}</desc>\n"
    def xmlFreq(self) -> str:
        return f"\t<freq>{self.freq}</freq>\n"
    def xmlAmount(self) -> str:
        return f"\t<amount>{self.amount}</amount>\n"
    def toXML(self) -> str:
        """
        Really ugly way of getting an XML-formatted string for a single CashFlow object.
        """
        return f"<CashFlow>\n" + self.xmlType() + self.xmlTitle() + self.xmlDesc() + self.xmlFreq() + self.xmlAmount() + "</CashFlow>"

if __name__ == "__main__":
    allCashFlows = []
    while(input("Add cash flow? Y/N\n>>> ") != "N"):
        data = []
        data.append(input("Income or Expense?\n>>> "))
        data.append(input("Title:\n>>> "))
        data.append(input("Description:\n>>> "))
        data.append(input("Frequency: (Daily, Weekly, Biweekly, Monthly, Yearly)\n>>> "))
        data.append(float(input("Amount:\n>>> ")))
        newCF = CashFlow()
        newCF.loadValues(type=data[0], title=data[1], desc=data[2], freq=data[3], amount=data[4])
        allCashFlows.append(newCF)

    for flow in allCashFlows:
        print(flow.toXML())
        