import numpy as np
import pandas as pd
import pickle


def RollingAvg(df,teams,column,window):
    new_col = 'RollAvg_'+str(window)+'_'+column
    df[new_col] = np.nan
    for team in teams:
        fran_indices = df[(df['fran_id']==team)].index
        fran_points = pd.rolling_mean(df[(df['fran_id']==team)][column],window)
        df.ix[fran_indices,new_col] = fran_points.tolist()

        fran_indices = df[(df['opp_fran']==team)].index
        fran_points = pd.rolling_mean(df[(df['opp_fran']==team)][column],window)
        df.ix[fran_indices,new_col] = fran_points.tolist()


def add_elo_columns(df):
    """ Add columns to dataframe, containing the elo ratings of the home team
        and away team at the current time of each game.  Gets elo scores out
        of the pickled elo_dict.p, so be sure it is up to date (trained on most
        recent data).

    :param df:  The dataframe to be added to
    """
    # Get elo dictionary
    elodict = pickle.load(open('../elo_dict.p', 'rb'))

    # Add columns to dataframe
    df['fran_elo'] = np.zeros(len(df))
    df['opp_elo'] = np.zeros(len(df))

    # Add elo rating for each team for each game
    for team in elodict.keys():
        # Find all games with this team and get indices where home and where away
        games = df[(df['fran_id'] == team) | (df['opp_fran'] == team)]
        home_actual_inds = games[(games['fran_id'] == team)].index
        away_actual_inds = games[(games['opp_fran'] == team)].index

        # Reindex from 0 to n
        games.index = range(len(games))
        home_elo_inds = games[(games['fran_id'] == team)].index
        away_elo_inds = games[(games['opp_fran'] == team)].index

        # Get the elo scores for each home and away game
        away_elos = np.array(elodict[team])[away_elo_inds]
        home_elos = np.array(elodict[team])[home_elo_inds]

        # Add this team's elo ratings to df
        df.ix[home_actual_inds, 'fran_elo'] = home_elos
        df.ix[away_actual_inds, 'opp_elo'] = away_elos


if __name__ == "__main__":
    # Read in data
    filename = 'data/all_games.csv'
    df = pd.read_csv(filename)
    teams = df['fran_id'].unique()
    
    # Add new columns here
    colToAdd = ['pts','opp_pts']
    for col in colToAdd:
        RollingAvg(df,teams,col,5)
    
    # Save final dataframe
    print df
    