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

df = pd.read_csv('data/indian_dataset.csv')

college_list = []
for college in df['name']:
    if college not in college_list:
        college_list.append(college)

def scrap_google_results_cloud(college):
    #define key
    API_KEY = os.getenv('API_KEY')
    SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
    
    try:
        resource = build("customsearch", 'v1', developerKey=API_KEY).cse()
        result = resource.list(q=college + " common dataset", cx=SEARCH_ENGINE_ID).execute()
        
        link = result['items'][0]['link']

        title = result['items'][0]['displayLink']
        links = []
        if link.endswith('.pdf') or link.endswith('.xlxs'):
                links.append(link)
        else:
            links.append("None")
        logging.info(f'Successfully scraped Google results for college: {college}')
        return links[0], title

    except Exception as e:
        logging.error(f'Error scraping Google results for college: {college}, error: {e}')
        return None, None
  
# Store everything in a database SQL
def store_db(college_name, domain, file_url):
    conn = sqlite3.connect('indian_college_cds.db')
    curr = conn.cursor()
    
    curr.execute('''
        CREATE TABLE IF NOT EXISTS search_result (
            college_name VARCHAR(100), 
            domain VARCHAR(100), 
            file_url VARCHAR(100)
        )
    ''')
    # insert data into a table
    curr.execute("INSERT INTO search_result (college_name, domain, file_url) VALUES (?,?,?)", 
                    (college_name, domain, file_url))
        
    conn.commit()
    conn.close()


for college in college_list:
    scraped_links = scrap_google_results_cloud(college)
    store_db(college, scraped_links[1], scraped_links[0])
    print(f'Successfully scraped {college}')
