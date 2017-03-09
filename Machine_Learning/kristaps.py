import elo
import numpy as np
import pandas as pd
import datetime as dt

class Kristaps(object):
    """

    """

    def __init__(self):
        self.elo_dict = dict()


    def train(self, data, init=True):
        """ Calculates the current Elo rating for each of the teams.

        :param data:    Pandas dataframe with each row being a game.  Columns include 'fran_id',
                        'opp_fran', 'pts', and 'opp_pts'
        :return:        Update the self.elo_dict where the team names are the keys and the elo
                        ratings are the values.
        """
        # Initialize score
        if init:
            teams = np.unique(data['fran_id'])
            self.elo_dict = dict(zip(teams, [1500] * len(teams)))
        data.sort_values('date',inplace=True)
        for i in range(len(data)):
            row = data.iloc[i]
            RA = self.elo_dict[row['fran_id']]
            RB = self.elo_dict[row['opp_fran']]
            self.elo_dict[row['fran_id']], self.elo_dict[row['opp_fran']] = elo.update_elo_ratings(RA, RB, row['pts'] > row['opp_pts'],
                                                                                     row['pts'] < row['opp_pts'])


    def simulate_games(self, future_games, n):
        """

        :param future_games:
        :param n:
        :return:
        """

        game_scores = np.zeros(len(future_games))

        for it in range(n):
            tmp_elo_dict = self.elo_dict.copy()
            for i in range(len(future_games)):
                game = future_games.iloc[i]
                A = game['fran_id']
                B = game['opp_fran']

                rA = tmp_elo_dict[A]
                rB = tmp_elo_dict[B]

                pA, pB = elo.predict_score(rA, rB)
                winner = np.random.choice([A, B], p=[pA, pB])

                A_score = 1 if winner == A else 0
                B_score = A_score - 1
                game_scores[i] += A_score

                # TODO Should we update elo ratings as we go?
                # rA, rB = elo.update_elo_ratings(rA, rB, A_score, B_score)
                # tmp_elo_dict[A] = rA
                # tmp_elo_dict[B] = rB

        A_probs = game_scores / float(n)

        return A_probs, 1 - A_probs


    def check(self, Aprobs, Bprobs, info):
        """ Compare given predictions for a series of games against a real outcome.

        :param Aprobs:  Probability of the Away team winning each game
        :param Bprobs:  Probability of the Home team winning each game
        :param info:    A pandas dataframe with game outcome information
        :return:
        """
        correct = 0.
        for i in range(len(Aprobs)):
            truth = np.argmax([info.iloc[i]['pts'], info.iloc[i]['opp_pts']])
            pred = np.argmax([Aprobs[i], Bprobs[i]])
            correct += (truth == pred)

        return correct / len(Aprobs)


    def predict_today(self, filename='../data/upcoming_games.csv'):
        """  Predict today's games, as pulled from the upcoming_games file.
             Saves predictions to csv as tomorrow.csv for use on website.

        :param filename:    Input file with future games.  Defaults to 'upcoming_games.csv'
        :return:            A pandas dataframe containing the probability of each team winning each game
        """
        df = pd.read_csv(filename)
        today = dt.datetime.today()
        df = df[(df['date'] == str(today.date()))]

        preds = []
        for i in range(len(df)):
            elo_A = self.elo_dict[df.iloc[i]['fran_id']]
            elo_B = self.elo_dict[df.iloc[i]['opp_fran']]

            sc = elo.predict_score(elo_A - 46, elo_B + 46)
            preds.append([df.iloc[i]['fran_id'], df.iloc[i]['opp_fran'], sc[0], sc[1]])

        table = pd.DataFrame(preds, columns=['fran_id', 'opp_fran', 'prob', 'opp_prob'])
        table.to_csv('../data/tomorrow.csv', index=None)

        return table
            
    def current_WL(self,filename='../data/historical_data.csv'):
        """ Count the current number of wins and losses for all teams in the 2016-2017 season.
            Returns a dictionary with the team names as the keys and [wins,losses] as the values.

        :param filename:    Input file with games of the current season.  Defaults to 'historical_data.csv'
        :return:            A dictionary with team names as the keys and a list [wins,losses] as the values.
        """
        data = pd.read_csv(filename)
        data['date'] = pd.to_datetime(data['date'])
        teams = np.unique(data['fran_id'])
        team_WL = {}
        data['Won'] = (data['pts'] > data['opp_pts'])
        for team in teams:
            won = data[(data['fran_id'] == team) & (data['date'] >= dt.datetime(2016, 9, 1))]['Won'].sum()
            won += (data[(data['opp_fran'] == team) & (data['date'] >= dt.datetime(2016, 9, 1))]['Won'] == False).sum()
            lost = (data[(data['fran_id'] == team) & (data['date'] >= dt.datetime(2016, 9, 1))]['Won'] == False).sum()
            lost += (data[(data['opp_fran'] == team) & (data['date'] >= dt.datetime(2016, 9, 1))]['Won'] == True).sum()
            team_WL[team] = [won, lost]
        return team_WL
        
    def simulate_seasons(self,filename='../data/upcoming_games.csv', n=100):
        """ This simulates the rest of 2016-2017 season n times.  This function assumes
            that train has been run as it uses self.elo_dict.  Elo scores are not updated
            during the simulated season.  This will also calculate the current wins and 
            losses through current_WL().  A pandas dataframe will be saved and returned.

        :param filename:    Input file with future games.  Defaults to 'upcoming_games.csv'
        :param n:           Number of times the 2016-2017 season will be simulated.  Defaults to 100
        :return:            Pandas dataframe with columns as Team name, Projected Wins, Projected Losses, and Elo rating
        """
        future_games = pd.read_csv(filename)
        teams = np.unique(future_games['fran_id'])
        team_WL_Predicted = dict(zip(teams, np.zeros((len(teams),2))))
        for it in range(n):
            for i in range(len(future_games)):
                game = future_games.iloc[i]
                A = game['fran_id']
                B = game['opp_fran']
            
                rA = self.elo_dict[A]
                rB = self.elo_dict[B]
            
                pA, pB = elo.predict_score(rA, rB)
                winner = np.random.choice([A, B], p=[pA, pB])
            
                A_score = 1 if winner == A else 0
                B_score = 1 - A_score
                team_WL_Predicted[A][0] += A_score
                team_WL_Predicted[A][1] += B_score
            
                team_WL_Predicted[B][0] += B_score
                team_WL_Predicted[B][1] += A_score
            
        for team in teams:
            team_WL_Predicted[team] = np.round(team_WL_Predicted[team]/float(n))
        team_WL = self.current_WL()
        total_WL = {}
        for team in teams:
            total_WL[team] = team_WL_Predicted[team]+team_WL[team]
        Projected_WL = pd.DataFrame({'fran_id':teams,'Projected W':[total_WL[team][0] for team in teams],'Projected L':[total_WL[team][1] for team in teams],'elo':[self.elo_dict[team] for team in teams]})
        table = Projected_WL.sort_values('elo',ascending=False)
        table.to_csv('../data/ProjectedWL.csv',index = False)
        return table


