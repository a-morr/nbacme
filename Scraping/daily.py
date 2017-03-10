from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime, timedelta
import pandas as pd
import csv

def daily_nba_ref():
    """
    Scrapes daily from the basketball reference website for game results.
    Formats them and adds them to the current season csv.
    """
    stem = 'http://www.basketball-reference.com/leagues/NBA_'

    now = datetime.now()
    yesterday = now - timedelta(days=1)
    month = yesterday.month
    year = yesterday.year + month // 10

    strmonth = yesterday.strftime('%B').lower()
    datestring = yesterday.strftime('%a, %b %-d, %Y')
    url = stem+str(year)+'_games-'+strmonth+'.html'
    soup = BeautifulSoup(urlopen(url),'html.parser')
    rows = soup.find('table', id='schedule').find_all('tr')
    games = [[entry.text for entry in row.find_all(['td','th'])[:-3]] for row in rows]
    today = []
    header = games[0]
    header[5] = 'PTS.1'

    for game in games:
        if game[0] == datestring:
            today.append(game)

    recent = pd.DataFrame(today, columns=header)

    # Make it look like historical data
    recent['fran_id'] = recent['Visitor/Neutral'].str.split().str[-1]
    recent['opp_fran'] = recent['Home/Neutral'].str.split().str[-1]
    fn = {'76ers':'Sixers', 'Blazers':'Trailblazers'}
    recent['fran_id'].replace(fn, inplace=True)
    recent['opp_fran'].replace(fn, inplace=True)
    recent['pts'] = recent['PTS']
    recent['opp_pts'] = recent['PTS.1']
    recent['game_location'] = 'A'

    # Parse dates
    recent['day'] = recent['Date'].str.split().str[2].str[:-1].map(int)
    recent['month'] = recent['Date'].str.split().str[1]
    recent['year'] = recent['Date'].str.split().str[-1].map(int)
    months = {'Jan' : 1,'Feb' : 2,'Mar' : 3,'Apr' : 4,'May' : 5,'Jun' : 6,'Jul' : 7,'Aug' : 8,'Sep' : 9,'Oct' : 10,'Nov' : 11,'Dec' : 12}
    recent['month'].replace(months,inplace=True)
    recent['date'] = pd.to_datetime(recent.year*10000+recent.month*100+recent.day,format='%Y%m%d')
    recent = recent[['fran_id','pts','opp_fran','opp_pts','game_location','date']]
    recent.to_csv('../data/historical_data.csv', mode='a', header=False, index=None)

if __name__=='__main__':
    daily_nba_ref()