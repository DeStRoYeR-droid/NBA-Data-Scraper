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

def get_team(year : int, teamID : str):
    extension = f"/data/1h/prod/{year}/teams_config.json"
    data = requests.get(BASE_URL + extension).json()["teams"]["config"]
    
    for value in data:
        if (value["teamId"] == teamID):
            return value["ttsName"]

def get_players_info(year : int):
    extension = f"/data/10s/prod/v1/{year}/players.json"
    data = requests.get(BASE_URL + extension).json()["league"]["standard"]
    
    players = [["Index" , "FirstName" , "LastName" , "Height (m)", "Height (feet)" , "Weight (lb)" , "Weight (kg)" , "Country" , "Position" , "Debut Year"]]
    for value in data:
        player = []
        player.append(len(players))
        player.append(value['firstName'])
        player.append(value['lastName'])
        player.append(value['heightMeters'])
        player.append(value['heightFeet'] + '\' ' + value['heightInches'] + '\"')
        player.append(value['weightPounds'] + "lb")
        player.append(value['weightKilograms'] + "kg")
        player.append(value['country'])
        player.append(value['pos'])
        player.append(value['nbaDebutYear'])
        
        players.append(player)
        
    return players

def get_playoff_stats(year : int):
    extension = f"/data/10s/prod/v1/{year}/playoffsBracket.json"
    data = requests.get(BASE_URL + extension).json()["series"]
    
    for value in data:
        print (f"=================================")
        print (f"Conference - {value['confName']}\t")
        print (f"Round      - {value['roundNum']}\t\t\t")
        print (f"-------------------------------")
        print (f"{get_team(2016, value['bottomRow']['teamId'])}\t\t")
        print (f"\tSeed -  {value['bottomRow']['seedNum']}\t\t")
        print (f"\tWins -  {value['bottomRow']['wins']}\t\t")
        print (f"{get_team(2016, value['topRow']['teamId'])}\t\t")
        print (f"\tSeed -  {value['topRow']['seedNum']}\t\t")
        print (f"\tWins -  {value['topRow']['wins']}\t\t")
        print (f"------------------------------")
        print (f"Result - {value['summaryStatusText']}\t\t")
        print (f"=================================")
        print ()

def get_team_info(year : int):
    extension = f"/data/prod/v2/{year}/teams.json"
    data = requests.get(BASE_URL + extension).json()["league"]["standard"]
    
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
    extension = f"/data/10s/prod/v1/{year}/team_stats_rankings.json"
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
        print ("3. Get team stats")
        print ("4. Get playoff stats")
        print ("5. Get players info by season")
        print ("69. Exit the menu")        
        choice = int(input("Please enter your choice "))
        
        if (choice == 1):
            year = int(input("Please enter the year "))
            if (year < 2019 or year > datetime.datetime.now().year):
                print ("Data not available")
            else:
                get_coach_info(year)
                
        elif (choice == 2):
            year = int(input("Please enter the year "))
            if (year < 2019 or year > datetime.datetime.now().year):
                print ("Data not available")
            else:
                get_team_info(year)
            
        elif (choice == 3):
            year = int(input("Please enter the year "))
            if (year < 2015 or year > datetime.datetime.now().year):
                print ("Data not available")
            else:
                get_team_stats(year)
            
        elif (choice == 4):
            year = int(input("Please enter the year "))
            if (year < 2016 or year > 2020):
                print ("Data not available")
            else:
                get_playoff_stats(year)
                
        elif (choice == 5):
            year = int(input("Please enter the year "))
            if (year < 2012 or year > 2022):
                print ("Data not available")
            else:
                print (tabulate(get_players_info(year) , headers="firstrow"))
                
        elif (choice == 69):
            run = False
            
        print ()         
        
    
if __name__ == '__main__':
    main()