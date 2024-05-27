from bs4 import BeautifulSoup
import os
import urllib.request

def download_file(URL, college_name, year, ext):
    folder_path = 'downloaded_files'
    filename = f"{folder_path}/{college_name}_{year}{ext if ext else ''}"
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    req = urllib.request.Request(URL, headers=hdr)
    try:
        response = urllib.request.urlopen(req)
        content = response.read()
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(filename, 'wb') as output:
            output.write(content)
            print(f"File {filename} downloaded successfully")
        return filename
    except urllib.error.HTTPError as e:
        print(e.read())