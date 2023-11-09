# oauth.py

import os
import json
from requests_oauthlib import OAuth1Session
import config


# Function to save OAuth tokens
def save_oauth_tokens(oauth_tokens):
    with open('oauth_tokens.json', 'w') as file:
        json.dump(oauth_tokens, file)


# Function to load OAuth tokens
def load_oauth_tokens():
    if os.path.exists('oauth_tokens.json'):
        with open('oauth_tokens.json', 'r') as file:
            return json.load(file)
    return None


def get_oauth_session():
    # Try to load existing tokens
    oauth_tokens = load_oauth_tokens()

    if oauth_tokens:
        # If tokens exist, create an OAuth1Session with these tokens
        oauth = OAuth1Session(
            config.CONSUMER_KEY,
            client_secret=config.CONSUMER_SECRET,
            resource_owner_key=oauth_tokens["oauth_token"],
            resource_owner_secret=oauth_tokens["oauth_token_secret"],
        )
    else:
        # If tokens do not exist, go through the authentication process
        oauth = OAuth1Session(config.CONSUMER_KEY, client_secret=config.CONSUMER_SECRET)
        fetch_response = oauth.fetch_request_token(config.REQUEST_TOKEN_URL)

        print("Got OAuth token: %s" % fetch_response.get("oauth_token"))

        authorization_url = oauth.authorization_url(config.AUTHORIZATION_BASE_URL)
        print("Please go here and authorize: %s" % authorization_url)

        verifier = input("Paste the PIN here: ")

        oauth = OAuth1Session(
            config.CONSUMER_KEY,
            client_secret=config.CONSUMER_SECRET,
            resource_owner_key=fetch_response.get("oauth_token"),
            resource_owner_secret=fetch_response.get("oauth_token_secret"),
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(config.ACCESS_TOKEN_URL)

        # Save the new tokens for future use
        save_oauth_tokens(oauth_tokens)

        oauth = OAuth1Session(
            config.CONSUMER_KEY,
            client_secret=config.CONSUMER_SECRET,
            resource_owner_key=oauth_tokens["oauth_token"],
            resource_owner_secret=oauth_tokens["oauth_token_secret"],
        )

    return oauth

# from requests_oauthlib import OAuth1Session
# import config


# def get_oauth_session():
#     oauth = OAuth1Session(config.CONSUMER_KEY, client_secret=config.CONSUMER_SECRET)
#     fetch_response = oauth.fetch_request_token(config.REQUEST_TOKEN_URL)

#     print("Got OAuth token: %s" % fetch_response.get("oauth_token"))

#     authorization_url = oauth.authorization_url(config.AUTHORIZATION_BASE_URL)
#     print("Please go here and authorize: %s" % authorization_url)

#     verifier = input("Paste the PIN here: ")

#     oauth = OAuth1Session(
#         config.CONSUMER_KEY,
#         client_secret=config.CONSUMER_SECRET,
#         resource_owner_key=fetch_response.get("oauth_token"),
#         resource_owner_secret=fetch_response.get("oauth_token_secret"),
#         verifier=verifier,
#     )
#     oauth_tokens = oauth.fetch_access_token(config.ACCESS_TOKEN_URL)

#     oauth = OAuth1Session(
#         config.CONSUMER_KEY,
#         client_secret=config.CONSUMER_SECRET,
#         resource_owner_key=oauth_tokens["oauth_token"],
#         resource_owner_secret=oauth_tokens["oauth_token_secret"],
#     )

#     return oauth
