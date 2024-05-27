import os
import re
import logging
from googleapiclient.discovery import build
from scrape_google_results import scrape_google_results


def scrap_google_results_cloud(college, year, ext):
    #define key
    API_KEY = os.getenv('API_KEY')
    SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
    try:
        resource = build("customsearch", 'v1', developerKey=API_KEY).cse()
        result = resource.list(q = college + " common dataset" + year + ext, cx=SEARCH_ENGINE_ID).execute()
        link = result['items'][0]['link']
        links = []
        if link.endswith('.pdf') or link.endswith('.xlxs'):
                links.append(link)
        else:
            if scrape_google_results(college + " common dataset") is not None:
                link_scraped = scrape_google_results(college + " common dataset")
                if link_scraped.__contains__(college.split(" ")[0]):
                    links.append(link_scraped)
        logging.info(f'Successfully scraped Google results for college: {college}')
        return links
    except Exception as e:
        logging.error(f'Error scraping Google results for college: {college}, error: {e}')
        return None
