#!/usr/bin/python

import sys
import json
import urllib2


#This class takes care of a specific league
class League:
    
    LEAGUE_DICT = {"England": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/en.1.clubs.json", 
    "Spain": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/es.1.clubs.json",
    "Italy": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/it.1.clubs.json",
    "Germany": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/de.1.clubs.json"}

    def __init__(self, name):
        self.name = name
        self.link = self.LEAGUE_DICT[name]

    #Returns the list of teams in a league
    def getTeamList(self):
        team_list = []
        data_clubs = json.load(urllib2.urlopen(self.link))
        for item in data_clubs["clubs"]:
            team_list.append(item.get("name"))
        team_list.sort()

        return team_list

#This class takes care of specific teams
class Teams:

    INFO_DICT = {"England": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/en.1.json",
    "Spain": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/es.1.json",
    "Italy": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/it.1.json",
    "Germany": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/de.1.json"}

    def __init__(self, name):
        self.name = name
        self.data_matches = json.load(urllib2.urlopen(self.INFO_DICT[name]))


    #Returns the list of matches of a team
    def getTeamMatches(self, team, limit):
        matches_played = []
        counter = 1
        for item in self.data_matches["rounds"]:
            if counter > limit:
                break
            else:
                for matchdays in item.get("matches"):
                    home_team = matchdays.get("team1").get("name")
                    away_team = matchdays.get("team2").get("name")

                    if (home_team == team) or (away_team == team):
                        #home_score = matchdays.get("score1")
                        #away_score = matchdays.get("score2")
                        matches_played.append(home_team + " " + str(matchdays.get("score1")) + " - " + str(matchdays.get("score2")) + " " + away_team)
                counter = counter+1

        return matches_played

    #Returns the number of points of a team
    def getPoints(self, team, limit):
        pts = 0
        counter = 1
        for item in self.data_matches["rounds"]:
            if counter > limit:
                break
            else:
                for matchdays in item.get("matches"):
                    home_team = matchdays.get("team1").get("name")
                    away_team = matchdays.get("team2").get("name")
                    home_score = matchdays.get("score1")
                    away_score = matchdays.get("score2")

                    if home_team == team:
                        if home_score > away_score:
                            pts = pts+3
                        elif home_score == away_score:
                            pts=pts+1
                    elif away_team == team:
                        if away_score > home_score:
                            pts = pts+3
                        elif home_score == away_score:
                            pts=pts+1

                counter = counter+1

        return pts


    

def connect(host):
    try:
        urllib2.urlopen(host)
    except Exception:
        print "No Internet connection!"
        raise

#Function for matchdays
def user_input():
    print "Which matchday would you want to display? Type 38 to get full results."
    while 1:
        try:
            inp = input()
            if (inp > 38) or (inp < 1):
                print "Invalid value. Please try again."
            else:
                break
        except Exception:
            print "Invalid value. Please try again."
        
    return inp


#Function for printing the results of a specific team
def printResults(league, team, limit):
    teamlist = []
    team_in = raw_input("\nEnter a team of your choice.\n")
    index = -1
    #team_in = ""
    while index == -1:
        #team_in = raw_input()

        for elem in league.getTeamList():
            if elem == team_in:
                index = 1
                break

        if index == -1:
            print "Team is not in this league. Please try again."

    for elem in team.getTeamMatches(team_in, limit):
        print elem
        teamlist.append(elem)

    return teamlist


#Function for printing the league table
def printTable(league, team, limit):
    table = []
    table_dict = {}
    for elem in league:
        scores = team.getPoints(elem, limit)
        table.append(scores)
        table_dict[elem] = scores
    #Removing duplicates from the list of scores
    finalt = list(set(table))
    finalt.sort(reverse = True)

    #Using the sorted list of scores to print an ordered table
    for entry in finalt:
        for elem in league:
            if table_dict[elem] == entry:
                print elem + " " + str(table_dict[elem])


#Function for taking action based on user modes
def userMode(mode, league, team):
    if mode == "table":
        printTable(league.getTeamList(), team, user_input())
    elif mode == "team results":
        printResults(league, team, user_input())


def main():
    connect("https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/en.1.clubs.json")

    #Main function starts here
    print "Please enter a league."

    #Checking for invalid inputs
    my_league = ""
    while my_league == "":
        user_in = raw_input()
        try:
            my_league = League(user_in)
        except KeyError:
            print "Invalid league. Please try again."

    print "\nWelcome to the " + my_league.name + " league."
    print "Here is a list of the current teams."
    for elem in my_league.getTeamList():
        print elem

    my_team = Teams(my_league.name)

    print "\nPlease select a mode: Team results, Matchday results, Table"

    modes = ["team results", "matchday results", "table"]

    #Once the user has put in a mode
    while 1:
        index = -1
        my_mode = raw_input().lower()
        for elem in modes:
            if my_mode == elem:
                index = 1
                break

        if my_mode == "q":
            sys.exit()
        elif index == -1:
            print "Invalid mode. Please try again."
        elif index == 1:
            userMode(my_mode, my_league, my_team)
            print "Another mode?" 


if __name__ == '__main__':
    main()



