import requests
from pprint import PrettyPrinter
from tabulate import tabulate
import datetime

BASE_URL = "https://data.nba.net/"
PRINTER = PrettyPrinter()

def get_coach_info(year : int):
    extension = f"/data/10s/prod/v1/{year}/coaches.json"
    data = requests.get(BASE_URL + extension).json()["league"]["standard"]
    
    values = []
    for value in data:
        coachInfo = []
        coachInfo.append(f"{value['firstName']} {value['lastName']}")
        coachInfo.append(value['isAssistant'])
        coachInfo.append(value['teamSitesOnly']['teamCode'].title())
        values.append(coachInfo)
        
    print (tabulate(values , headers = ["Name" , "IsAssistant" , "Team"]))

def get_team_info():
    data = requests.get(BASE_URL + "/prod/v2/2022/teams.json").json()["league"]["standard"]
    
    values = []
    for value in data:
        if (not(value['isNBAFranchise'])):
            continue
        
        teamInfo = []
        teamInfo.append(value['fullName'])
        teamInfo.append(value['confName'])
        teamInfo.append(value['city'])
        teamInfo.append(value['tricode'])
        values.append(teamInfo)
        
    print (tabulate(values , headers = ["Name" , "Conference" , "City", "TriCode"]))
  
def get_team_stats(year : int):
    extension = "/data/10s/prod/v1/2021/team_stats_rankings.json"
    data = requests.get(BASE_URL + extension).json()["league"]["standard"]["regularSeason"]["teams"]
    
    values = []
    
    for value in data:
        teamInfo = []
        teamInfo.append(f"{value['name']} {value['nickname']}")
        teamInfo.append(value['ppg']['avg'])
        teamInfo.append(eval(f"{value['drpg']['avg']} + {value['orpg']['avg']}"))
        teamInfo.append(value['apg']['avg'])
        teamInfo.append(value['spg']['avg'])
        teamInfo.append(value['bpg']['avg'])
        
        values.append(teamInfo)
        
    print (tabulate(values, headers = ["Team Name" , "PPG (Avg)" , "RPG (Avg)" , "APG (Avg)" , "SPG (Avg)" , "BPG (Avg)"]))
    

def main():
    run = True
    while (run):
        print ("Welcome to the NBA Menu")
        print ("1. Show data of coaches ")
        print ("2. Get team information ")
        print ("3. Get team stats ")
        print ("69. Exit the menu")        
        choice = int(input("Please enter your choice "))
        
        if (choice == 1):
            year = int(input("Please enter the year "))
            if (year < 2019 or year > datetime.datetime.now().year):
                print ("Data not available")
            else:
                get_coach_info(year)
                
        elif (choice == 2):
            get_team_info()
            
        elif (choice == 3):
            year = int(input("Please enter the year "))
            if (year < 2015 or year > datetime.datetime.now().year):
                print ("Data not available")
            else:
                get_team_stats(year)
                
        elif (choice == 69):
            run = False
            
        print ()         
        
    
if __name__ == '__main__':
    main()