#!/usr/bin/env python3
import argparse
import datetime
import sys
import requests


class Scoreboard:
    """
    Creates a scoreboard object storing Games
    """
    def __init__(self, year, month, day):
        url = f"https://gd.mlb.com/components/game/mlb/year_{year}/month_{month}/day_{day}/master_scoreboard.json"
        scoreboard = requests.get(url)
        self.data = scoreboard.json()
        self.games = [Game(**game) for game in self.data["data"]["games"]["game"]]

    def get_games_by_league(self, league):
        """
        Returns list of games by league.
        Interleague games are returned always.
        """
        game_list = []
        for game in self.games:
            if league in game.league:
                game_list.append(game)
        return game_list

    def get_games_by_team(self, teams):
        """
        Returns list of games in which specified teams are playing
        """
        game_list = []
        for game in self.games:
            for team in teams:
                if team.upper() in (game.home_team_abbrev, game.away_team_abbrev):
                    game_list.append(game)
        return game_list

    def get_in_progress_games(self):
        """
        Returns games are currently in progress
        """
        game_list = []
        for game in self.games:
            if game.game_status["status"] == "In Progress":
                game_list.append(game)
        return game_list


class Game:
    """
    Class that stores game information
    """
    def __init__(self, **game_info):
        # self.game_info = game_info

        self.away_team = game_info["away_team_name"]
        self.away_team_abbrev = game_info["away_name_abbrev"]
        self.home_team = game_info["home_team_name"]
        self.home_team_abbrev = game_info["home_name_abbrev"]
        self.game_status = game_info["status"]
        self.game_time = game_info["time"]
        self.game_time_zone = game_info["time_zone"]
        self.league = game_info["league"]
        try:
            self.linescore = game_info["linescore"]
        except KeyError:
            self.linescore = None

    def game_board(self):
        """
        Returns string of individual game score
        """
        top_line = "_".ljust(28, "_")
        mid_line = "-".ljust(28, "-")
        bottom_line = "‾".ljust(28, "‾")
        away_team_name = self.away_team.ljust(12)
        home_team_name = self.home_team.ljust(12)

        away_runs = "0".rjust(3)
        away_hits = "0".rjust(3)
        away_errors = "0".rjust(3)
        home_runs = "0".rjust(3)
        home_hits = "0".rjust(3)
        home_errors = "0".rjust(3)

        if self.game_status["ind"] == "I":
            game_status = "{0} {1}".format(self.game_status["inning_state"],
                                           self.game_status["inning"])
        elif self.game_status["ind"] in ('P', 'S'):
            game_status = "{0} {1}".format(self.game_time,
                                           self.game_time_zone)
        else:
            game_status = self.game_status["ind"]

        if self.linescore:
            if self.game_status["status"] in ('Cancelled', 'Postponed'):
                away_runs = "".rjust(3)
                home_runs = "".rjust(3)
            else:
                away_runs = self.linescore["r"]["away"].rjust(3)
                home_runs = self.linescore["r"]["home"].rjust(3)
            away_hits = self.linescore["h"]["away"].rjust(3)
            away_errors = self.linescore["e"]["away"].rjust(3)
            home_hits = self.linescore["h"]["home"].rjust(3)
            home_errors = self.linescore["e"]["home"].rjust(3)

        game = f'''\
  {top_line}\n \
| {away_team_name}| {away_runs}| {away_hits}| {away_errors}|   {game_status}\n \
|{mid_line}|\n \
| {home_team_name}| {home_runs}| {home_hits}| {home_errors}|\n \
 {bottom_line}\n \
        '''
        return game


def main(args):
    """
    Prints games based on specified arguments
    """

    day = datetime.date.today()
    scoreboard = Scoreboard("{:04d}".format(day.year),
                            "{:02d}".format(day.month),
                            "{:02d}".format(day.day))

    games = scoreboard.games

    if args.league:
        games = scoreboard.get_games_by_league(args.league.upper()[0])

    if args.team:
        games = scoreboard.get_games_by_team(args.team)

    if args.in_progress:
        games = scoreboard.get_in_progress_games()

    for game in games:
        print(game.game_board())


def arg_parse():
    """
    Returns args to be sent to main function
    """
    parser = argparse.ArgumentParser(description="Prints MLB scores")
    parser.add_argument('-t', '--team', action='append',
                        help='Prints out teams given. They should be given as their abbreviation.')

    parser.add_argument('-l', '--league',
                        help='Prints games from either AL or NL. A for American, N for National')

    parser.add_argument('-p', '--in-progress', action='store_true',
                        help='Prints games that are currently in progress')
    args = parser.parse_args()

    if args.league and args.team:
        print("Unable to use league and team arguments together")
        sys.exit(1)

    if args.league and args.league not in ('NL', 'nl', 'N', 'n', 'AL', 'al', 'A', 'a'):
        print("Must select AL or NL")
        sys.exit(1)

    return args


if __name__ == '__main__':
    ARGS = arg_parse()
    main(ARGS)
