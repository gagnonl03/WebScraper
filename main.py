import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

driver = webdriver.Chrome(options=chrome_options)


def download_from_urls(path_target, img_sources):
    x = 1
    for url in img_sources:
        urllib.request.urlretrieve(url, path_target + f"\\ Image {x}.png")
        x += 1
    return


def collect_img_urls(chap_url):
    driver.get(chap_url)
    soup_source = BeautifulSoup(driver.page_source, "html.parser")
    ch_imgs = soup_source.find_all("img", class_="page-img")
    img_urls = list()
    for img in ch_imgs:
        img_urls.append(img['src'])

    return img_urls


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

img_urls = dict()
print("Collecting URIs...")
for chap in chapt_dict:
    chap_folder = folder_name + "\\" + chap
    os.mkdir(chap_folder)
    img_urls[chap] = collect_img_urls(chapt_dict[chap])
    print(f"Collected URIs for {chap}")

print("Collected all URIs")
driver.close()

for chap in img_urls:
    print(f"Downloading images for {chap}")
    chap_folder = folder_name + "\\" + chap
    download_from_urls(chap_folder, img_urls[chap])
    print("Download Success")