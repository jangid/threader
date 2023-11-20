# x.py

import sys
import time
import random
from oauth import get_oauth_session
from post import post_tweet, is_tweet_long
from media import upload_media
from scrap import get_readable_markdown
from chatgpt import generate_thread
import config


def validate_args():
    if len(sys.argv) < 2:
        print("Usage: python x.py <URL>")
        sys.exit(1)


def handle_tweets(thread_data):
    oauth = get_oauth_session()
    previous_tweet_id = None
    for tweet_data in thread_data["thread"]:
        tweet_text = tweet_data["text"]
        media_ids = process_attachments(tweet_data, oauth)
        # Pass media_ids to post_tweet function
        response = post_tweet(oauth, tweet_text, previous_tweet_id, media_ids)
        previous_tweet_id = response
        time.sleep(random.randint(config.TWEET_GAP_MIN, config.TWEET_GAP_MAX))
    print("Thread posted successfully!")


def process_attachments(tweet_data, oauth):
    media_ids = []
    # Check for attachments and upload them
    if "attachments" in tweet_data:
        for attachment in tweet_data["attachments"]:
            media_id = upload_media(oauth, attachment["photo"])
            if media_id:
                media_ids.append(media_id)
    return media_ids


def user_confirmation():
    return input("Do you want to post the tweets? [Yes/Regenerate/Abort]: ").strip().lower()


def regenerate_thread(content, url):
    while True:
        thread_data = generate_thread(content, url)
        if not is_tweet_long(thread_data):
            return thread_data


def main():
    validate_args()
    url = sys.argv[1]
    content = get_readable_markdown(url, True)
    thread_data = regenerate_thread(content, url)

    while True:
        user_input = user_confirmation()

        if user_input in ['yes', 'y']:
            handle_tweets(thread_data)
            break
        elif user_input in ['regenerate', 'r']:
            thread_data = regenerate_thread(content, url)
        elif user_input in ['abort', 'a']:
            print("Operation aborted by the user.")
            break
        else:
            print("Invalid input. Please enter 'Yes', 'Regenerate', or 'Abort'.")


if __name__ == "__main__":
    main()
