# scrap.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from readability import Document
from markdownify import markdownify as md
import requests
import os


def get_readable_markdown(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures the browser window isn't shown

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for the JavaScript to be idle (i.e., wait for the page to fully load)
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

    # Retrieve and store the page source
    html_content = driver.page_source

    # Close the driver
    driver.quit()

    # Process the content with Readability
    doc = Document(html_content)
    soup = BeautifulSoup(doc.summary(), 'html.parser')

    # Convert HTML to Markdown
    markdown_content = md(str(soup), heading_style="ATX")
    return markdown_content


# Example usage:
if __name__ == "__main__":
    url = "https://www.theguardian.com/science/2023/nov/05/how-maths-can-help-you-win-at-everything"
    content = get_readable_markdown(url)
    print(content)
