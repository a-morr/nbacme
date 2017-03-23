import numpy as np


def convert_name(name):
    try:
        name = str(name)
    except:
        return "Invalid character in name :" + name

    teams = {"Warriors": "Warriors","Golden State": "Golden State Warriors","GSW": "Warriors","GS": "Warriors",
             "Spurs": "Spurs", "San Antonio": "Spurs", "San Antonio Spurs": "Spurs", "SA": "Spurs", "SAS": "Spurs",
             "Rockets": "Rockets", "Houston": "Rockets", "Houston Rockets": "Rockets", "HOU": "Rockets",
             "Celtics": "Celitcs", "Boston": "Celitcs", "Boston Celtics": "Celitcs", "BOS": "Celitcs",
             "Wizards": "Wizards", "Washington DC": "Wizards", "Washington D.C.": "Wizards", "Washington Wizards": "Wizards", "WSH": "Wizards", "WAS": "Wizards",
             "Jazz": "Jazz", "Utah": "Jazz", "Utah Jazz": "Jazz", "UTA": "Jazz",
             "Cavaliers": "Cavaliers", "Cleveland": "Cavaliers", "Cleveland Cavaliers": "Cavaliers", "CLE": "Cavaliers",
             "Clippers": "Clippers", "Los Angeles Clippers": "Clippers", "LAC": "Clippers",
             "Raptors": "Raptors", "Toronto": "Raptors", "Toronto Raptors": "Raptors", "TOR": "Raptors",
             "Heat": "Heat", "Miami": "Heat", "Miami Heat": "Heat", "MIA": "Heat",
             "Grizzlies": "Grizzlies", "Memphis": "Grizzlies", "Memphis Grizzlies": "Grizzlies", "MEM": "Grizzlies",
             "Timberwolves": "Timberwolves", "Minnesota": "Timberwolves", "Minnesota Timberwolves": "Timberwolves", "MIN": "Timberwolves",
             "Thunder": "Thunder", "Oklahoma": "Thunder", "Oklahoma City": "Thunder", "Oklahoma City Thunder": "Thunder", "OKC": "Thunder",
             "Trailblazers": "Trailblazers", "Trail blazers": "Trailblazers", "Trail Blazers": "Trailblazers", "Portland Trailblazers": "Trailblazers", "Portland Trail Blazers": "Trailblazers", "Portland Trail blazers": "Trailblazers", "Blazers": "Trailblazers", "POR": "Trailblazers",
             "Pacers": "Pacers", "Indiana": "Pacers", "Indiana Pacers": "Pacers", "IND": "Pacers",
             "Mavericks": "Mavericks", "Dallas": "Mavericks", "Dallas Mavericks": "Mavericks", "Mavs": "Mavericks", "DAL": "Mavericks",
             "Nuggets": "Nuggets", "Denver": "Nuggets", "Denver Nuggets": "Nuggets", "DEN": "Nuggets",
             "Hornets": "Hornets", "Charlotte": "Hornets", "Charlotte Hornets": "Hornets", "CHA": "Hornets", "CHO": "Hornets",
             "Bucks": "Bucks", "Milwaukee": "Bucks", "Milwaukee Bucks": "Bucks", "MIL": "Bucks",
             "Pistons": "Pistons", "Detroit": "Pistons", "Detroit Pistons": "Pistons", "DET": "Pistons",
             "Bulls": "Bulls", "Chicago": "Bulls", "Chicago Bulls": "Bulls", "CHI": "Bulls",
             "Hawks": "Hawks", "Atlanta": "Hawks", "Atlanta Hawks": "Hawks", "ATL": "Hawks",
             "Pelicans": "Pelicans", "New Orleans": "Pelicans", "New Orleans Pelicans": "Pelicans", "NO": "Pelicans",
             "Knicks": "Knicks", "NY": "Knicks", "NY Knicks": "Knicks", "New York Knicks": "Knicks", "NYN": "Knicks", "New York": "Knicks", "NYK": "Knicks",
             "Kings": "Kings", "Sacramento": "Kings", "Sacramento Kings": "Kings", "SAC": "Kings",
             "Suns": "Suns", "Phoenix": "Suns", "Phoenix Suns": "Suns", "PHX": "Suns", "PHO": "Suns",
             "Magic": "Magic", "Orlando": "Magic", "Orlando Magic": "Magic", "ORL": "Magic",
             "Sixers": "Sixers", "76ers": "Sixers", "76'ers": "Sixers", "76 ers": "Sixers", "Philadelphia": "Sixers", "Philadelphia 76ers": "Sixers", "Philadelphia Sixers": "Sixers", "Philadelphia 76'ers": "Sixers", "Philadelphia 76 ers": "Sixers", "PHI": "Sixers",
             "Lakers": "Lakers", "Los Angeles Lakers": "Lakers", "LAL": "Lakers",
             "Nets": "Nets", "Brooklyn": "Nets", "Brooklyn Nets": "Nets", "BKN": "Nets", "BRK": "Nets",
             }

    try:
        return teams[name]
    except:
        return "Error uploading : " + name


if __name__ == '__main__':
    pass
    """print convert_name('Blazers')
    print convert_name('76ers')
    print convert_name('76 ers')
    print convert_name("76'ers")
    """
