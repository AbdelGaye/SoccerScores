#!/usr/bin/python

import sys
import json
import urllib2

#This class takes care of a specific league
class League:
	global league_dict
	league_dict = {"England": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/en.1.clubs.json", 
	"Spain": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/es.1.clubs.json",
	"Italy": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/it.1.clubs.json",
	"Germany": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/de.1.clubs.json"}

	def __init__(self, name):
		global league_dict
		self.name = name
		self.link = league_dict[name]

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
	global info_dict
	info_dict = {"England": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/en.1.json",
	"Spain": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/es.1.json",
	"Italy": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/it.1.json",
	"Germany": "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/de.1.json"}

	def __init__(self, name):
		global info_dict
		self.name = name
		self.data_matches = json.load(urllib2.urlopen(info_dict[name]))


	#Returns the list of matches of a team
	def getTeamMatches(self, team, limit):
		matches_played = []
		counter = 1
		for item in self.data_matches["rounds"]:
			if counter > limit:
				break
			else:
				for matchdays in item.get("matches"):
					homeTeam = matchdays.get("team1").get("name")
					awayTeam = matchdays.get("team2").get("name")

					if (homeTeam == team) or (awayTeam == team):
						homeScore = matchdays.get("score1")
						awayScore = matchdays.get("score2")
						matches_played.append(homeTeam + " " + str(matchdays.get("score1")) + " - " + str(matchdays.get("score2")) + " " + awayTeam)
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
					homeTeam = matchdays.get("team1").get("name")
					awayTeam = matchdays.get("team2").get("name")
					homeScore = matchdays.get("score1")
					awayScore = matchdays.get("score2")

					if homeTeam == team:
						if homeScore > awayScore:
							pts = pts+3
						elif homeScore == awayScore:
							pts=pts+1
					elif awayTeam == team:
						if awayScore > homeScore:
							pts = pts+3
						elif homeScore == awayScore:
							pts=pts+1

				counter = counter+1

		return pts


	

#Main function starts here
print "Please enter a league."

#Checking for invalid inputs
my_league = ""
while my_league == "":
	user_in = raw_input()
	try:
		my_league = League(user_in)
	except:
		print "Invalid league. Please try again."

print "\nWelcome to the " + my_league.name + " league."
print "Here is a list of the current teams."
for elem in my_league.getTeamList():
	print elem

my_team = Teams(my_league.name)

print "\nPlease select a mode: Team results, Matchday results, Table"

modes = ["team results", "matchday results", "table"]

#Function for matchdays
def user_input():
	inp = 1
	print "Which matchday would you want to display? Type 38 to get full results."
	while 1:
		inp = input()
		if (inp > 38) or (inp < 1):
			print "Invalid value. Please try again."
		else:
			break
	return inp


#Function for printing the results of a specific team
def printResults(team, limit):
	print "\nEnter a team of your choice."
	index = -1
	team_in = ""
	while index == -1:
		team_in = raw_input()

		for elem in my_league.getTeamList():
			if elem == team_in:
				index = 1
				break

		if index == -1:
			print "Team is not in this league. Please try again."

	for elem in team.getTeamMatches(team_in, limit):
		print elem


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
def userMode(mode):
	if mode == "table":
		printTable(my_league.getTeamList(), my_team, user_input())
	elif mode == "team results":
		printResults(my_team, user_input())


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
		userMode(my_mode)
		print "Another mode?" 





