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
        self.__unsavedChanges: bool = False

    def Prompt(self):
        print(MAINMENU)
        if self.__unsavedChanges:
            print(f"Budget: {self.__activeBudget} {RED}(unsaved){RESET}")
        else:
            print(f"Budget: {self.__activeBudget}")
        return int(input(">>> "))
    
    def run(self):
        clear()
        menuSelect = self.Prompt()

        while(True):
            if (menuSelect == 1):
                self.StartNew()         # RUN SUB-APP
                menuSelect = self.Prompt()
            elif (menuSelect == 2):
                self.LoadSaved()        # RUN SUB-APP
                menuSelect = self.Prompt()
            elif (menuSelect == 3):
                self.EditBudget()       # RUN SUB-APP
                menuSelect = self.Prompt()
            elif (menuSelect == 4):
                self.DisplayCFInfo()    # RUN SUB-APP
                menuSelect = self.Prompt()
            elif (menuSelect == 5):
                self.SaveBudget()       # RUN SUB-APP
                menuSelect = self.Prompt()
            elif (menuSelect == 6):
                if not self.__unsavedChanges:
                    break
                if input("Are you sure you want to quit? (Y/N)\n>>> ") == "Y":
                    break
                clear()
                menuSelect = self.Prompt()
            else:
                clear()
                menuSelect = self.Prompt()
        
        clear()
        return

    # ** AVAILABLE SUB-APPLICATIONS **

    def StartNew(self):
        clear()

        # if active budget contains data and is unsaved
        if len(self.__cashFlows) > 0 and self.__unsavedChanges:
            print("! WARNING ! This action will overwrite the active budget.")
            if (input("Are you sure you want to continue? (Y/N)\n>>> ") != "Y"):
                print("Failed to create new budget.")
                input("Press enter to return to main menu.")
                clear()
                return
            
        clear()
        
        # get name for new budget
        newName = input("Enter budget name.\n>>> ")
        while (newName == self.__activeBudget):
            print("This budget is already active!")
            newName = input("Enter budget name.\n>>> ")
        
        # start new and add cash flows
        self.__cashFlows = []
        addFlows(self.__cashFlows)
        
        # if cash flows were added
        if len(self.__cashFlows) > 0:
            self.__unsavedChanges = True
    
        clear()
        return

    def AddToBudget(self):
        oldLength = len(self.__cashFlows)

        # add flows until user is finished editing
        addFlows(self.__cashFlows)
        
        # if new data is present
        if len(self.__cashFlows) > oldLength:
            self.__unsavedChanges = True

    def RemoveFromBudget(self):
        oldLength = len(self.__cashFlows)

        # remove flows until user is finished editing
        removeFlows(self.__cashFlows)
        
        # if data has been removed
        if len(self.__cashFlows) < oldLength:
            self.__unsavedChanges = True
    
    def EditBudget(self):
        clear()
        
        # if current budget is empty
        if len(self.__cashFlows) == 0:
            print("You must first create or load a budget!")
            input("Press enter to return to the main menu.")
            return
        
        listFlows(self.__cashFlows)
        addOrDelete = input("Would you like to add or delete cash flows? (A/D)\n>>> ")
        while (addOrDelete not in ["A", "D", "a", "d"]):
            print("Invalid input. Try again.")
            addOrDelete = input("Would you like to add or delete cash flows? (A/D)\n>>> ")

        clear()
        
        if (addOrDelete in ["A", "a"]):
            self.AddToBudget()
        else:
            self.RemoveFromBudget()

        clear()
        return

    def LoadSaved(self):
        clear()

        # if active budget contains data and is unsaved
        if len(self.__cashFlows) > 0 and self.__unsavedChanges:
            print("! WARNING ! This action will overwrite the active budget.")
            if (input("Are you sure you want to continue? (Y/N)\n>>> ") != "Y"):
                print("Failed to load budget.")
                input("Press enter to return to main menu.")
                clear()
                return
        
        clear()

        # if no files exist in savefiles
        if len(getSavedBudgets()) == 0:
            print("No budgets available to load.")
            input("Press enter to return to main menu.")
            clear()
            return
        
        # list saved files
        print("--- SAVED BUDGETS ---")
        i = 1
        for name in getSavedBudgets():
            print(f"{i}. {name}")
            i += 1

        # get name for budget to load
        budgetName = input("Enter the name of a budget to load.\n>>> ")
        while (budgetName not in getSavedBudgets()):
            budgetName = input("Invalid. Enter the name of a budget to load.\n>>> ")

        # start new and set budget name
        self.__cashFlows = []
        self.__unsavedChanges = False
        self.__activeBudget = budgetName

        # parse relevant XML file and load to active budget
        filename = "savefiles/" + budgetName + ".xml"
        tree = ET.parse(filename)
        saveData = tree.getroot()
        for cashFlow in saveData:
            title = cashFlow[0].text
            type = cashFlow[1].text
            desc = cashFlow[2].text
            freq = cashFlow[3].text
            amount = float(cashFlow[4].text)
            newCF = CashFlow(title=title, type=type, desc=desc, freq=freq, amount=amount)
            self.__cashFlows.append(newCF)

        print("Budget loaded successfully.")
        input("Press enter to return to main menu.")
        clear()
        return

    def DisplayCFInfo(self) -> None:
        clear()

        # if no cash flow data present
        if len(self.__cashFlows) == 0:
            print("No cash flow data to display.")
            input("Press enter to return to main menu.")
            clear()
            return
        
        # print cash flow data
        for cashFlow in self.__cashFlows:
            print(cashFlow)

        monthlyIn, monthlyOut = sumFourWeeks(self.__cashFlows)
        print(f"TOTAL INCOME: {GREEN}${round(monthlyIn,2)}{RESET}\nTOTAL SPENDING: {RED}${round(monthlyOut,2)}{RESET}")
        netIn = monthlyIn - monthlyOut
        if netIn > 0:
            print(f"NET: {GREEN}${round(netIn,2)}{RESET}")
        else:
            print(f"NET: {RED}(${abs(round(netIn,2))}){RESET}")
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
            print(f"Active budget does not contain any data!")
            input("Press enter to return to the main menu.")
            clear()
            return
        if (budgetName in getSavedBudgets()):
            if (input("Are you sure you want to overwrite? (Y/N)\n>>> ") != "Y"):
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

        self.__unsavedChanges = False
        print("Budget saved under", filename)
        input("Press enter to return to the main menu.")
        clear()
        return

if __name__ == "__main__":
    myProgram = uBudget()
    myProgram.run()


    

