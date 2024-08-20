import requests
from dotenv import load_dotenv
import os
import csv

env_path = os.path.join('..', '.env')

load_dotenv(env_path)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

# Authenticate using application-only OAuth2
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

data = {
    'grant_type': 'client_credentials'
}

headers = {'User-Agent': user_agent}

# Request the access token
response = requests.post('https://www.reddit.com/api/v1/access_token',
                         auth=auth, data=data, headers=headers)
response.raise_for_status()  # Ensure the request was successful

# Get the access token from the response
token = response.json().get('access_token')

# Update the headers with the access token
headers['Authorization'] = f'bearer {token}'

# File path setup
output_folder = os.path.join('..', 'data')
os.makedirs(output_folder, exist_ok=True)  # Create the 'data' directory if it doesn't exist
output_file = os.path.join(output_folder, 'comments2.csv')

# CSV file setup
fieldnames = ['Id', 'Username', 'Subreddit', 'Comment']
if not os.path.exists(output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

# Parameters
num_comments_to_fetch = 100  # Number of comments to fetch per request
max_comments = 1000000  # Maximum number of comments to fetch in total
current_id = 1

# Fetch comments in a loop until the limit is reached
while current_id <= max_comments:
    # Fetch a batch of comments
    comments_url = 'https://oauth.reddit.com/comments'
    comments_response = requests.get(comments_url, headers=headers, params={'limit': num_comments_to_fetch})
    comments_data = comments_response.json()

    # Check if there are comments to process
    if comments_data and 'data' in comments_data:
        comments_list = comments_data['data']['children']
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for comment in comments_list:
                if current_id > max_comments:
                    break  # Stop if we've reached the maximum number of comments
                comment_body = comment['data']['body']
                comment_author = comment['data']['author']
                comment_subreddit = comment['data']['subreddit']
                
                # Write the comment to the CSV file
                writer.writerow({
                    'Id': current_id,
                    'Username': comment_author,
                    'Subreddit': comment_subreddit,
                    'Comment': comment_body
                })
                print(f"Comment {current_id} saved: {comment_author} in {comment_subreddit}")
                current_id += 1
    else:
        print("No comments found.")
        break
