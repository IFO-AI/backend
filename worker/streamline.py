from mastodon import Mastodon, StreamListener
from environment import Config
import logging


client_id = Config.get('MASTODON_CLIENT_ID')
client_secret = Config.get('MASTODON_CLIENT_SECRET')
api_base_url = Config.get('MASTODON_API_BASE_URI')
access_token = Config.get('MASTODON_ACCESS_TOKEN')


mastodon = Mastodon(client_id = client_id, client_secret=client_secret, api_base_url=api_base_url, access_token=access_token)
class HashTagListener(StreamListener):
    def on_update(self, status):
        print(f"New status from {status['account']['acct']}:\n{status['content']}")
        
def mastodon_stream_hashtag(hashtag):
    try:
        listener = HashTagListener()
        mastodon.stream_hashtag(hashtag,listener=listener)
    except Exception as e:  
       print("Error", e)
    

mastodon_stream_hashtag("ifo")