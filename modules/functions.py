# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: functions.py
# Lateste Revision: 7-Aug-2024
# Description: Helper functions for uBudget program

from py.objects import *
import os
import xml.etree.ElementTree as ET

# *** BACKEND ***
def addFlows(data: list):
    """
    Takes a single parameter which should be a list, either empty or already containing
    cashFlow type objects and prompts the user for information necessary to create new cashFlows
    and adds them to the parameter list.
    """
    while(input("Add cash flow? Y/N\n>>> ") == "Y"):
        # get type, check validity
        type = input("Income or Expense?\n>>> ").upper()
        while (not type in cfTypes):
            type = input("Income or Expense?\n>>> ").upper()
        # get title, no need to check validity
        title = input("Title:\n>>> ")
        # get desc, no need to check validity
        desc = input("Description:\n>>> ")
        # get freq, check validity
        freq = input("Frequency: (Daily, Weekly, Biweekly, Monthly, Yearly)\n>>> ").upper()
        while (not freq in cfFreqs):
            freq = input("Frequency: (Daily, Weekly, Biweekly, Monthly, Yearly)\n>>> ").upper()
        # get amount, no need to check validity
        amount = float(input("Amount:\n>>> "))
        # create CashFlow and add to list
        newCF = CashFlow()
        newCF.loadValues(type=type, title=title, desc=desc, freq=freq, amount=amount)
        data.append(newCF)

def sumFourWeeks(data: list[CashFlow]) -> tuple:
    """
    Sums the income and expenses for each CashFlow object in the list passed.
    Totals are calculated on a monthly (4 week, 28 day) basis, with totals extrapolated via the frequency
    and given amount for each CashFlow.
    (e.g. biweekly income is doubled before added to the monthly total).
    Return value is a tuple corresponding to (monthly income, monthly expenses)
    """
    totalIncome = 0.0
    totalExpense = 0.0
    for flow in data:
        match flow.freq:
            case "DAILY":
                if (flow.type == "INCOME"):
                    totalIncome += (28.0 * flow.amount)
                else:
                    totalExpense += (28.0 * flow.amount)
            case "WEEKLY":
                if (flow.type == "INCOME"):
                    totalIncome += (4.0 * flow.amount)
                else:
                    totalExpense += (4.0 * flow.amount)
            case "BIWEEKLY":
                if (flow.type == "INCOME"):
                    totalIncome += (2.0 * flow.amount)
                else:
                    totalExpense += (2.0 * flow.amount)
            case "MONTHLY":
                if (flow.type == "INCOME"):
                    totalIncome += (flow.amount)
                else:
                    totalExpense += (flow.amount)
            case "YEARLY":
                if (flow.type == "INCOME"):
                    totalIncome += (flow.amount / 12.0)
                else:
                    totalExpense += (flow.amount / 12.0)
            case _:
                print("ERROR: 0x1")
            
    return (totalIncome, totalExpense)

# ** IO **

def save(data: list[CashFlow]):
    """
    Encode save date and time in file name, then save a list of CashFlow objects
    in XML format to said file. Takes one parameter which should be a list of
    CashFlow type objects.
    """
    if (input("Do you want to overwrite current save? (Y/N)\n>>> ") == "Y"):
        filename = "savefiles/" + "savedFlows" + ".xml"
        root = ET.Element("saveData")
        for cashFlow in data:
            cashFlowItem = ET.SubElement(root, "CashFlow")
            titleItem = ET.SubElement(cashFlowItem, "title")
            titleItem.text = cashFlow.title
            typeItem = ET.SubElement(cashFlowItem, "type")
            typeItem.text = cashFlow.type
            descItem = ET.SubElement(cashFlowItem, "desc")
            descItem.text = cashFlow.desc
            freqItem = ET.SubElement(cashFlowItem, "freq")
            freqItem.text = cashFlow.freq
            amountItem = ET.SubElement(cashFlowItem, "amount")
            amountItem.text = str(cashFlow.amount)
        tree = ET.ElementTree(root)
        ET.indent(tree, space='\t', level=0)
        tree.write(filename, encoding="UTF-8")


def MainMenu() -> str:
    return  """
            ------------------(\u03BCBUDGET)------------------

            1. Start New Budget Planner
            2. Load Saved Budget
            3. Quit

            ---------------------------------------------
            """
def clear():
    if (os.name == "nt"):  # windows
        os.system("cls")
    else:   # mac / linux
        os.system("clear")



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
    print("Loading Saved Budget...")
    
    tree = ET.parse('savefiles/savedFlows.xml')
    saveData = tree.getroot()
    for cashFlow in saveData:
        for child in cashFlow:
            print(child.tag, child.attrib)
    
    