import csv, datetime
from bs4 import BeautifulSoup
import requests
import numpy as np

team_cities = { 'Bucks':'MIL',
                'Bulls':'CHI',
                'Cavaliers':'CLE',
                'Celtics':'BOS',
                'Clippers':'LAC',
                'Grizzlies':'MEM',
                'Hawks':'ATL',
                'Heat':'MIA',
                'Hornets':'CHA',
                'Jazz':'UTA',
                'Kings':'SAC',
                'Knicks':'NY',
                'Lakers':'LAL',
                'Magic':'ORL',
                'Mavericks':'DAL',
                'Nets':'BKN',
                'Nuggets':'DEN',
                'Pacers':'IND',
                'Pelicans':'NO',
                'Pistons':'DET',
                'Raptors':'TOR',
                'Rockets':'HOU',
                'Sixers':'PHI',
                'Spurs':'SA',
                'Suns':'PHX',
                'Thunder':'OKC',
                'Timberwolves':'MIN',
                'Trailblazers':'POR',
                'Warriors':'GS',
                'Wizards':'WSH',
                'X':'X',
                }

city_teams = dict(zip(team_cities.values(), team_cities.keys()))

def get_daily_predictions():
    """
    Goes to 538 and gets todays predictions.
    Stores them as:
    Away team || Away win prob || Home team || Home win prob || Spread || Date
    in a csv named pred_538

    Note:
    Spread is positive if the home team is favored, negative if the away team is favored.
    """
    def try_float(str):
        try:
            return float(str)
        except:
            return 0
    url = 'https://projects.fivethirtyeight.com/2017-nba-predictions/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    predictions = soup.find('table', class_='prob-visible')
    away = predictions.find('tr', class_='away')
    awayprob = predictions.find('tr', class_='prob-row-top')
    homeprob = predictions.find('tr', class_='prob-row-bottom')
    home = predictions.find('tr', class_='home')
    away_teams = [i.text for i in away('td')][::2][1:]
    away_probabilities = [i.text[:-1] for i in awayprob('div', class_='away')]
    away_spread = [try_float(i.text) for i in awayprob('div', class_='spread')][1:]
    home_probabilities = [i.text[:-1] for i in homeprob('div', class_='home')]
    home_spread = [try_float(i.text) for i in homeprob('div', class_='spread')]
    home_teams = [i.text for i in home('td')][::2][1:]
    today = datetime.date.today()
    todays = [today]*len(home_teams)
    for i in xrange(len(home_teams)):
        if away_spread[i] != 0:
            home_spread[i] = -away_spread[i]
        elif home_spread[i] != 0:
            away_spread[i] = -home_spread[i]

    together = [[city_teams[x] for x in away_teams], away_teams, away_probabilities,
                [city_teams[x] for x in home_teams], home_teams, home_probabilities, home_spread, todays]
    together = np.array(together).T

    with open('data/pred_538.csv', 'a') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(['fran', 'fran_city', 'prob', 'opp', 'opp_city', 'opp_prob', 'sprd', 'date'])
        for row in together:
            if row[0] != 'X':
                writer.writerow(row)

    return True

if __name__=='__main__':
    get_daily_predictions()
