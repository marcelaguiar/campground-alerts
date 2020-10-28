import os
import tweepy


consumer_key = os.environ.get('twitter_consumer_key')
consumer_secret = os.environ.get('twitter_consumer_secret')
access_token = os.environ.get('twitter_access_token')
access_token_secret = os.environ.get('twitter_access_token_secret')

#Tweet module
def OAuth():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    except Exception as e:
        return None


def tweet_message(message):
    oauth = OAuth()
    api = tweepy.API(oauth)

    api.update_status('Test Tweet')

    print(message)
