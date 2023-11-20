# scrap.py

import os
import hashlib
from urllib.parse import urlparse
from default_scraper import get_default_readable_markdown
from noscript_scraper import get_noscript_readable_markdown
import nyt_scraper
import sys


def validate_args():
    # Adjust to check for at least 2 arguments (script name and URL)
    if len(sys.argv) < 2:
        print("Usage: python scrap.py [-cache] <URL>")
        sys.exit(1)


def get_cache_filename(url):
    # Create a hash of the entire URL for a unique filename
    url_hash = hashlib.md5(url.encode()).hexdigest()

    # Ensure the cache directory exists
    cache_dir = ".threader_cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Generate a filename based on the URL hash
    return os.path.join(cache_dir, f"cache_{url_hash}.md")


def read_from_cache(cache_file):
    with open(cache_file, 'r') as file:
        return file.read()


def write_to_cache(cache_file, content):
    with open(cache_file, 'w') as file:
        file.write(content)


def get_readable_markdown(url, use_cache):
    # Generate cache filename
    cache_file = get_cache_filename(url)

    # Check if cache exists and use_cache is True
    if use_cache and os.path.exists(cache_file):
        print("Reading from cache.")
        return read_from_cache(cache_file)

    # Scrape content if cache doesn't exist or not using cache
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    md_content = ""

    if 'nytimes.com' in domain:
        scraper = nyt_scraper.Scraper()
        article = scraper.get_article(url)
        md_content = article.title
    else:
        md_content = get_noscript_readable_markdown(url)

    # Write content to cache
    write_to_cache(cache_file, md_content)

    return md_content


# Example usage
if __name__ == "__main__":
    validate_args()

    # Check if the first argument is '-cache'
    use_cache = (sys.argv[1] == "-cache")

    # Determine the URL based on whether '-cache' is present
    url = sys.argv[2] if use_cache else sys.argv[1]

    content = get_readable_markdown(url, use_cache)
    print(content)
