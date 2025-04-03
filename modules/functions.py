# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: functions.py
# Lateste Revision: 1-April-2025
# Description: Helper functions for uBudget program

from modules.objects import *
import os
import xml.etree.ElementTree as ET

# *** BACKEND ***
def listFlows(data: list[CashFlow]):
    print("--- CASH FLOWS ---")
    i = 1
    for cashFlow in data:
        color = GREEN if (cashFlow.type == "INCOME") else RED
        print(f"{i}. {cashFlow.title} {color}({cashFlow.type}){RESET}")
        i += 1

def addFlows(data: list[CashFlow]):
    """
    Takes a single parameter which should be a list, either empty or already containing
    cashFlow type objects and prompts the user for information necessary to create new cashFlows
    and adds them to the parameter list.
    """
    clear()
    listFlows(data)
    while(input("Add cash flow? (Y/N)\n>>> ") == "Y"):
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
        newCF = CashFlow(type=type, title=title, desc=desc, freq=freq, amount=amount)
        data.append(newCF)
        clear()
        listFlows(data)

def removeFlows(data: list[CashFlow]):
    """
    Takes a single parameter which should be a list, either empty or already containing
    cashFlow type objects and prompts the user for information necessary to remove cashFlows
    from the parameter list.
    """
    clear()
    listFlows(data)
    while (input("Delete cash flow? (Y/N)\n>>> ") == "Y" and len(data) > 0):
        deleteThis = int(input("Enter the number of a cash flow to delete.\n>>> "))
        del data[deleteThis - 1]
        clear()
        listFlows(data)
    return


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

def clear():
    if (os.name == "nt"):  # windows
        os.system("cls")
    else:   # mac / linux
        os.system("clear")

def getSavedBudgets() -> list[str]:
    budgets = []
    path = "savefiles/"
    files = os.listdir(path)
    for file in files:
        budgets.append(file[:-4])
    return budgets