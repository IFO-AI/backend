from mastodon import Mastodon
from api.helper.environment import Config
import logging


client_id = Config.get('MASTODON_CLIENT_ID')
client_secret = Config.get('MASTODON_CLIENT_SECRET')
api_base_url = Config.get('MASTODON_API_BASE_URI')
access_token = Config.get('MASTODON_ACCESS_TOKEN')


mastodon = Mastodon(client_id = client_id, client_secret=client_secret, api_base_url=api_base_url, access_token=access_token)

def generate_mastodon_post(description, keyword, url):
    # Generate content using a transformer model
    generator = pipeline('text-generation', model=gpt_model_name)
    generated_text = generator(description, max_length=100, num_return_sequences=1)[0]['generated_text']
    
    # Create Twitter post content
    mastodon_post = f"{generated_text}\n\n🔍 Keyword: {keyword}\n🌐 URL: {url}"
    
    return mastodon_post

def create_mastodon_post(message):
    try:
        response = mastodon.toot(message)
        return response
    except Exception as e:
        error_message = f"Error posting to Mastodon: {e}"
        logging.error(error_message)
        return None

def create_mastodon_comment(reply_content, comment_id):
    try:
        response =  mastodon.status_post(reply_content, in_reply_to_id=comment_id, visibility='direct')
        return response
    except Exception as e:
        error_message = f"Error commenting to Mastodon: {e}"
        logging.error(error_message)
        return None

def mastodon_status(id):
    resp = mastodon.status(id)
    return resp

