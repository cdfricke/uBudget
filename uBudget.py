# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: uBudget.py
# Latest Revision: 7-Aug-2024
# Description: Main program for uBudget (micro-budget, mu-budget, u-Budget)

from modules.objects import *
from modules.functions import *

class uBudget:
    def __init__(self):
        self.__cashFlows: list[CashFlow] = []
        self.__activeBudget: str = "NO ACTIVE BUDGET"

    def Prompt(self):
        print(MAINMENU)
        print(f"Budget: {self.__activeBudget}")
        return int(input(">>> "))
    
    def run(self):
        clear()
        menuSelect = self.Prompt()

        while(menuSelect != 6):
            if (menuSelect == 1):
                self.StartNew()         # RUN SUB-APP
                clear()
                menuSelect = self.Prompt()
            elif (menuSelect == 2):
                self.LoadSaved()        # RUN SUB-APP
                clear()
                menuSelect = self.Prompt()
            elif (menuSelect == 3):
                self.DisplayCFInfo()    # RUN SUB-APP
                clear()
                menuSelect = self.Prompt()
            elif (menuSelect == 4):
                self.SaveBudget()       # RUN SUB-APP
                clear()
                menuSelect = self.Prompt()
            elif (menuSelect == 5):
                self.ShowSavedBudgets() # RUN SUB-APP
                menuSelect = self.Prompt()

    # ** AVAILABLE SUB-APPLICATIONS **

    def StartNew(self):
        clear() # clear screen FIRST

        print("! WARNING ! This action will erase the active budget.")
        if (input("Are you sure you want to continue? (Y/N)\n>>> ") != "Y"):
            print("Failed to create new budget.")
            input("Press enter to return to main menu.")
            clear()
            return

        addFlows(self.__cashFlows)

        while (input("Return to main menu? (Y/N)\n>>> ") != "Y"):
            addFlows(self.__cashFlows)
        self.__activeBudget = input("Enter budget name.\n>>> ")
        print("Successfully created budget.")
        input("Press enter to return to main menu.")
        clear()
        return

    def LoadSaved(self):
        clear()
        if len(getSavedBudgets()) == 0:
            print("No budgets available to load.")
            input("Press enter to return to main menu.")
            clear()
            return
        
        print("--- SAVED BUDGETS ---")
        i = 1
        for name in getSavedBudgets():
            print(f"{i}. {name}")
            i += 1

        budgetName = input("Enter the name of a budget to load.\n>>> ")
        while (budgetName not in getSavedBudgets()):
            budgetName = input("Invalid. Enter the name of a budget to load.\n>>> ")
        filename = "savefiles/" + budgetName + ".xml"
        tree = ET.parse(filename)
        saveData = tree.getroot()
        for cashFlow in saveData:
            title = cashFlow[0].text
            type = cashFlow[1].text
            desc = cashFlow[2].text
            freq = cashFlow[3].text
            amount = float(cashFlow[4].text)
            newCF = CashFlow()
            newCF.loadValues(title=title, type=type, desc=desc, freq=freq, amount=amount)
            self.__cashFlows.append(newCF)
        self.__activeBudget = budgetName
        print("Budget loaded successfully.")
        input("Press enter to return to main menu.")
        clear()
        return

    def DisplayCFInfo(self) -> None:
        clear()
        if len(self.__cashFlows) == 0:
            print("No cash flow data to display.")
            input("Press enter to return to main menu.")
            clear()
            return
        for cashFlow in self.__cashFlows:
            print(cashFlow)
        input("Press enter to return to main menu.")
        clear()
        return

    def SaveBudget(self) -> None:
        """
        Encode save date and time in file name, then save a list of CashFlow objects
        in XML format to said file. Takes one parameter which should be a list of
        CashFlow type objects.
        """
        clear()
        budgetName = self.__activeBudget
        if len(self.__cashFlows) == 0:
            print("Budget does not contain any data!")
            input("Press enter to return to the main menu.")
            clear()
            return
        if (budgetName in getSavedBudgets()):
            if (input("Do you want to overwrite an existing budget with this name? (Y/N)\n>>> ") != "Y"):
                print("Failed to save budget.")
                input("Press enter to return to the main menu.")
                clear()
                return
        filename = "savefiles/" + budgetName + ".xml"
        root = ET.Element(budgetName)
        for cashFlow in self.__cashFlows:
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
        print("Budget saved under", filename)
        input("Press enter to return to the main menu.")
        clear()
        return

    def ShowSavedBudgets(self) -> None:
        clear()
        print("--- SAVED BUDGETS ---")
        if len(getSavedBudgets()) == 0:
            print("No budgets saved.")
            input("Press enter to return to the main menu.")
            clear()
            return
        i = 1
        for name in getSavedBudgets():
            print(f"{i}. {name}")
            i += 1
        input("Press enter to return to the main menu.")
        clear()
        return

if __name__ == "__main__":
    myProgram = uBudget()
    myProgram.run()


    

