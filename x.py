import json
from oauth import get_oauth_session
from post import post_tweet


def main():
    oauth = get_oauth_session()

    with open('tweets.json', 'r') as f:
        data = json.load(f)
        previous_tweet_id = None
        for tweet_data in data["thread"]:
            tweet_text = tweet_data["text"]
            response = post_tweet(oauth, tweet_text, previous_tweet_id)
            previous_tweet_id = response

    print("Thread posted successfully!")


if __name__ == "__main__":
    main()
