import json
from openai import OpenAI
from api.helper.environment import Config
# from environment import Config

client = OpenAI(api_key= Config.get('OPENAI_API_KEY'))

import random

items = ['🔥 Visit', '🤖 Check it out at', '💡 Discover more at', '🌐 Check out our website at', '🌐 Explore more at', '🌐 Check out more at']


def generate_hashtags(project_title, project_description):
    prompt = f"Create 1 unique hashtag related with project based on the project:\n\nTitle: {project_title}\n and Description: {project_description}\n"
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "It will generate to hashtags"},
            {"role": "user", "content": prompt}
        ]
    )
   
    # Extract the generated hashtags from the API response
    generated_hashtags = completion.choices[0].message
    
    return generated_hashtags.content

def generate_campaign_post(project_title, project_description, product_url, campaign_goal, hashtags):
    prompt = f"Generate a social campaign post within 400 character for the project:\n\nTitle: {project_title}\n\nDescription: {project_description}\n\nCampaign Goal: {campaign_goal}\n\n"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "It will generate social content"},
            {"role": "user", "content": prompt}
        ]
        )
    
    generated_content = completion.choices[0].message.content
    data = generated_content.split("#",1)
    selected_item = random.choice(items)
    message = data[0]+ "\n"+ selected_item + " "+product_url + "\n"+ hashtags
    new_tags = "#" + data[1] # Will be used later if required
    return message


def generate_comment_post(project_description, comment):
    prompt = f"Project Description: {project_description}\n\nI received the following comment in response to my post: '{comment}'. What would be my ideal and engaging reply to foster a positive and insightful conversation? Also give the sentiment analysis by sentiment and reply_content in json fields"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "It will generate social content"},
            {"role": "user", "content": prompt}
        ]
        )
    
    generated_content = completion.choices[0].message.content
    content_details = json.loads(generated_content)
    reply_content = content_details["reply_content"]
    sentiment = content_details["sentiment"]
    return reply_content, sentiment


# # Example project details
# project_title = "IFO"
# project_description = "IFO products give space to engage people in New AI products community."

# # Generate hashtags using OpenAI
# api_response = generate_hashtags(project_title, project_description)

# product_url = "https://ifo.ai"
# campaign_goal = "Help us Kickstart AI Startups with the Power of Community and Crypto"

# # Generate campaign-style Twitter post using OpenAI
# campaign_post_content = generate_campaign_post(project_title, project_description, product_url, campaign_goal,api_response)

# print(api_response)
# print(campaign_post_content)


# project_description = "IFO products give space to engage people in New AI products community."

# comment_post, d = generate_comment_post(project_description, "This product is really good")
# print(comment_post)
# print(d)