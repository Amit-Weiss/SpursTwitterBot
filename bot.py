import tweepy
from datetime import date
from dateutil.relativedelta import relativedelta
from os import environ
import time

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


def tweet_days_passed(api, spurs_event=LATEST_TROPHY):
    days_delta = (date.today() - spurs_event).days
    dates_delta = relativedelta(date.today(), spurs_event)

    try:
        api.update_status(f'{days_delta}\n'
                          f'({dates_delta.years} years, {dates_delta.months} months and {dates_delta.days} days)\n')
    except tweepy.TweepError as e:
        print(f'Tweepy raised an exception we ignore: {e}')
        pass


# Maintains the "you follow me I follow you" policy
def check_followers(api):
    my_id = api.me().id
    my_followers = api.followers_ids(my_id)
    my_friends = api.friends_ids(my_id)

    to_follow = [u for u in my_followers if u not in my_friends]
    to_unfollow = [u for u in my_friends if u not in my_followers]

    for u in to_follow:
        api.create_friendship(u)
        api.send_direct_message(u, f"Hello new friend!\n"
                                "I'm a bot posting daily how many days passed since Spurs won a trophy.\n"
                                "If you have any suggestions for things I should do, please send them here!")
    for u in to_unfollow:
        api.destroy_friendship(u)


if __name__ == '__main__':
    posting_interval = 60 * 60 * 24  # Daily

    while True:
        print('Performing the daily tasks...')
        auth, twitter_api = auth_and_get_api()

        tweet_days_passed(twitter_api, LATEST_TROPHY)
        check_followers(twitter_api)

        time.sleep(posting_interval)