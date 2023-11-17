# scraper_default.py

from bs4 import BeautifulSoup, Comment
from readability import Document
from markdownify import markdownify as md
import requests


def get_noscript_readable_markdown(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        # doc = Document(response.content)
        # soup = BeautifulSoup(doc.summary(), 'html.parser')
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract and print the desired content
        # For example, extracting all paragraph texts
        # paragraphs = soup.find_all('p')
        # for para in paragraphs:
        #     print(para.get_text())

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Remove comment elements
        for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Optional: Remove attributes from tags to simplify
        for tag in soup.find_all(True):
            tag.attrs = {}

        # Convert HTML to Markdown
        markdown_content = md(str(soup), heading_style="ATX")
        return markdown_content
    else:
        print("Error: Unable to fetch the webpage.")
        response = requests.get(url)


# Example usage:
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Twitter"
    content = get_noscript_readable_markdown(url)
    print(content)
