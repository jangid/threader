# x.py

import json
from oauth import get_oauth_session
from post import post_tweet
from media import upload_media


def main():
    oauth = get_oauth_session()

    # Assuming 'tweets.json' has the updated format with a "thread" key.
    with open('tweets.json', 'r') as f:
        data = json.load(f)["thread"]  # Access the "thread" key directly.
        previous_tweet_id = None
        for tweet_data in data:
            tweet_text = tweet_data["text"]
            media_ids = []
            # Check for attachments and upload them
            if "attachments" in tweet_data:
                for attachment in tweet_data["attachments"]:
                    # Assume that upload_media function returns the media ID
                    media_id = upload_media(oauth, attachment["photo"])
                    if media_id:
                        media_ids.append(media_id)
            # Pass media_ids to post_tweet function
            response = post_tweet(oauth, tweet_text, previous_tweet_id, media_ids)
            previous_tweet_id = response

    print("Thread posted successfully!")


if __name__ == "__main__":
    main()
