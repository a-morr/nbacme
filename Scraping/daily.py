from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import time, csv
import pandas as pd

def daily_nba_ref():
    """
    Scrapes daily from the basketball reference website for game results.
    Formats them and adds them to the current season csv.
    """
    stem = 'http://www.basketball-reference.com/leagues/NBA_'
    year = 2017
    months = ['october','november','december','january','february','march','april','may','june']

    with open('data/current_raw.csv','w') as outfile:
        out = csv.writer(outfile)
        for month in months:
            try:
                url = stem+str(year)+'_games-'+month+'.html'
                soup = BeautifulSoup(urlopen(url),'html.parser')
            except:
                continue
            rows = soup.find('table', id='schedule').find_all('tr')
            games = [[entry.text for entry in row.find_all(['td','th'])[:-3]] for row in rows]
            out.writerows(games)
            print year, month
            time.sleep(3)

def split_current():
    ## Future games pull out
    recent = pd.read_csv('data/current_raw.csv')
    recent = recent[recent['Date'] != 'Date']

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
    recent['day'] = recent['Date'].str.split().str[2].str[:-1].astype(int)
    recent['month'] = recent['Date'].str.split().str[1]
    recent['year'] = recent['Date'].str.split().str[-1].astype(int)
    months = {'Jan' : 1,'Feb' : 2,'Mar' : 3,'Apr' : 4,'May' : 5,'Jun' : 6,'Jul' : 7,'Aug' : 8,'Sep' : 9,'Oct' : 10,'Nov' : 11,'Dec' : 12}
    recent['month'] = recent['month'].replace(months).astype(int)
    recent['date'] = pd.to_datetime(recent.year*10000+recent.month*100+recent.day,format='%Y%m%d')
    recent = recent[['fran_id','pts','opp_fran','opp_pts','game_location','date']]


    upcoming = recent[recent['pts'] != recent['pts']]
    upcoming.to_csv('data/upcoming_games.csv',index=None)

    recent = recent[recent['pts'] == recent['pts']]
    recent.to_csv('data/current_season.csv', index=None)

def make_final_dataset():
    recent = pd.read_csv('data/current_season.csv')
    hist_data = pd.read_csv('data/historical_data.csv')
    final = pd.concat([hist_data, recent])
    final.to_csv('data/all_games.csv',index=None)


if __name__=='__main__':
    #daily_nba_ref()
    split_current()
    make_final_dataset()