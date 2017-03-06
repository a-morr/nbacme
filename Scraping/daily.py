from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime, timedelta
import csv

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

for game in games:
	if game[0] == datestring:
		today.append(game)

with open('live_season.csv', 'a') as outfile:
	out = csv.writer(outfile)
	out.writerows(games)