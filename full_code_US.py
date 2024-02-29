import os
import pandas as pd
import time
import sqlite3
import re
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from googleapiclient.discovery import build

logging.basicConfig(filename='log_file/US_CDS.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

df = pd.read_excel('data/US CDS List.xlsx')

college_list = []
for college in df['Colleges']:
    if college not in college_list:
        college_list.append(college)


# Function to scrape Google search results
def scrape_google_results(query, num_results=10):
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
        results = driver.find_elements(By.CSS_SELECTOR,"div.yuRUbf a")
        for result in results[:num_results]:
            link = result.get_attribute("href")
            if link.endswith('.pdf') or link.endswith('.xlxs'):
                links.append(link)
        
        # Close the browser
        driver.quit()
        logging.info(f'Successfully scraped Google results for keyword: {query}')
        return links[0]
    
    except Exception as e:
        logging.error(f'Error scraping Google results for keyword: {query}, error: {e}')
        return "None"
    
def scrap_google_results_cloud(college):
    #define key
    API_KEY = os.getenv('API_KEY')
    SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
    
    try:
        resource = build("customsearch", 'v1', developerKey=API_KEY).cse()
        result = resource.list(q=college, cx=SEARCH_ENGINE_ID).execute()
        
        link = result['items'][0]['link']
        links = []
        if link.endswith('.pdf') or link.endswith('.xlxs'):
                links.append(link)
        else:
            links.append("None")
        logging.info(f'Successfully scraped Google results for college: {college}')
        return links[0]

    except Exception as e:
        logging.error(f'Error scraping Google results for college: {college}, error: {e}')
        return None

# Get the name of the college
def clean_college(college):
    college = college.lower()
    return re.sub(r'[^\w\s]', '', college.split(" cds")[0])  # Remove symbols
  
# Store everything in a database SQL
def store_db(college_name, file_name, url):
    conn = sqlite3.connect('college_cds.db')
    curr = conn.cursor()
    
    curr.execute('''
        CREATE TABLE IF NOT EXISTS search_result (
            college_name VARCHAR(100), 
            file_name VARCHAR(100), 
            url VARCHAR(100)
        )
    ''')
    # insert data into a table
    curr.execute("INSERT INTO search_result (college_name, file_name, url) VALUES (?,?,?)", 
                    (college_name, file_name, url))
        
    conn.commit()
    conn.close()


for college in college_list:
    college_name = clean_college(college)
    scraped_links = scrap_google_results_cloud(college)
    store_db(college_name, college, scraped_links)
    print(f'Successfully scraped {college_name} CDS file')
