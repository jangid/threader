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
    prompt = f"""

    Summarize the following text in less than {config.SUMMARY_SIZE_IN_WORDS} words:

    {content}

    """

    messages = [
        {"role": "system", "content": "You are a grammar assistant, skilled in summarizing content with eloquence."},
        {"role": "user", "content": prompt}
    ]

    summary = get_completion(messages=messages)
    return summary


def get_thread(content, url):
    advice = f'''

Please generate a Twitter thread in strict JSON format, adhering to the following guidelines:

1. The content is provided in plain text and should be broken down into a series of tweets, keeping the number of tweets to a minimum. Not more than 5 tweets.
2. Include relevant hashtags to make the thread easily discoverable and enhance engagement.
3. Maintain a respectful tone throughout the thread.
4. If a Twitter handle of the publisher is mentioned in the content, it must be included in the thread.
5. The source URL ({url}) must be referenced in the thread.
6. Each tweet must be represented as a separate object within the "thread" array of the JSON.
7. The first tweet should introduce the topic, and subsequent tweets should elaborate on the content, ending with a conclusion or call-to-action in the final tweet.
8. Where relevant, include photos by specifying the URL in the "photo" field of the "attachments" array for each tweet object.
9. Tweet length strictly should not be greater than 160 characters.

    '''

    thread_format = '''

The JSON structure for the thread should be exactly as follows, with no deviations:

{
  "thread": [
    {
      "id": "1",
      "text": "Introduction to the thread...",
      "attachments": [
        {
          "photo": "photo_url if available"
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

Add attachments.photo element only if the photo url is available; otherwise just add empty attachments array.
Ensure that all fields are filled accurately, and the JSON format is strictly maintained. Please proceed with generating the Twitter thread.

    '''

    content = f'''

Content:

{content}

    '''

    print(content)
    if len(content.split()) > config.SUMMARY_SIZE_IN_WORDS:
        content = get_summary(content)
        print("SUMMARY:")
        print(content)

    prompt = advice + thread_format + content

    messages = [
        {"role": "system", "content": "You are a grammar assistant, skilled in summarizing content with eloquence."},
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
