# post.py

import config


def post_tweet(oauth, content, in_reply_to_tweet_id=None, media_ids=None):
    """
    Posts a tweet with the given content and media attachments.
    If in_reply_to_tweet_id is provided, the new tweet will be a reply to it.
    Returns the ID of the tweet that was posted.
    """
    # Construct the payload based on parameters
    payload = {"text": content}
    if media_ids:
        payload["media"] = {"media_ids": media_ids}

    # If this tweet is a reply to another, set the appropriate fields
    if in_reply_to_tweet_id:
        payload["reply"] = {"in_reply_to_tweet_id": str(in_reply_to_tweet_id)}

    # Make the request using the passed OAuth1Session
    response = oauth.post(config.TWEET_URL, json=payload)

    # Check for any potential errors and throw an exception if any occur
    if response.status_code != 201:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")

    # Parse the response to JSON
    json_response = response.json()

    # Return the ID of the tweet that was just posted
    return json_response["data"]["id"]
