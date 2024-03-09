import json
from openai import OpenAI
client = OpenAI(api_key="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")

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

def generate_campaign_post(project_title, project_description, product_url, campaign_goal,hashtags):
    prompt = f"Generate a social campaign post for the project:\n\nTitle: {project_title}\n\nDescription: {project_description}\n\nCampaign Goal: {campaign_goal}\n\n give content and hashtags in separate fields in  Json"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "It will generate social content"},
            {"role": "user", "content": prompt}
        ]
        )
   
    generated_content = completion.choices[0].message.content
    return generated_content



# Example project details
project_title = "IFO"
project_description = "IFO products give space to engage people in New AI products community."

# Generate hashtags using OpenAI
api_response = generate_hashtags(project_title, project_description)

product_url = "https://ifo.ai"
campaign_goal = "Help us Kickstart AI Startups with the Power of Community and Crypto"

# Generate campaign-style Twitter post using OpenAI
campaign_post_content = generate_campaign_post(project_title, project_description, product_url, campaign_goal,api_response)

print(api_response)
print(campaign_post_content)