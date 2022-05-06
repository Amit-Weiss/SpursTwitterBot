"""
Main file for the Twitter bot, containing all logic and constants.
"""
from os import environ
import time

from datetime import date
from dateutil.relativedelta import relativedelta


import tweepy

# from creds import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
API_KEY = environ["API_KEY"]
API_SECRET = environ["API_SECRET"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]
ACCESS_SECRET = environ["ACCESS_SECRET"]

LAST_CHAMPIONSHIP = date(1961, 4, 29)
LAST_FA_CUP = date(1991, 5, 18)
LAST_LEAGUE_CUP = date(2008, 2, 24)
LAST_UEFA_CUP = date(1984, 5, 23)
LATEST_TROPHY = max(
    LAST_CHAMPIONSHIP, LAST_FA_CUP, LAST_LEAGUE_CUP, LAST_UEFA_CUP
)


def auth_and_get_api():
    """
    Authenticate to twitter using the credentials stored as env variables.
    """
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    return auth, tweepy.API(auth)


def tweet_days_passed(api, spurs_event=LATEST_TROPHY):
    """
    Calculate the days since the last event and post an update (a tweet).
    """
    days_delta = (date.today() - spurs_event).days
    dates_delta = relativedelta(date.today(), spurs_event)

    try:
        api.update_status(
            f"{days_delta}\n"
            f"({dates_delta.years} years, {dates_delta.months} months and"
            f" {dates_delta.days} days)\n"
        )
    except tweepy.TweepError as err:
        print(f"Tweepy raised an exception we ignore: {err}")


def check_followers(api):
    """
    Maintain the "you follow me I follow you" policy.
    """
    my_id = api.me().id
    my_followers = api.followers_ids(my_id)
    my_friends = api.friends_ids(my_id)

    to_follow = [u for u in my_followers if u not in my_friends]
    to_unfollow = [u for u in my_friends if u not in my_followers]

    for user in to_follow:
        api.create_friendship(user)
        api.send_direct_message(
            user,
            "Hello new friend!\n"
            "I'm a bot posting daily how many days passed since Spurs won a trophy.\n"
            "If you have any suggestions for things I should do, please send them here!",
        )
    for user in to_unfollow:
        api.destroy_friendship(user)


if __name__ == "__main__":
    POSTING_INTERVAL = 60 * 60 * 24  # Daily

    while True:
        print("Performing the daily tasks...")
        auth, twitter_api = auth_and_get_api()

        tweet_days_passed(twitter_api, LATEST_TROPHY)
        check_followers(twitter_api)

        time.sleep(POSTING_INTERVAL)
