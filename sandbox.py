import time

import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver

import helper_functions



browser = webdriver.Chrome()

#wire_browser = webdriver.Firefox()



browser.get("http://bato.to/chapter/1579383")

soup_source = BeautifulSoup(browser.page_source, "html.parser")
ch_imgs = soup_source.find_all("img", class_="page-img")
uri = ch_imgs[10]['src']

