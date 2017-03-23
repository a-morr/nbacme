import numpy as np
import pandas as pd



def RollingAvgPoints(df,teams):
    df['Roll_Avg5_PTS'] = np.nan
    for team in teams:
        fran_indices = df[(df['fran_id']==team)].index
        fran_points = pd.rolling_mean(df[(df['fran_id']==team)]['pts'],5)
        df.ix[fran_indices,'Roll_Avg5_PTS'] = fran_points.tolist()

        fran_indices = df[(df['opp_fran']==team)].index
        fran_points = pd.rolling_mean(df[(df['opp_fran']==team)]['pts'],5)
        df.ix[fran_indices,'Roll_Avg5_PTS'] = fran_points.tolist()

if __name__ == "__main__":
    # Read in data
    filename = 'data/all_games.csv'
    df = pd.read_csv(filename)
    teams = df['fran_id'].unique()
    
    # Add new columns here
    RollingAvgPoints(df,teams)
    
    # Save final dataframe
    print df
    