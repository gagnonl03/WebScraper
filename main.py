import os
import requests
from bs4 import BeautifulSoup


def dump_from_target(url, chap_folder):
    page = requests.get(url)
    soup = BeautifulSoup(page.content)


url = "https://bato.to/series/82074/horimiya-official"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

manga_name = soup.find("h3", class_="item-title").text
manga_name = manga_name[1:len(manga_name) - 1]
print(manga_name)

ch_raws = soup.find_all("a", class_="visited chapt")
chapt_dict = dict()

for chapt in ch_raws:
    url_target = "http://bato.to" + chapt['href']
    chapt_num = chapt.text[1:len(chapt.text) - 1]
    chapt_dict[chapt_num] = url_target

folder_name = os.getcwd() + "\\" + manga_name
os.mkdir(folder_name)

for chap in chapt_dict:
    chap_folder = folder_name + "\\" + chap
    os.mkdir(chap_folder)
    dump_from_target(chapt_dict[chap], chap_folder)