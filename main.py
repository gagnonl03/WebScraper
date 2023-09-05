import shutil
import urllib.request

from bs4 import BeautifulSoup
import requests

url = "https://bato.to/series/82074/horimiya-official"
page = requests.get(url)
manga_name = ""

soup = BeautifulSoup(page.content, "html.parser")
manga_name = ""
ch_raws = soup.find_all("a", class_="visited chapt")

url_targets = []

for chapt in ch_raws:
    url_targets.append("http://bato.to/" + chapt['href'], )

print(url_targets)