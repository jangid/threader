# chatgpt.py

import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_completion(prompt, model="gpt-3.5-turbo"):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,  # Degree of randomness
        # Include any other parameters you need
    )
    return response.choices[0].text.strip()


def generate_thread(content, url):
    advice = f'''

    Convert the content into a tweeter thread. Consider the following advice:

    1. The following content is in plain html format
    2. Embed relevant photos
    3. Keep the number of tweets to minimum
    4. Add relevant hashtags for making it easily discoverable
    5. Keep the tone respectable
    6. Mention twitter handle of the publisher if found in the content
    7. Add information source url: {url}

    '''
    thread_format = '''

    Generate twitter thread in JSON format given below:

      {
        "thread": [
          {
            "id": "1",
            "text": "",
            "attachments": [
                {
                  "photo": ""
                }
            ]
          },
          {
            "id": "2",
            "text": "",
            "attachments": [
                {
                  "photo": ""
                }
            ]
          },
          ...
        ]
      }

    '''

    html = f'''

    content:

    {content}

    '''
    prompt = advice + thread_format + html
    # use above prompt code to generate json thread
    return get_completion(prompt, model="gpt-4")
