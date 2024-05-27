import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Function to scrape Google search results
def scrape_google_results(query):
    # Set up Chrome WebDriver
    driver = webdriver.Chrome()
    # Navigate to Google
    driver.get("https://www.google.com")
    # Find the search box and input the query
    search_box = driver.find_element(By.NAME,"q")
    search_box.send_keys(query)
    # Submit the search
    search_box.send_keys(Keys.RETURN)
    # Wait for results to load
    time.sleep(2)
    # Get URLs of search results
    try:
        links = []
        results = driver.find_elements(By.XPATH,'//a')   
        for result in results:
            link = result.get_attribute("href")
            if link and (link.endswith('.pdf') or link.endswith('.xlsx')):
                links.append(link)
        # Close the browser
        driver.quit()
        logging.info(f'Successfully scraped Google results for keyword: {query}')
        if len(links) > 1:
            for link in links:
                if query.split(" ")[0] in link:
                    links = link
        return links
    except Exception as e:
        logging.error(f'Error scraping Google results for keyword: {query}, error: {e}')
        return "None"

