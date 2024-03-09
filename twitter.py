import tweepy
from dotenv import dotenv_values

config = dotenv_values(".env")

consumer_key = config['CONSUMER_KEY']
consumer_secret = config['CONSUMER_SECRET']
access_token = config['ACCESS_TOKEN']
access_token_secret = config['ACCESS_TOKEN_SECRET']
bearer_token = config['BEARER_TOKEN']


auth = tweepy.OAuth2BearerHandler(bearer_token)
api = tweepy.API(auth)

 
tweet = "Another day, another #scifi #book and a cup of #coffee"
status = api.update_status(status=tweet)