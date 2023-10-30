import json
from requests_oauthlib import OAuth1Session
import os

# Assuming you've already set these environment variables
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")


def post_tweet(content, in_reply_to_tweet_id=None):
    """
    Posts a tweet with the given content.
    If in_reply_to_tweet_id is provided, the new tweet will be a reply to it.
    Returns the ID of the tweet that was posted.
    """
    url = "https://api.twitter.com/2/tweets"

    # Construct the payload based on parameters
    payload = {"text": content}

    # If this tweet is a reply to another, set the appropriate fields
    if in_reply_to_tweet_id:
        payload["reply"] = {"in_reply_to_tweet_id": str(in_reply_to_tweet_id)}

    # Make the request using OAuth1Session with user's access token and token secret
    response = oauth.post(url, json=payload)

    # Check for any potential errors and throw an exception if any occur
    if response.status_code != 201:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")

    # Parse the response to JSON
    json_response = response.json()

    # Return the ID of the tweet that was just posted
    return json_response["data"]["id"]

# Main code starts here


# 1. Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# 2. Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# 3. Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Update oauth session for tweet posting
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Load tweets from json and post them
with open('tweets.json', 'r') as f:
    data = json.load(f)
    previous_tweet_id = None
    for tweet_data in data["thread"]:
        tweet_text = tweet_data["text"]
        response = post_tweet(tweet_text, previous_tweet_id)
        previous_tweet_id = response

print("Thread posted successfully!")
