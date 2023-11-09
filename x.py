# x.py

import sys
from oauth import get_oauth_session
from post import post_tweet
from media import upload_media
from scrap import get_html_content
from chatgpt import generate_thread  # Assuming you have a function to generate threads using ChatGPT


def main():
    # Step 1: Read link from CLI argument and scrap using scrap.py
    if len(sys.argv) < 2:
        print("Usage: python x.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    content = get_html_content(url)

    # Step 2: Parse content and create json thread using chatgpt api
    thread_data = generate_thread(content, url)  # This function should return the thread data in the required JSON format

    print(thread_data)
    # Loop to handle user input
    while True:
        # Step 3: Ask user to confirm if tweets should be posted
        user_input = input("Do you want to post the tweets? [Yes/Regenerate/Abort]: ").strip().lower()

        if user_input in ['yes', 'y']:
            # Step 6: Post tweets if user says Yes
            oauth = get_oauth_session()
            previous_tweet_id = None
            for tweet_data in thread_data:
                tweet_text = tweet_data["text"]
                media_ids = []
                # Check for attachments and upload them
                if "attachments" in tweet_data:
                    for attachment in tweet_data["attachments"]:
                        media_id = upload_media(oauth, attachment["photo"])
                        if media_id:
                            media_ids.append(media_id)
                # Pass media_ids to post_tweet function
                response = post_tweet(oauth, tweet_text, previous_tweet_id, media_ids)
                previous_tweet_id = response
            print("Thread posted successfully!")
            break
        elif user_input in ['regenerate', 'r']:
            # Step 5: Regenerate the thread if the user is not satisfied
            thread_data = generate_thread(content)  # Regenerate the thread
        elif user_input in ['abort', 'a']:
            # Step 7: Abort if user decides not to post
            print("Operation aborted by the user.")
            break
        else:
            print("Invalid input. Please enter 'Yes', 'Regenerate', or 'Abort'.")


if __name__ == "__main__":
    main()
