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

for elem in my_team.getTeamMatches(team_in, 10):
	print elem


def printTable(league, limit):
	table = []
	table_dict = {}
	for elem in league:
		scores = my_team.getPoints(elem, limit)
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

printTable(my_league.getTeamList(), 38)





