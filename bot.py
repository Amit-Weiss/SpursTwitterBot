import tweepy
from datetime import date
from os import environ

# from creds import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
API_KEY = environ['API_KEY']
API_SECRET = environ['API_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_SECRET = environ['ACCESS_SECRET']

LAST_CHAMPIONSHIP = date(1961, 4, 29)
LAST_FA_CUP = date(1991, 5, 18)
LAST_LEAGUE_CUP = date(2008, 2, 24)
LAST_UEFA_CUP = date(1984, 5, 23)
LATEST_TROPHY = max(LAST_CHAMPIONSHIP, LAST_FA_CUP, LAST_LEAGUE_CUP, LAST_UEFA_CUP)


def auth_and_get_api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    return auth, tweepy.API(auth)


def tweet_days_passed(api):
    dates_delta = date.today() - LATEST_TROPHY

    api.update_status(f'{dates_delta.days} Days since Spurs last won a trophy')


def check_followers(api):
    my_followers = api.followers()
    my_friends = api.friends_ids()

    to_follow = [u.id for u in my_followers if u not in my_friends]
    to_unfollow = [u for u in my_friends if u not in my_followers]

    for u in to_follow:
        api.create_friendship(u)
    for u in to_unfollow:
        api.destroy_friendship(u)


if __name__ == '__main__':
    auth, twitter_api = auth_and_get_api()

    # tweet_days_passed(twitter_api)
    check_followers(twitter_api)