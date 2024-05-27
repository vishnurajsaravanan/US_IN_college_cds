from scrape_google_results import scrape_google_results
from scrap_google_results_cloud import scrap_google_results_cloud
from download_file import download_file
from extract_data_from_excel import extract_data_excel
from extract_data_from_pdf import extract_data_pdf
from upload_file import upload_file, store_in_firestore
from store_db import store_db
from clean_college import clean_college, get_extension, year
import time
import logging
import os
import pandas as pd
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By


logging.basicConfig(filename='log_file/US_CDS.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

df = pd.read_excel('data/US CDS List.xlsx')
college_list = []
for college in df['Colleges']:
    if college not in college_list:
        college_list.append(college)

  
def direct_download_from_website(URL, college_name, year, ext):
    if URL is None:
        print("No URL found in the provided HTML.")
        return None

    folder_path = 'downloaded_files'
    filename = f"{folder_path}/{college_name}_{year}{ext if ext else ''}"
    # Initialize a browser driver
    driver = webdriver.Chrome()  # or webdriver.Chrome(), depending on your browser
    print(f"Downloading file from {URL}")
    # Navigate to the URL
    download_link = driver.get(URL)
    # Find the download link and click it
    # You'll need to replace 'download-link' with the actual ID, name, or XPath of the download link
    download_link = driver.find_element(By.XPATH, f"//a[@href='{download_link}']")
    download_link.click()
    # Wait for the download to complete
    # You'll need to replace this with actual code to wait for the download to complete
    # This could be as simple as a time.sleep() call, or as complex as code that checks the download directory for the file
    time.sleep(5)  # wait for 5 seconds
    # Move the downloaded file to the desired location
    # You'll need to replace 'downloaded_file_path' with the actual path of the downloaded file
    downloaded_file_path = os.path.join(folder_path, URL.split('/')[-1])
    os.rename(downloaded_file_path, filename)

    print(f"File {filename} downloaded successfully")  
    return filename


count = 0
length = len(college_list)
# Code starts here
no_links = []
for college in college_list:
    print("------------------------")
    # print(college)
    college_name = clean_college(college)
    print(college_name)
    cds_year = year(college)
    print(cds_year)
    if cds_year is None:
        cds_year = '2022-2023'
    extension = get_extension(college)
    print(extension)
    scraped_links = scrap_google_results_cloud(college_name, cds_year, extension)
    print(f'Successfully scraped {college_name} CDS file')
    if scraped_links is None:
        if extension is None:
            scraped_links = list(scrape_google_results(college_name + " common dataset" + cds_year))
        elif extension.endswith('.pdf') or extension.endswith('.xlsx'):
            scraped_links = list(scrape_google_results(college_name + " common dataset" + cds_year + extension))
        else:
            logging.error(f'Error scraping Google results for college: {college_name}')
            print(f'Error scraping Google results for college: {college_name}')

    if len(scraped_links) >= 1:
        scraped_link = scraped_links[0]
    else:
        scraped_link = scraped_links
                        # if scraped_links is None:
            #     logging.error(f'Error scraping Google results for college: {college_name}')
            #     print(f'Error scraping Google results for college: {college_name}')
            #     break
    print(scraped_link)
    try:
        download_files = download_file(URL=scraped_link, college_name=college_name, year=cds_year, ext=extension)
        print(download_files)
        if download_files is None:
            download_files = direct_download_from_website(URL=scraped_links, college_name=college_name, year=cds_year, ext=extension)
    except Exception as e:
        logging.error(f'Error downloading file for college: {college_name}, error: {e}')
        print(f'Error downloading file for college: {college_name}, error: {e}')
        no_links.append(college_name)
        continue
    if download_files is not None:
        upload_file(download_files) # Upload file to Firebase Storage
        if download_files.endswith('.pdf'):  
            print(download_files)
            data = extract_data_pdf(download_files)

        elif download_files.endswith('.xlsx'):
            data = extract_data_excel(download_files)
          
        else:
            print("File format not supported")
        store_db(college_name, college, scraped_links[0])
        # print(scraped_link)
        # print(data)
        
        if data is not None:
            store_in_firestore(college_name, data) # Store data in Firestore
        else:
            print(f'No data extracted for {college_name}')
        count += 1

        # print("PDF/Excel file downloaded and data extracted successfully!", count, "out of", length)
        with open('output.txt', 'a') as f:
            f.write('\n-------------------------------------\n')
            f.write(f"{college}\n")
            f.write(f"{college_name}\n")
            f.write(f"{cds_year}\n")
            f.write(f"{extension}\n")
            f.write(f"{scraped_link}\n")
            f.write(f"Successfully scraped {college_name} cds file\n")
            for key, value in data.items():
               f.write(f"{key}: {value}\n")
            f.write(f"Data for {college_name} stored in Firestore\n")
            f.write(f"PDF/Excel file downloaded and data extracted successfully! {count} out of {length}")
        # print(data)
    # print(no_links)