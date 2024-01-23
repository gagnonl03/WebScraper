import time

import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver

import helper_functions




#wire_browser = webdriver.Firefox()

headers = {
    'referer': 'https://chapmanganato.to/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


r = requests.get("https://chapmanganato.to/manga-rz951534/chapter-1")
soup = BeautifulSoup(r.content, "html.parser")
#out = soup.find_all("a", class_="chapter-name text-nowrap")
#print(out[::-1][0]["href"])

out = soup.find_all("img")
print(out[1:len(out) - 1])



