'''
LAYMAN SUMMARY GENERATOR for Abstracts of research papers

This script makes layman summaries from scientific abstracts using a Large Language Model from OpenAI ChatGPT.
As input we use the API from OpenAIRE to get content from the Netherlands Research Portal: https://netherlands.openaire.eu
Assistance in code development and debugging was provided by the code interpretation functionality of OpenAI's GPT-4 model.
Authors: Maurice Vanderfeesten and OpenAI's GPT-4 model
License: CC0
'''

import requests
import openai
import pandas as pd
import json
import time
import openai.error
import os
import yaml 
from datetime import datetime

''' 
# Load OpenAI API key and other configuration from a JSON configuration file
def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config
'''

# Load OpenAI API key and other configuration from a YAML configuration file
def load_config():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config

# Fetch data from the OpenAIRE API
def fetch_data(data_url):
    response = requests.get(data_url)
    return response.json()

# Extract necessary information from each "result" in the data
def extract_info(result):
    identifier = result['header']['dri:objIdentifier']['$']
    originalId = extract_key_info(result, 'originalId')
    title = extract_key_info(result, 'title')
    description = extract_key_info(result, 'description')

    return identifier, originalId, title, description

# Extract information from given key if it exists
def extract_key_info(result, key):
    if key in result['metadata']['oaf:entity']['oaf:result']:
        try: 
            info = result['metadata']['oaf:entity']['oaf:result'][key][0]['$']
        except:
            info = result['metadata']['oaf:entity']['oaf:result'][key]['$']
    else:
        info = None  # Or any default value of your choice
    return info

# Define a  function to handle API calls from OpenAI with retry logic
def create_chat_completion_with_retry(prompt, aimodel, max_tokens, retries=3, delay=5):
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(model=aimodel, messages=prompt, max_tokens=max_tokens)
            return response
        except openai.error.APIError as e:
            if e.status == 502 and i < retries - 1:  # Retry on 502 error
                time.sleep(delay)  # Wait for a bit before retrying
                continue
            else:
                raise e  # If it's not a 502 error or we've run out of retries, re-raise the exception

# Generate a layman summary using OpenAI
def generate_summary(description, aimodel, max_tokens, audience_name, audience_message):
    if description is None:
        return None
    # Make for each audience a different system message
    system_message = "You are a helpful assistant. " + audience_message

    # Instruct what to do with the abstract for a specific audience
    user_message = f'Summarize this text for a {audience_name}: {description}'

    prompt = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    # Use the retry function instead of directly calling `openai.ChatCompletion.create`
    response = create_chat_completion_with_retry(prompt, aimodel, max_tokens)
    
    # Get generated text from each response
    generated_text = response['choices'][0]['message']['content'].strip()
    
    # Truncate the text to end with a complete sentence
    truncated_text = truncate_text(generated_text, max_tokens-20)

    # Return the truncated response
    return truncated_text

# Truncate the text to the last complete sentence that fits within max_tokens.
def truncate_text(text, max_tokens):
    tokenized_text = text.split()  # split the text into words
    if len(tokenized_text) > max_tokens:
        # find the last period within max_tokens
        last_period = ' '.join(tokenized_text[:max_tokens]).rfind('.')
        # truncate to the last complete sentence
        tokenized_text = tokenized_text[:last_period+1]
    return ' '.join(tokenized_text)

# Save DataFrame to CSV and Excel files
def save_df(df, aimodel):
    num_records = len(df)

    if not os.path.exists('results'):
        os.makedirs('results')

    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d_%H%M")

    csv_file_name = f"results_{num_records}_{aimodel}_{formatted_date}.csv"
    xlsx_file_name = f"results_{num_records}_{aimodel}_{formatted_date}.xlsx"

    csv_file_path = os.path.join('results', csv_file_name)
    xlsx_file_path = os.path.join('results', xlsx_file_name)

    df.to_csv(csv_file_path, index=False)
    df.to_excel(xlsx_file_path, index=False)

# Main function to orchestrate the operations
def main(config):
    # Get the variables from the config
    openai.api_key = config['openai_api_key']
    aimodel = config['aimodel']
    max_tokens = config['max_tokens']
    data_url = config['data_url']
    audiences = config['audiences']

    # Get the input data
    data = fetch_data(data_url)
    results = []

    # Extract metadata fields for each of the records from the input data
    for result in data['response']['results']['result']:
        identifier, originalId, title, description = extract_info(result)
        
        result_dict = {
            'objIdentifier': identifier,
            'originalId': originalId,
            'title': title,
            'description': description
        }
        
        # Generate layman summaries for each of the defined audiences from the abstract of the paper
        for audience in audiences:
            layman_summary = generate_summary(description, aimodel, max_tokens, audience['name'], audience['message'])
            result_dict[f'layman_summary_{audience["name"].lower()}'] = layman_summary

        results.append(result_dict)

    # Create a DataFrame from the results
    df = pd.DataFrame(results)
    
    # Save the data of this session as an excel and csv file in the results folder
    save_df(df, aimodel)
    
    # Return the DataFrame
    return df