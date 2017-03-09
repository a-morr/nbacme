# main.py
from Machine_Learning import Kristaps
from Scraping import scrape_538, daily
# Scraping function
daily.daily_nba_ref()
scrape_538.get_daily_predictions()


# Training
k = kristaps.Kristaps()
k.train('../data/historical_data.csv')

# Creates csv for website
k.predict_today()       # This creates tomorrow.csv
k.simulate_seasons()    # This creates ProjectedWL.csv