# scrap.py

from urllib.parse import urlparse
from default_scraper import get_default_readable_markdown
from noscript_scraper import get_noscript_readable_markdown
import nyt_scraper
import sys


def validate_args():
    if len(sys.argv) < 2:
        print("Usage: python x.py <URL>")
        sys.exit(1)


def get_readable_markdown(url):
    # Parse the URL to extract the domain
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if 'nytimes.com' in domain:
        scraper = nyt_scraper.Scraper()
        # Use New York Times specific scraping method
        article = scraper.get_article(url)
        return article.title
    # else:
    #     # Use the default scraping method
    #     return get_default_readable_markdown(url)
    else:
        # Use the default scraping method
        return get_noscript_readable_markdown(url)


# Example usage
if __name__ == "__main__":
    validate_args()
    url = sys.argv[1]
    content = get_readable_markdown(url)
    print(content)
