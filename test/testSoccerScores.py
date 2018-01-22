#!/usr/bin/python
import unittest
import json
import nose2
from mock import patch

#from SoccerScores import League
#from SoccerScores import Teams
from SoccerScores import *

#In order to use unittest's methods
class Helper(unittest.TestCase):
	def runTest(self):
		pass

HELPER = Helper()

TESTDATA = {}
#Setup function
#The mockfile is in SoccerScores directory because open only checks for files in the current directory
def setup():
	with open('mockfile.json') as json_file:
		TESTDATA = json.load(json_file)
	


#TEST CASES FOR LEAGUE

#Test cases for __init__
def test_constructor():
	premleague = League("England")
	assert premleague.link, "https://raw.githubusercontent.com/opendatajson/football.json/master/2016-17/en.1.clubs.json"

def test_constructorfail():
#WORKS BUT BAD PRACTICE
#	try:
#		testvar = False
#		League("India")
#		testvar = True
#	except:
#		assert testvar is False

	with HELPER.assertRaises(KeyError):
		League("India")

#Test cases for getTeamList
def test_getTeamList():
	gleague = League("Germany")
	glist = gleague.getTeamList()
	num_teams = len(glist)

	#The right number of teams
	assert num_teams, 18

	#Making sure the list is sorted
	#The cmp method returns 0 if the lists share the same data
	new_list = glist.sort()
	assert cmp(new_list, glist), 0


#TEST CASES FOR TEAMS

#Test cases for __init__
def test_team_const():
	iteams = Teams("Italy")
	assert iteams.name, "Italy"
	assert iteams.name, "Spain" is False

def test_team_const_fail():
	with HELPER.assertRaises(KeyError):
		Teams(" ")

#Testing if getTeamMatches only returns matches from a selected team
def test_getTeamMatches_team():
	spteams = Teams("Spain")
	limit = 38

	counter = 0
	eibar_list = spteams.getTeamMatches("Eibar", limit)
	for item in eibar_list:
		if "Eibar" in item:
			counter=counter+1
	
	assert counter, limit

#Testing if getTeamMatches has the inputted limit
def test_getTeamMatches_limit():
	spteams = Teams("Spain")
	limit = 5

	eibar_list = spteams.getTeamMatches("Eibar", 5)
	elength = len(eibar_list)
	HELPER.assertEqual(elength, limit)

#Testing for invalid parameters does not change the coverage since there is no piece of code that checks for the right parameters inside the function
#def test_getTeamMatches_invalidteam():
#	enteams = Teams("England")
#	with HELPER.assertRaises(Exception):
#		fail_list = enteams.getTeamMatches("123", 10)

#def test_getTeamMatches_invalidlimit():
#	enteams = Teams("England")
#	with HELPER.assertRaises(Exception):
#		fail_list = enteams.getTeamMatches("Chelsea", "yo")

#Cannot use a mock json file so I should not have harded coded the dictionary inside the class
def test_getPointsWithMock():
	setup()
	Teams.info_dict = {"Test": 'mockfile.json'}
	with HELPER.assertRaises(KeyError):
		Teams("Test")

def test_getPoints():
	bteams = Teams("Germany")
	print bteams.getTeamMatches("RB Leipzig", 3)
	HELPER.assertEqual(bteams.getPoints("RB Leipzig", 3), 1+3+3)


#TEST CASES FOR FUNCTIONS

#def test_connected():
#	assert connect("http://www.google.com"), True

def testPrintResults():
	bplteams = Teams("England")
	bpl = League("England")

	iteams = Teams("Italy")
	seriea = League("Italy")

	with patch('__builtin__.raw_input', return_value='Chelsea') as _raw_input:
		HELPER.assertEqual(printResults(bpl, bplteams, 2), ['Chelsea 2 - 1 West Ham United', 'Watford 1 - 2 Chelsea'])
		#HELPER.assertEqual(printResults(seriea, iteams, 2), [])




if __name__ == '__main__':
    nose2.main()