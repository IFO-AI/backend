from transformers import pipeline, GPTNeoForCausalLM, GPT2Tokenizer
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

gpt_model_name = "EleutherAI/gpt-neo-2.7B"

def generate_hashtags_gpt_neo(project_title, project_description, num_hashtags=2):
    # Load GPT-Neo model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained(gpt_model_name)
    model = GPTNeoForCausalLM.from_pretrained(gpt_model_name)

    # Generate hashtags
    input_text = f"Create hashtags for the project: {project_title}\n\nDescription: {project_description}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=1024)

    # Generate text using the model
    output_ids = model.generate(input_ids, max_length=50, num_beams=5, length_penalty=2.0, early_stopping=True)
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Extract hashtags from the generated text
    hashtags = [tag.strip() for tag in generated_text.split("#") if tag.strip()]

    # Return the specified number of hashtags
    return hashtags[:num_hashtags]





# # Example project title
# project_title = "IFO Offering"

# # Generate two hashtags based on the project title using GPT-Neo
# generated_hashtags_gpt_neo = generate_hashtags_gpt_neo(project_title, num_hashtags=2)

# # Print the generated hashtags using GPT-Neo
# print("Generated Hashtags using GPT-Neo:")
# for i, hashtag in enumerate(generated_hashtags_gpt_neo, start=1):
#     print(f"{i}. #{hashtag}")











# from openai import OpenAI
# from api.helper.environment import Config
# client = OpenAI(
#   api_key= Config.get("OPENAI_API_KEY"),
# )

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)