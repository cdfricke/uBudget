# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: uBudget.py
# Latest Revision: 7-Aug-2024
# Description: Main program for uBudget (micro-budget, mu-budget, u-Budget)

from objects import *
from functions import *

clear()
print(MainMenu())
menuSelect = int(input(">>> "))

while(menuSelect != 3):
    if (menuSelect == 1):
        StartNew() 
        print(MainMenu())
        menuSelect = int(input(">>> "))
    elif (menuSelect == 2):
        LoadSaved()
        print(MainMenu())
        menuSelect = int(input(">>> "))

    

