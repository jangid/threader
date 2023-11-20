# x.py

import os
import hashlib
import json
import sys
import time
import random
from oauth import get_oauth_session
from post import post_tweet, check_tweet_lengths
from media import upload_media
from scrap import get_readable_markdown
from chatgpt import generate_thread
import config


def validate_args():
    # Adjust to check for at least 2 arguments (script name and URL)
    if len(sys.argv) < 2:
        print("Usage: python x.py [-cache] <URL>")
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


def process_attachments(tweet_data, oauth):
    media_ids = []
    # Check for attachments and upload them
    if "attachments" in tweet_data:
        for attachment in tweet_data["attachments"]:
            media_id = upload_media(oauth, attachment["photo"])
            if media_id:
                media_ids.append(media_id)
    return media_ids


def get_thread_cache_filename(url):
    """Generates a cache filename based on the URL."""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return f".threader_cache/tweets_{url_hash}.json"


def read_from_thread_cache(url):
    """Reads thread data from the cache."""
    cache_file = get_thread_cache_filename(url)
    if not os.path.exists(cache_file):
        print(f"No cached data found for URL: {url}")
        return None

    with open(cache_file, 'r') as file:
        return json.load(file)


def write_to_thread_cache(thread_data, url):
    """Writes thread data to the cache."""
    cache_dir = ".threader_cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    file_path = get_thread_cache_filename(url)
    with open(file_path, 'w') as file:
        json.dump(thread_data, file, indent=4)

    print(f"Thread saved to {file_path}")


def user_confirmation():
    return input("Do you want to post the tweets? [Yes/Regenerate/Abort/Save]: ").strip().lower()


def regenerate_thread(content, url):
    thread_data = generate_thread(content, url)
    check_tweet_lengths(thread_data)
    return thread_data


def main():
    validate_args()

    # Check if the first argument is '-cache'
    use_cache = (sys.argv[1] == "-cache")

    # Determine the URL based on whether '-cache' is present
    url = sys.argv[2] if use_cache else sys.argv[1]

    if use_cache:
        # Code to tweet from cache if "-cache" argument is given
        thread_data = read_from_thread_cache(url)
        if thread_data:
            handle_tweets(thread_data)
            print("Thread posted from cache successfully!")
            return  # Exit after posting from cache
        else:
            print("Proceeding to generate thread data...")

    content = get_readable_markdown(url, True)
    thread_data = regenerate_thread(content, url)

    while True:
        user_input = user_confirmation()

        if user_input in ['yes', 'y']:
            handle_tweets(thread_data)
            print("Thread posted successfully!")
            break
        elif user_input in ['regenerate', 'r']:
            thread_data = regenerate_thread(content, url)
        elif user_input in ['save', 's']:
            write_to_thread_cache(thread_data, url)
            break
        elif user_input in ['abort', 'a']:
            print("Operation aborted by the user.")
            break
        else:
            print("Invalid input. Please enter 'Yes', 'Regenerate', 'Abort', or 'Save'.")


if __name__ == "__main__":
    main()
