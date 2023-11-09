# scrap.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def get_html_content(url):
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

    # Return the HTML content
    return html_content


# Example usage:
if __name__ == "__main__":
    url = "https://www.fastcompany.com/90978355/in-the-mississippi-valley-these-farmers-are-getting-paid-to-restore-3000-acres-of-forest?partner=rss"
    content = get_html_content(url)
    print(content)
