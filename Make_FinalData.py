import numpy as np
import pandas as pd



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
    