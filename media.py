# media.py

import config
import requests


def upload_media(oauth, media_source):
    """
    Uploads media to Twitter and returns the media ID.
    The media_source can be a local file path or a remote URL.
    """
    if media_source.startswith('http://') or media_source.startswith('https://'):
        # Media source is a URL
        response = requests.get(media_source)
        if response.status_code != 200:
            raise Exception(f"Error downloading image from URL: {response.status_code}")
        media_data = response.content
    else:
        # Media source is a local file path
        with open(media_source, 'rb') as file:
            media_data = file.read()

    media_endpoint_url = config.MEDIA_UPLOAD_URL
    files = {'media': media_data}

    # Make the request to upload the media
    media_response = oauth.post(media_endpoint_url, files=files)
    if media_response.status_code != 200:
        raise Exception(f"Media upload failed: {media_response.status_code} {media_response.text}")

    media_id = media_response.json()["media_id_string"]
    return media_id
