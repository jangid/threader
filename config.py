# config.py

import os

# Assuming you've already set these environment variables
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
AUTHORIZATION_BASE_URL = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
TWEET_URL = "https://api.twitter.com/2/tweets"
MEDIA_UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"

# Parameters
SUMMARY_SIZE_IN_WORDS = 2500
TWEET_LENGTH = 280
TWEET_GAP_MIN = 10
TWEET_GAP_MAX = 30
