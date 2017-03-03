from bs4 import BeautifulSoup
from urllib2 import urlopen
import bs4
import pandas as pd
import pickle
import time
import calendar
import requests
import re


def startup():
    dailyStandings = "http://www.basketball-reference.com/leagues/NBA_2017_standings.html"
    allGames = "http://www.basketball-reference.com/leagues/NBA_2017_games-february.html"
    soup = BeautifulSoup(urlopen(dailyStandings), "lxml")
    allTeams = soup.find(class_="standings_confs table_wrapper").div.tbody

    totalTeams = []
    wins = []
    losses = []
    wl_perc = []
    gb = []
    ppg = []
    oppg = []
    conference = []

    def fillLists(tagIn, conf):
        for i in tagIn:

            if isinstance(i, bs4.element.NavigableString):
                pass
            else:
                totalTeams.append(str((i.contents[0].find('a').text)))
                wins.append(int(i.contents[1].text))
                losses.append(int(i.contents[2].text))
                wl_perc.append(float(i.contents[3].text))
                try:
                    gb.append(float(i.contents[4].text))
                except:
                    gb.append(0.)

                ppg.append(float(i.contents[5].text))
                oppg.append(float(i.contents[6].text))
                conference.append(str(conf))

    east = soup.find(class_="standings_confs table_wrapper").find("div",  {"id": "all_confs_standings_E"}).tbody
    west = soup.find(class_="standings_confs table_wrapper").find("div",  {"id": "all_confs_standings_W"}).tbody

    fillLists(west, 'West')
    fillLists(east, 'East')

    data = {'Team':totalTeams, 'Win':wins, 'Loss':losses, 'WL %':wl_perc, 'Conference':conference, 'Games Behind':gb, 'Points Per/G':ppg, 'Op Points Per/G':oppg}
    df = pd.DataFrame.from_dict(data)
    df = df[['Team', 'Conference', 'Win', 'Loss', 'WL %', 'Games Behind', 'Points Per/G', 'Op Points Per/G']]
    df = df.sort(['Win'], ascending=[False])
    with open('nba.pickle', 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

def post():
    with open('nba.pickle', 'rb') as handle:
        df = pickle.load(handle)
    #print df
    date = time.strftime("%D:%M:%Y")
    month = date[:2]
    day = date[3:5]
    day = str(int(day))
    month = str(int(month))
    year = date[6:8]
    print day, month, year
    cal = dict((str(k),v.lower()) for k,v in enumerate(calendar.month_name))
    print cal[month]

    searchFor = ("/boxscores/index.cgi?month=%s&amp;day=%s&amp;year=%s" % (day, month, year))
    print searchFor
    print df

def fiveThreeEight():
    with open('nba.pickle', 'rb') as handle:
        old = pickle.load(handle)



    url538 = "https://projects.fivethirtyeight.com/2017-nba-predictions/"
    r = requests.get(url538)

    soup = BeautifulSoup(r.content,"lxml")
    soup = soup.find("table", { "id" : "standings-table" }).next.nextSibling.findAll("tr")

    names = []
    elo = []
    record = []
    pointDiff = []
    percMakePlayoffs = []
    percTopSeed = []
    df = pd.DataFrame()


    for i in soup:
        #print filter(str.isalpha, str(i.find(class_="team").text))
        names.append(filter(str.isalpha, str(i.find(class_="team").text)))
        elo.append(i.find(class_="num elo carmelo").text)
        record.append(i.find(class_="num div proj-rec break").text)

        pointDiff.append(float(i.find(class_="num desktop").text))
        regex = re.compile('[^0-9]')

        pmakeP = regex.sub('',i.find(class_="pct div break").text)
        pmakeP = .01 * float(pmakeP)
        percMakePlayoffs.append(float(pmakeP))


        try:
            ptopP = regex.sub('',i.find(class_="pct top-seed").text)
            ptopP = .01 * float(ptopP)
        except:
            ptopP = .01
        percTopSeed.append(float(ptopP))

        #print i
    df['Name'] = names
    df['CARM-ELO'] = elo
    df['ProjRec 538'] = record
    df['PointDiff 538'] = pointDiff
    df['Make Playoffs % 538'] = percMakePlayoffs
    df['Top Seed % 538'] = percTopSeed



    #print df.Name
    mascots = list(old.Team)
    for i in xrange(len(mascots)):
        mascots[i] = mascots[i].rsplit(None, 1)[-1]

    #print mascots
    old['Name'] = mascots


    df = df.replace(to_replace='ers', value='76ers',)
    df = df.replace(to_replace='TrailBlazers', value='Trail Blazers',)

    old = old.replace(to_replace='Blazers', value='Trail Blazers',)
    #print df.Name.values
    #print old.Name.values
    df = df.merge(old, left_on='Name', right_on='Name', how='outer')

    df = df[['Name', 'Conference', 'Win', 'Loss', 'WL %',  'ProjRec 538', 'CARM-ELO', 'PointDiff 538', 'Games Behind', 'Make Playoffs % 538', 'Top Seed % 538', 'Points Per/G', 'Op Points Per/G']]
    print df


if __name__=="__main__":
    #startup()
    #post()
    fiveThreeEight()
