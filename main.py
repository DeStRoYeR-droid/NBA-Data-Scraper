import requests
from pprint import PrettyPrinter
from tabulate import tabulate
import datetime

BASE_URL = "https://data.nba.net/"
PRINTER = PrettyPrinter()

def getCoachInfo(year):
    extension = f"/data/10s/prod/v1/{year}/coaches.json"
    data = requests.get(BASE_URL + extension).json()
    
    values = []
    for value in data["league"]["standard"]:
        coachInfo = []
        coachInfo.append(f"{value['firstName']} {value['lastName']}")
        coachInfo.append(value['isAssistant'])
        coachInfo.append(value['teamSitesOnly']['teamCode'].title())
        values.append(coachInfo)
        
    print (tabulate(values , headers = ["Name" , "IsAssistant" , "Team"]))
    
def main():
    run = True
    while (run):
        print ("Welcome to the NBA Menu")
        print ("1. Show data of coaches ")
        print ("2. Exit the menu")        
        choice = int(input("Please enter your choice "))
        
        if (choice == 1):
            year = int(input("Please enter the year "))
            if (year < 2019 or year > datetime.datetime.now().year):
                print ("Data not available")
            else:
                getCoachInfo(year)
        elif (choice == 2):
            run = False
            
        print ()         
        
    
if __name__ == '__main__':
    main()