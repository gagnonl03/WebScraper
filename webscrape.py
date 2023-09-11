import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import shutil

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

driver = webdriver.Chrome(options=chrome_options)


def download_from_urls(path_target, img_sources):
    if len(os.listdir(path_target)) > 0:
        print("Directory is not empty, skipping...")
        return
    x = 1
    total_images = len(img_sources)
    for uri in img_sources:
        print(f"Downloading image {x} / {total_images}")
        urllib.request.urlretrieve(uri, path_target + f"\\ Image {x}.png")
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


print("Input the link for a manga on bato.to (this should be the main page for the manga) "
      "to start scraping")
user_input = input().strip().lower()
url = ""
try:
    if user_input[0:4] != "http":
        user_input = "http://" + user_input
    spliced_input = user_input.split("/")
    if spliced_input[2] != "bato.to" or spliced_input[3] != "series" or len(spliced_input) != 6:
        print("not a valid series link")
        exit(200)
    response = requests.get(user_input)
    if response.status_code == 200:
        url = user_input
except:
    print("error accessing link")
    exit(100)

# url = "https://bato.to/series/82074/horimiya-official"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

manga_name = soup.find("h3", class_="item-title").text
manga_name = manga_name[1:len(manga_name) - 1]

ch_raws = soup.find_all("a", class_="visited chapt")
chapt_dict = dict()

for chapt in ch_raws:
    url_target = "http://bato.to" + chapt['href']
    chapt_num = (chapt.text[1:len(chapt.text) - 1]
                 .replace(":", "-")
                 .replace("\n", "")
                 .replace("?", "")
                 .replace("*", " ")
                 .replace("\"", "'"))
    chapt_dict[chapt_num] = url_target

folder_name = os.getcwd() + "\\" + manga_name
if os.path.exists(folder_name):
    print("A folder with this manga's name already exists. Would you like to replace it? \n"
          "This will delete all subfolders and files! (y/n)")
    input1 = input()
    if input1.lower().strip() == "y":
        shutil.rmtree(folder_name)
        os.mkdir(folder_name)
    else:
        print("using existing directory")
else:
    os.mkdir(folder_name)

img_urls = dict()
print("Collecting URIs...")
ask_to_replace = True
for chap in chapt_dict:
    chap_folder = folder_name + "\\" + chap
    if os.path.isdir(chap_folder):
        if len(os.listdir(chap_folder)) > 0 and ask_to_replace:
            print("A folder for the volume and chapter number already exists and is not empty? Would you "
                  "like to replace it? \n"
                  "This will delete all of the folders contents! (y/n)")
            input1 = input()
            if input1.lower().strip() == "y":
                shutil.rmtree(chap_folder)
                os.mkdir(chap_folder)
            elif input1.lower().strip() == "nta":
                ask_to_replace = False
                print("received nta")
            else:
                print(f"skipped making folder for {chap}")
        else:
            print(f"skipped making folder for {chap} because of nta")
    else:
        os.mkdir(chap_folder)
    img_urls[chap] = collect_img_urls(chapt_dict[chap])
    print(f"Collected URIs for {chap}")

print("Collected all URIs")
driver.close()

for chap in img_urls:
    print(f"Downloading images for {chap}...")
    chap_folder = folder_name + "\\" + chap
    download_from_urls(chap_folder, img_urls[chap])
