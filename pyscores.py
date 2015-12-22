import sys
import json
import requests
from tabulate import tabulate
from termcolor import colored

import leagues
import secret

BASE_URL = "http://api.football-data.org/alpha/"
API_KEY = secret.secret_key

headers = {'X-Auth-Token' : API_KEY}

def get_fixtures(league):
	if league in leagues.LEAGUE_IDS:
		request_url = "{}soccerseasons/{}/fixtures?timeFrame=n7".format(BASE_URL, leagues.LEAGUE_IDS[league])
	else:
		print("Error: No such league code")

	try:
		resp = requests.get(request_url, headers=headers)
		data = resp.json()
		print_fixtures(data['fixtures'])
	except:
		print("Error retrieving fixtures")

def print_fixtures(array):
	current_matchday = array[0]['matchday']
	fixtures = []
	for fixture in array:
		if fixture['matchday'] == current_matchday:
			s = [
				(fixture['date'][8:10] + '-' + fixture['date'][5:7]),
				fixture['date'][11:16],
				fixture['homeTeamName'],
				'vs',
				fixture['awayTeamName']
			]
			fixtures.append(s)
	print(tabulate(fixtures, tablefmt="plain"))


def get_past_results(league):
	if league in leagues.LEAGUE_IDS:
		request_url = "{}soccerseasons/{}/fixtures?timeFrame=p7".format(BASE_URL, leagues.LEAGUE_IDS[league])
	else:
		print("Error: No such league code")

	try:
		resp = requests.get(request_url, headers=headers)
		data = resp.json()
		print_results(data['fixtures'])
	except:
		print("Error retrieving recent results")

def print_results(array):
	results = []
	for fixture in array:
		s = [
			fixture['homeTeamName'],
			fixture['result']['goalsHomeTeam'],
			'vs',
			fixture['result']['goalsAwayTeam'],
			fixture['awayTeamName']
		]
		if int(s[1]) > int(s[3]):
			s[0] = colored(s[0], 'green')
			s[-1] = colored(s[-1], 'red')
		elif int(s[1]) < int(s[3]):
			s[0] = colored(s[0], 'red')
			s[-1] = colored(s[-1], 'green')
		else:
			s[0] = colored(s[0], 'yellow')
			s[-1] = colored(s[-1], 'yellow')

		results.append(s)
	print(tabulate(results, tablefmt="plain"))

# Gets current league table from selected league and calls print function
def get_standings(league):
	if league in leagues.LEAGUE_IDS:
		request_url = "{}soccerseasons/{}/leagueTable".format(BASE_URL, leagues.LEAGUE_IDS[league])
	else:
		print("Error: No such league code")
		
	try:
		resp = requests.get(request_url, headers=headers)
		data = resp.json()	
		print_standings(data['standing'])
	except:
		print("Error retrieving selected league table...")

# Prints the league standings in a table
def print_standings(table):
	standings = []
	for team in table:
		entry = [
			team['position'],
			team['teamName'],
			team['playedGames'],
			team['points']
		]
		standings.append(entry)

	print(tabulate(standings, headers=['Pos', 'Club', 'Played', 'Points'], tablefmt="rst"))

def main():
	arg = sys.argv[1]
	# get_standings(sys.argv[1])
	#get_past_results(arg)
	get_fixtures(arg)

if __name__ == '__main__':
	main()