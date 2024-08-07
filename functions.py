# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: functions.py
# Lateste Revision: 7-Aug-2024
# Description: Helper functions for uBudget program

from objects import *
from os import system, name

# *** BACKEND ***
def addFlows(data: list):
    """
    Takes a single parameter which should be a list, either empty or already containing
    cashFlow type objects and prompts the user for information necessary to create new cashFlows
    and adds them to the parameter list.
    """
    while(input("Add cash flow? Y/N\n>>> ") == "Y"):
        # get type, check validity
        type = input("Income or Expense?\n>>> ")
        while (not type in cfTypes):
            type = input("Income or Expense?\n>>> ")
        # get title, no need to check validity
        title = input("Title:\n>>> ")
        # get desc, no need to check validity
        desc = input("Description:\n>>> ")
        # get freq, check validity
        freq = input("Frequency: (Daily, Weekly, Biweekly, Monthly, Yearly)\n>>> ")
        while (not freq in cfFreqs):
            freq = input("Frequency: (Daily, Weekly, Biweekly, Monthly, Yearly)\n>>> ")
        # get amount, no need to check validity
        amount = float(input("Amount:\n>>> "))
        # create CashFlow and add to list
        newCF = CashFlow()
        newCF.loadValues(type=type, title=title, desc=desc, freq=freq, amount=amount)
        data.append(newCF)

def sumMonthlyValues(data: list) -> tuple:
    """
    Sums the income and expenses for each CashFlow object in the list passed.
    Totals are calculated on a monthly basis, with totals extrapolated via the frequency
    and given amount for each CashFlow.
    (e.g. biweekly income is doubled before added to the monthly total).
    Return value is a tuple corresponding to (monthly income, monthly expenses)
    """
    totalIncome = 0.0
    totalExpense = 0.0
    for flow in data:
        if (flow.freq == "Yearly"):
            if (flow.type == "Income"):
                totalIncome += (flow.amount / 12.0)
            else:
                totalExpense += (flow.amount / 12.0)
        elif (flow.freq == "Monthly"):
            if (flow.type == "Income"):
                totalIncome += (flow.amount)
            else:
                totalExpense += (flow.amount)
        elif (flow.freq == "Biweekly"):
            if (flow.type == "Income"):
                totalIncome += (2.0 * flow.amount)
            else:
                totalExpense += (2.0 * flow.amount)
        elif (flow.freq == "Weekly"):
            if (flow.type == "Income"):
                totalIncome += (4.0 * flow.amount)
            else:
                totalExpense += (4.0 * flow.amount)
        else:   # daily
            if (flow.type == "Income"):
                totalIncome += (4.0 * flow.amount)
            else:
                totalExpense += (4.0 * flow.amount)
    return (totalIncome, totalExpense)

# ** IO **
def xmlType(obj: CashFlow) -> str:
    return f"\t\t<type>{obj.type}</type>\n"
def xmlTitle(obj: CashFlow) -> str:
    return f"\t\t<title>{obj.title}</title>\n"
def xmlDesc(obj: CashFlow) -> str:
    return f"\t\t<desc>{obj.desc}</desc>\n"
def xmlFreq(obj: CashFlow) -> str:
    return f"\t\t<freq>{obj.freq}</freq>\n"
def xmlAmount(obj: CashFlow) -> str:
    return f"\t\t<amount>{obj.amount}</amount>\n"
def toXML(obj: CashFlow) -> str:
    """
    Really ugly way of getting an XML-formatted string for a single CashFlow object.
    """
    return "\t<CashFlow>\n" + xmlType(obj) + xmlTitle(obj) + xmlDesc(obj) + xmlFreq(obj) + xmlAmount(obj) + "\t</CashFlow>\n"

def save(data: list):
    """
    Encode save date and time in file name, then save a list of CashFlow objects
    in XML format to said file. Takes one parameter which should be a list of
    CashFlow type objects.
    """
    if (input("Do you want to overwrite current save? (Y/N)\n>>> ") == "Y"):
        filename = "savefiles/" + "savedFlows" + ".xml"
        saveFile = open(file=filename, mode="w")
        saveFile.write("<?xml version=\"1.0\" encoding=\"utf-8\">\n")
        saveFile.write("<saveData>\n")
        for flow in data:
            saveFile.write(toXML(flow))
        saveFile.write("</saveData>\n")

def MainMenu() -> str:
    return  """
            ------------------(\u03BCBUDGET)------------------

            1. Start New Budget Planner
            2. Load Saved Budget
            3. Quit

            ---------------------------------------------
            """
def clear():
    if (name == "nt"):  # windows
        system("cls")
    else:   # mac / linux
        system("clear")



# ** MAIN MENU FUNCTIONS **
def StartNew():
    clear() # clear screen FIRST

    allCashFlows = []
    addFlows(allCashFlows)

    while (input("Return to main menu? (Y/N)\n>>> ") != "Y"):
        addFlows(allCashFlows)
    save(allCashFlows)
    clear()


def LoadSaved():
    print("Loading Saved Budget... (UNIMPLEMENTED)")
    
    