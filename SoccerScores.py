#!/usr/bin/python

import json
import urllib2


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
	def getTeamMatches(self, team):
		matches_played = []
		for item in self.data_matches["rounds"]:
			for matchdays in item.get("matches"):
				homeTeam = matchdays.get("team1").get("name")
				awayTeam = matchdays.get("team2").get("name")

				if (homeTeam == team) or (awayTeam == team):
					homeScore = matchdays.get("score1")
					awayScore = matchdays.get("score2")
					matches_played.append(homeTeam + " " + str(matchdays.get("score1")) + " - " + str(matchdays.get("score2")) + " " + awayTeam)

		return matches_played

	

#Main function starts here
print "Please enter a league."

my_league = ""
while my_league == "":
	user_in = raw_input()
	try:
		my_league = League(user_in)
	except:
		print "Invalid league. Please try again."

for elem in my_league.getTeamList():
	print elem


print "Enter a team of your choice."
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

my_team = Teams(my_league.name)

for elem in my_team.getTeamMatches(team_in):
	print elem




