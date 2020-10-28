import os
import tweepy
import requests


consumer_key = os.environ.get('twitter_consumer_key')
consumer_secret = os.environ.get('twitter_consumer_secret')
access_token = os.environ.get('twitter_access_token')
access_token_secret = os.environ.get('twitter_access_token_secret')

# Authenticate
def OAuth():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    except Exception as e:
        print("ERROR: Failed to get access token")
        return None
    

# Tweet
def tweet_message(message):
    oauth = OAuth()
    api = tweepy.API(oauth)

    try:
        api.update_status(status=message)
        print()
    except Exception as e:
        print("ERROR: Failed to post status:\n" + str(e))
