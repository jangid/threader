# scraper_default.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from readability import Document
from markdownify import markdownify as md


def get_default_readable_markdown(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures the browser window isn't shown

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for the JavaScript to be idle (i.e., wait for the page to fully load)
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

    # Find the body element using the updated method
    # body = driver.find_element(By.TAG_NAME, 'body')

    # Scroll through the page
    # for _ in range(10):  # Adjust the range as necessary
    #     body.send_keys(Keys.END)
    #     time.sleep(1)  # Wait for content to load

    # Retrieve and store the page source after scrolling
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
    url = "https://en.wikipedia.org/wiki/Twitter"
    content = get_default_readable_markdown(url)
    print(content)
