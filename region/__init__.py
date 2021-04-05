import requests
import os
import json
from region.setting import *
from region.countries import allContries
from region.states import allStatesByCountry
from region.cities import allCitiesByState

def main():
    print("\nEnter 1: Get all countries name:")
    print("Enter 2: Get all states name by country:")
    print("Enter 3: Get all cities name by state: \n")
    
    i = input("Enter choies no: ")
    if i == "1":
        print(allContries())
    elif i == "2":
        print(allStatesByCountry())
    elif i == "3":
        print(allCitiesByState())
    else:
        print("Enter valid input")

if __name__ == "__main__":
    main()
    