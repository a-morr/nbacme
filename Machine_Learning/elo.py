""" This module provides a basic implementation of Arpad Elo's
    ranking algorithm for two-player games.

    See https://en.wikipedia.org/wiki/Elo_rating_system

"""


# TODO Identify the optimum k value, or hierarchy of k values
k = 20


def predict_score(ra, rb):
    """ Compute the expected score for two players based on their current elo ratings.

        :param ra:  The rating for player A
        :param rb:  The rating for player B
        :returns:   Tuple, the expected score of player A and of player B
    """

    ea = 1. / (1 + 10 ** ((rb - ra) / 400.))
    eb = 1 - ea
    return ea, eb


def update_elo_ratings(ra, rb, a_score, b_score):
    """ Update the elo ratings of two players based on an actual or predicted outcome.

    :param ra:      The rating of player A
    :param rb:      The rating of player B
    :param a_score: The score of player A
    :param b_score: The score of player B
    :return:        Tuple, the updated ratings of player A and of player B
    """

    ea, eb = predict_score(ra, rb)
    ra += k * (a_score - ea)
    rb += k * (b_score - eb)

    return ra, rb


def train(data):
    """
    """
    # Initialize score
    teams = np.unique(data['fran_id'])
    team_elo = dict(zip(teams,[1500]*len(teams)))
    for i in range(len(data)):
        row = data.iloc[i]
        RA = team_elo[row['fran_id']]
        RB = team_elo[row['opp_fran']]
        team_elo[row['fran_id']], team_elo[row['opp_fran']] = update_elo_ratings(RA,RB,row['pts']>row['opp_pts'],row['pts']<row['opp_pts'])
    return team_elo