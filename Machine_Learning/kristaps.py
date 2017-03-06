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
        """

        :param data:
        :return:
        """
        # Initialize score
        if init:
            teams = np.unique(data['fran_id'])
            self.elo_dict = dict(zip(teams, [1500] * len(teams)))

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
        df = df[(df['month'] == today.month) & (df['day'] == today.day) & (df['year'] == today.year)]

        preds = []
        for i in range(len(df)):
            elo_A = self.elo_dict[df.iloc[i]['fran_id']]
            elo_B = self.elo_dict[df.iloc[i]['opp_fran']]

            sc = elo.predict_score(elo_A - 46, elo_B + 46)
            preds.append([df.iloc[i]['fran_id'], df.iloc[i]['opp_fran'], sc[0], sc[1]])

        table = pd.DataFrame(preds, columns=['fran_id', 'opp_fran', 'prob', 'opp_prob'])
        table.to_csv('../data/tomorrow.csv', index=None)

        return table

