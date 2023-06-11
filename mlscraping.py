from bs4 import BeautifulSoup
import re
import time
import requests
from bs4 import BeautifulSoup
import re
import time

def login_session(login_url, form_data):
    sesh = requests.Session()
    sesh.post(login_url, data = form_data)
    return sesh
def cl_search_txt(soup, class_str, index = 0):
    container = soup.select(class_str)
    return container[index].text
def pages_search(sesh, search_url, find_text, url_match = None, backup_first_result = False):
    search_page = sesh.get(search_url)
    search = find_text
    urls = get_matching_urls(search_page, url_match)
    first_match = None
    page = None
    for url in urls:
        page = sesh.get(url)
        if first_match is None:
            first_match = page
        search_m = re.search(str(search), page.text)
        if search_m is not None:
            print("found " + str(search) + " in page " + page.url)
            break
        else:
            page = None
            print(url)
            time.sleep(0.5)
    if page is None and first_match is not None and backup_first_result == True:
        page = first_match
    return page
def get_matching_urls(page, url_pattern = None):
    soup = BeautifulSoup(page.text)
    if url_pattern is None:
        links = soup.find_all('a')
    else:
        links = soup.find_all('a', href=re.compile('^' + url_pattern))
    urls = []
    for link in links:
        url = link.get('href')
        if url not in urls:
            urls.append(url)
    return urls
