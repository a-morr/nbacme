import numpy as np
import pandas as pd
import pickle


def RollingAvg(df,teams,column,window):
    """ Calculates the rolling average of a column for both teams.
    
    :param df:  The dataframe to be added to
    :param teams:  A list of all the teams
    :param column:  Basketball statistic to average (i.e. points)
    :param window:  Number of games to use for the average
    """
    
    # Column names for new variables
    new_colA = 'RollAvg_A_'+str(window)+'_'+column
    new_colB = 'RollAvg_B_'+str(window)+'_'+column
    new_col_oppA = 'RollAvg_A_'+str(window)+'_opp_'+column
    new_col_oppB = 'RollAvg_B_'+str(window)+'_opp_'+column
    
    # Default value is NAN
    df[new_colA] = np.nan
    df[new_colB] = np.nan
    df[new_col_oppA] = np.nan
    df[new_col_oppB] = np.nan
    for team in teams:
        # Indices of the games for this team
        fran_indices = df[(df['fran_id']==team)].index
        opp_indices = df[(df['opp_fran']==team)].index
        
        # Get the statistic that will be averaged
        fran_stats = df[(df['fran_id']==team)][column]
        opp_stats = df[(df['opp_fran']==team)]['opp_'+column]
        
        # Order and calculate moving average
        stats = fran_stats.append(opp_stats)
        stats.sort_index(inplace = True)
        stats = pd.rolling_mean(stats,window)
        
        # Add the information to the columns
        df.ix[fran_indices,new_colA] = stats[fran_indices].tolist()
        df.ix[opp_indices,new_colB] = stats[opp_indices].tolist()
        
        # Get the statistic that will be averaged for the opposing team
        fran_stats = df[(df['fran_id']==team)]['opp_'+column]
        opp_stats = df[(df['opp_fran']==team)][column]
        
        # Order and calculate moving average for the opposing team
        stats = fran_stats.append(opp_stats)
        stats.sort_index(inplace = True)
        stats = pd.rolling_mean(stats,window)
        
        # Add the information to the columns
        df.ix[fran_indices,new_col_oppA] = stats[fran_indices].tolist()
        df.ix[opp_indices,new_col_oppB] = stats[opp_indices].tolist()

def add_elo_columns(df):
    """ Add columns to dataframe, containing the elo ratings of the home team
        and away team at the current time of each game.  Gets elo scores out
        of the pickled elo_dict.p, so be sure it is up to date (trained on most
        recent data).

    :param df:  The dataframe to be added to
    """
    # Get elo dictionary
    elodict = pickle.load(open('elo_dict.p', 'rb'))

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
    
def days_between_games(df,teams):
    """ Adds the days since the last game for each team used to measure
        fatigue of players.
    
    :param df:  The dataframe to be added to
    :param teams:  A list of all the teams
    """
    df['Days_Since_Last'] = np.nan
    for team in teams:
        df['date'] = pd.to_datetime(df['date'])
        
        team_df = df[(df['fran_id']==team) | (df['opp_fran']==team)]
        teamTime = (team_df['date'] - team_df['date'].shift(1))
        days =  teamTime.iloc[1:].map(lambda x: x.days if x.days<=10 else 10)
        
        fran_indices = team_df.index[1:]
        df.ix[fran_indices,'Days_Since_Last'] = days.tolist()

def who_wins(df):
    """ Adds the Win column. If Win is true then team A (away team) won
        the game.
    
    :param df:  The dataframe to be added to
    """
    df['Win'] = df['pts']>df['opp_pts']


if __name__ == "__main__":
    # Read in data
    filename = 'data/all_games.csv'
    df = pd.read_csv(filename)
    teams = df['fran_id'].unique()
    
    
    # Add new columns here
    colToAdd = ['pts']
    for col in colToAdd:
        RollingAvg(df,teams,col,5)
    
    add_elo_columns(df)
    
    days_between_games(df,teams)
    who_wins(df)
    
    # Save final dataframe
    df.to_csv('Algorithms_Data.csv')
    #print df