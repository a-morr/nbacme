from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import time, csv
import pandas as pd
from scrape_utility import convert_name

def get_stats():
    """
    Scrapes daily from the basketball reference website for game results.
    Formats them and adds them to the current season csv.
    """
    stem = 'http://www.basketball-reference.com'
    seasonstem = stem + '/leagues/NBA_'
    years = range(2015,2000,-1)
    months = ['october','november','december','january','february','march','april','may','june']

    with open('data/hist_stats.csv','w') as outfile:
        out = csv.writer(outfile)
        out.writerow(['date','away','home','amp','afg','afga','afg_pct','afg3','afg3a','afg3_pct','aft','afta','aft_pct','aord','adrb','atrb','aast','astl','ablk','atov','apf','apts',
                                           'hmp','hfg','hfga','hfg_pct','hfg3','hfg3a','fhg3_pct','hft','hfta','hft_pct','hord','hdrb','htrb','hast','hstl','hblk','htov','hpf','hpts'])
        for year in years:
            for month in months:
                try:
                    url = seasonstem+str(year)+'_games-'+month+'.html'
                    soup = BeautifulSoup(urlopen(url),'html.parser')
                except:
                    continue
                rows = soup.find('table', id='schedule').find_all('tr')
                try:
                    games = [row.find_all('td')[-3].find('a')['href'] for row in rows[1:]]
                except:
                    temp = [row.find_all('td') for row in rows[1:]]
                    games = []
                    for i in temp:
                        if len(i) > 3:
                            if i[-3].find('a'):
                                games.append(i[-3].find('a')['href'])
                for game in games:
                    gamestem = stem + game
                    try:
                        soup = BeautifulSoup(urlopen(gamestem),'html.parser')
                    except:
                        print game, 'failed'
                        continue
                    away, home = map(convert_name, [i.find('a')['href'][7:10] for i in soup.find_all('strong')[1:3]])
                    date = game[11:15] + '-' + game[15:17] + '-' + game[17:19]
                    awayinfo = [i.text for i in soup.find_all('table', class_='stats_table')[0].find('tfoot').find('tr').find_all('td')[:-1]]
                    homeinfo = [i.text for i in soup.find_all('table', class_='stats_table')[2].find('tfoot').find('tr').find_all('td')[:-1]]
                    output = [date, away, home] + awayinfo + homeinfo
                    print date, away, '@', home
                    out.writerow(output)              
                    time.sleep(0.1)

if __name__=='__main__':
    get_stats()