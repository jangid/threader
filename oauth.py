# oauth.py

from requests_oauthlib import OAuth1Session
import config


def get_oauth_session():
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

    oauth = OAuth1Session(
        config.CONSUMER_KEY,
        client_secret=config.CONSUMER_SECRET,
        resource_owner_key=oauth_tokens["oauth_token"],
        resource_owner_secret=oauth_tokens["oauth_token_secret"],
    )

    return oauth
