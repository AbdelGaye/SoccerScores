#!/usr/bin/python

import Tkinter
from Tkinter import *
import json
import urllib2


global gui
global main_menu_var

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
		self.link = info_dict[name]

	#Want to print Home team score - Away team score
	def getTeamMatches(self, team):
		matches_played = []
		data_matches = json.load(urllib2.urlopen(self.link))
		for item in data_matches["rounds"]:
			for matchdays in item.get("matches"):
				if (matchdays.get("team1").get("name") == team) or (matchdays.get("team2").get("name") == team):
					matches_played.append(str(matchdays.get("score1")) + " - " + str(matchdays.get("score2")))

		return matches_played


def printToGUI(txt):
	match_gui = Tkinter.Toplevel(gui)
	label = Label(match_gui, text= txt)
	#this creates a new label to the GUI
	label.pack()
    

en_league = League("England")
en_teams = en_league.getTeamList()

sp_league = League("Spain")
sp_teams = sp_league.getTeamList()

it_league = League("Italy")
it_teams = it_league.getTeamList()

de_league = League("Germany")
de_teams = de_league.getTeamList()

gui = Tkinter.Tk()

#Widgets below
OPTIONS = ["England", "Spain", "Italy", "Germany"]
main_menu_var = StringVar(gui)
main_menu_var.set("Select a league")
main_menu = apply(OptionMenu, (gui, main_menu_var) + tuple(OPTIONS))
main_menu.pack() 

variable = StringVar(gui)
variable.set(en_teams[0]) # default value

w = apply(OptionMenu, (gui, variable) + tuple(en_teams))
w.pack()

my_team = Teams("England")
txt = my_team.getTeamMatches(variable.get())

#Trying to activate button click only when team is selected
button = Button(gui, text="OK", command=printToGUI(txt))
button.pack()

gui.mainloop()

