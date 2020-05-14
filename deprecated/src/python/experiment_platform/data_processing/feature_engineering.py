"""
Collection of functions to create new features
"""
import numpy as np


def friends_followers_ratio(friends, followers):
    """
    Function for getting the normalized friends to followers ratio, as specified in:
    Wang, Haining. "Detecting Automation of Twitter Accounts: Are You a Human, Bot or Cyborg?"
    IEEE Transactions on Dependable and Secure Computing. November 2012.

    Args:
        friends - 1xN numpy array of friend counts
        followers - 1xN numpy array of follower counts

    Returns:
        1xN numpy array containing friends to followers ratios
    """

    # Zero division handling adapted from DStauffman's solution at:
    # https://stackoverflow.com/a/37977222
    result = np.divide(
        followers,
        (friends + followers),
        out=np.zeros(followers.shape, dtype=float),
        where=(friends + followers) != 0,
    )
    return result


def account_age(account_createdat, tweet_createdat):
    """
    Function for getting the account age

    Args:
        account_createdat - 1xN numpy array of account creation dates in pandas datetime format

        tweet_createdat - 1xN numpy array of tweet creation dates in pandas datetime format

    Returns:
        1xN numpy array containing the account age in seconds
    """
    # Find the age by taking difference of tweet and acc creation dates
    diff = tweet_createdat - account_createdat
    return diff.dt.total_seconds()


# Dictionary mapping "New feature name" => (feature_function, [input column names])
ALL_FEATURES = {
    "account_rep": (friends_followers_ratio, ["friendscount", "followerscount"]),
    "account_age": (account_age, ["user_createdat", "tweet_createdat"]),
    "friends_growth": (np.divide, ["friendscount", "account_age"]),
    "followers_growth": (np.divide, ["followerscount", "account_age"]),
}
