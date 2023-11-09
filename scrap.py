# scrap.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from readability import Document
import requests


def get_text_content(url):
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

    # Use BeautifulSoup to parse and clean up the HTML content
    # soup = BeautifulSoup(Document(html_content).summary(), 'html.parser')
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script_or_style in soup(["script", "style", "noscript"]):
        script_or_style.decompose()

    # Get the text content of the webpage
    text_content = soup.get_text(separator=' ', strip=True)

    # Return the text content
    return text_content


def get_readable_text(url):
    response = requests.get(url)
    print(response.text)
    exit(0)
    doc = Document(response.text)
    soup = BeautifulSoup(doc.summary(), 'html.parser')

    # Optional: remove unwanted tags like script, style, etc.
    for script_or_style in soup(["script", "style", "noscript"]):
        script_or_style.decompose()

    # Get the text content of the webpage
    text_content = soup.get_text(separator=' ', strip=True)
    return text_content


# Example usage:
if __name__ == "__main__":
    # url = "https://www.theguardian.com/science/2023/nov/05/how-maths-can-help-you-win-at-everything"
    # content = get_text_content(url)
    # print(content)
    # print("--------------------------------------------------------")
    url = "https://www.theguardian.com/science/2023/nov/05/how-maths-can-help-you-win-at-everything"
    content = get_readable_text(url)
    print(content)
