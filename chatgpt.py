# chatgpt.py

import os
import json
from openai import OpenAI
import config

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_completion(messages, response_format={"type": "text"}, model="gpt-3.5-turbo-1106"):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format=response_format
    )
    return completion.choices[0].message.content


def get_summary(content):
    prompt = f'''

    ------------------------------------------------------------------
    Steps
    ------------------------------------------------------------------
    Generate summary of the following article. Steps/guidelines:

    1. Read the article provided below in markdown format.
    2. Generate summary in markdown format
    3. Size of summary should be less than {config.SUMMARY_SIZE_IN_WORDS} words
    4. Must include images from the original article in the summary

    ------------------------------------------------------------------
    Article
    ------------------------------------------------------------------

    {content}

    '''

    messages = [
        {"role": "system", "content": "You are a grammar assistant, skilled in summarizing content with eloquence."},
        {"role": "user", "content": prompt}
    ]

    summary = get_completion(messages=messages)
    return summary


def get_thread(content, url):
    tweet_format = '''
       {
         "id": "1",
          "text": "Introduction to the thread...",
          "attachments": [
            {
              "photo": "photo_1_url_here"
            },
            {
              "photo": "photo_2_url_here"
            }
          ]
       }
    '''

    thread_format = '''
        {
          "thread": [
            {
              "id": "1",
               "text": "Introduction to the thread...",
               "attachments": [
                 {
                   "photo": "photo_1_url_here"
                 },
                 {
                   "photo": "photo_2_url_here"
                 }
               ]
            },
            {
              "id": "2",
              "text": "Continuation of the thread...",
              "attachments": []
            },
            // More tweets as needed
            {
              "id": "last_tweet_number",
              "text": "Conclusion or CTA...",
              "attachments": []
            }
          ]
        }
    '''

    steps = f'''

    ------------------------------------------------------------------
    Steps
    ------------------------------------------------------------------

    Generate a Twitter thread in strict JSON format. Follow the steps/guidelines given below:

    1. Read the article provided below in markdown format.
    2. Prepare a thread of 5 to 10 tweets, summarizing the essense of the article. Keep the number of tweets to minimum.
    3. First tweet should introduce the topic of the article.
    4. Add twitter handle of the publisher in the first tweet.
    5. Last tweet should conclude the article with source url {url}.
    6. If found in article, include relevant photos in the tweets.
    7. Example of a single tweet is given below. Field "id", "text" are mandatory. Optional field "attachment" is an array of objects containing field "photo".
       {tweet_format}
    8. Think of hashtags to make tweets easily discoverable and to enhance engagement.
    9. Add hashtags to the prepared tweets. Select hashtags relevant to the article and the tweet.
    10. Combine multiple tweets into an array like this:
        {thread_format}
    11. Maintain a respectful tone throughout the thread.
    12. Tweet length strictly should not be greater than {config.TWEET_LENGTH} characters.

    '''

    print(content)
    if len(content.split()) > config.SUMMARY_SIZE_IN_WORDS:
        content = get_summary(content)
        print("SUMMARY:")
        print(content)

    content = f'''

    ------------------------------------------------------------------
    Article
    ------------------------------------------------------------------

    {content}

    '''

    prompt = steps + content

    messages = [
        {"role": "system", "content": "You are a journalist, skilled in reporting news on twitter."},
        {"role": "user", "content": prompt}
    ]

    while True:
        try:
            json_string = get_completion(messages=messages, response_format={
                "type": "json_object"
            })
            thread_data = json.loads(json_string)
            break
        except json.JSONDecodeError:
            print("The completion did not return valid JSON.")
            messages.append({"role": "assistant", "content": json_string})
            messages.append({"role": "user", "content": "Generate in JSON format as specified"})
            thread_data = {}

    return thread_data


def generate_thread(content, url):

    thread_data = get_thread(content, url)
    print("OUTPUT:")
    # If you want to pretty-print the dictionary
    print(json.dumps(thread_data, indent=4, ensure_ascii=False))

    return thread_data
