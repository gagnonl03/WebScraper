import os
import urllib.request
from bs4 import BeautifulSoup


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


def collect_img_urls(driver, chap_url):
    driver.get(chap_url)
    soup_source = BeautifulSoup(driver.page_source, "html.parser")
    ch_imgs = soup_source.find_all("img", class_="page-img")
    img_urls = list()
    for img in ch_imgs:
        img_urls.append(img['src'])

    return img_urls
