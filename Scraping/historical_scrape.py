from bs4 import BeautifulSoup
import numpy as np
from urllib2 import urlopen
import time, csv

stem = 'http://www.basketball-reference.com/leagues/NBA_'
years = [2016,2017]
months = ['october','november','december','january','february','march','april','may','june']

with open('recent_data.csv','w') as outfile:
	out = csv.writer(outfile)
	for year in years:
		for month in months:
			if year == 2017 and month == 'may':
				break
			url = stem+str(year)+'_games-'+month+'.html'
			soup = BeautifulSoup(urlopen(url),'html.parser')
			rows = soup.find('table', id='schedule').find_all('tr')
			games = [[entry.text for entry in row.find_all(['td','th'])[:-3]] for row in rows]
			out.writerows(games)
			print year, month
			time.sleep(3)
