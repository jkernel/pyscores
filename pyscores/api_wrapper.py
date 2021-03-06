"""A wrapper class for the football-data API"""

import os

import requests


class APIWrapper(object):

    def __init__(self, base_url=None, auth_token=None):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = "http://api.football-data.org/v1"

        if auth_token:
            self.headers = {'X-Auth-Token': auth_token}
        else:
            self.headers = {}

    def _request(self, url, filters=None):
        """
        Send a GET request to the API and return the JSON result.
        
        :param url: The URL of the API endpoint to be queried.
        :param filters: A dict of optional filters(params) to include in the request.
        :return: The JSON response of the request 
        """
        params = filters if filters else {}
        r = requests.get(url=url, params=params, headers=self.headers)
        if r.status_code == requests.codes.ok:
            return r.json()
        return None

    def all_competitions(self, filters=None):
        """
        Return a list of competitions (defaults to competitions in current season).
        
        Filters:
        - season
        """
        url = "{0}/competitions".format(self.base_url)
        response = self._request(url=url, filters=filters)
        return response

    def competition(self, competition_id):
        """Return a JSON object for a competition by its id."""
        url = "{0}/competitions/{1}".format(self.base_url, competition_id)
        response = self._request(url=url)
        return response

    def competition_teams(self, competition_id):
        """Return a JSON list of teams in a particular competition."""
        url = "{0}/competitions/{1}/teams".format(self.base_url, competition_id)
        return self._request(url=url)

    def competition_fixtures(self, competition_id, filters=None):
        """
        Return a JSON list of all fixtures, past and present, in a competition.
        
        Filters:
        - timeFrame
        - matchday
        """
        url = "{0}/competitions/{1}/fixtures".format(self.base_url, competition_id)
        return self._request(url=url, filters=filters)

    def competition_table(self, competition_id, filters=None):
        """
        Return the current league table for a competition as a JSON list.
        
        Example filters:
        - matchday=23
        """
        url = "{0}/competitions/{1}/leagueTable".format(self.base_url, competition_id)
        return self._request(url=url, filters=filters)

    def team_search(self, name):
        """
        Search for a team by name.
        
        Return a JSON object which contains a list of search results matching the name.
        """
        url = "{0}/teams".format(self.base_url)
        return self._request(url=url, filters={'name': name})

    def team(self, team_id):
        """Return a JSON object for a team by id."""
        url = "{0}/teams/{1}".format(self.base_url, team_id)
        return self._request(url=url)

    def team_players(self, team_id):
        """Return a JSON list of the players playing for a team."""
        url = "{0}/teams/{1}/players".format(self.base_url, team_id)
        return self._request(url=url)

    def team_fixtures(self, team_id, filters=None):
        """
        Return a list of fixtures for a team.
        
        Example filters:
        - season=2016   -> Fixtures for the 2016/2017 season
        - timeFrame=p20 -> Fixtures for previous 20 days
        - timeFrame=n7  -> Fixtures for next 7 days (default)
        - timeFrameStart=2017-03-14&timeFrameEnd=2017-03-31
                        -> Fixtures between two dates (both must be present)
        - venue=home    -> Show only home or away fixtures
        """
        url = "{0}/teams/{1}/fixtures".format(self.base_url, team_id)
        return self._request(url=url, filters=filters)

    def all_fixtures(self, filters=None):
        """
        Return a list of fixtures across a set of competitions.
        
        Filters:
        - timeFrame
        - league
        """
        url = "{0}/fixtures".format(self.base_url)
        return self._request(url=url, filters=filters)

    def fixture(self, fixture_id, filters=None):
        """
        Return a fixture by its id.
        
        A fixture will contain the latest fixture between two teams, as well as
        past fixtures between those two same teams.
        
        Filters:
        - head2head=15  -> Show the last 15 fixtures between the teams (default 10)
        """
        url = "{0}/fixtures/{1}".format(self.base_url, fixture_id)
        return self._request(url=url, filters=filters)


def main():
    api = APIWrapper(auth_token=os.environ["PYSCORES_KEY"])
    res = api.all_competitions()
    print(res)

if __name__ == "__main__":
    main()

