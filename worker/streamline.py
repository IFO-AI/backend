from mastodon import Mastodon, StreamListener
from environment import Config
import logging
from bs4 import BeautifulSoup
import re
import requests
import json

api_endpoint = "http://127.0.0.1:5000/api/comment"

client_id = Config.get('MASTODON_CLIENT_ID')
client_secret = Config.get('MASTODON_CLIENT_SECRET')
api_base_url = Config.get('MASTODON_API_BASE_URI')
access_token = Config.get('MASTODON_ACCESS_TOKEN')

mastodon = Mastodon(client_id = client_id, client_secret=client_secret, api_base_url=api_base_url, access_token=access_token)

def extract_comments_message(message):
    try:
        soup = BeautifulSoup(message.status.content, 'html.parser')
        text_content = soup.get_text()
        cleaned_content = re.sub(r'@\w+', '', text_content)
        data = {
            "account_id": message.account.id,
            "username": message['account']['acct'],
            "comment_id": message.status.id,
            "content": cleaned_content,
            "full_content": text_content,
            "parent_id": message.status.in_reply_to_id
        }
        print(data)
        return data
    except Exception as e:
        print("Comment extraction error", e) 
        return None   
        

class UserListener(StreamListener):
    def on_update(self, message):
        print(message)
        # print(f"New message from {message['account']['acct']}:\n{message['content']}")
        
    def on_notification(self, message):
        print(message)
        comment = extract_comments_message(message)
        print(comment)
        print("parent_id")
        print(comment["parent_id"])
        if comment is not None and comment["parent_id"]:
            response = requests.post(api_endpoint, json=comment)
            print(response)

def mastodon_stream_user():
    try:
        listener = UserListener()
        # mastodon.stream_hashtag(hashtag,listener=listener)
        mastodon.stream_user(listener=listener)
    except Exception as e:  
       print("Error", e)
    

mastodon_stream_user()


