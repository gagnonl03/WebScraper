import requests
from bs4 import BeautifulSoup
import helper_functions as helper


def download_chapter(driver, chap, chapter_url, folder_name):
    img_sources = collect_img_urls(driver, chapter_url)
    chapter_folder = folder_name + "\\" + chap
    helper.download_from_urls(chap, chapter_folder, img_sources)
    return


def collect_img_urls(driver, chap_url):
    driver.get(chap_url)
    soup_source = BeautifulSoup(driver.page_source, "html.parser")
    ch_imgs = soup_source.find_all("img", class_="page-img")
    img_urls = list()
    for img in ch_imgs:
        img_urls.append(img['src'])
    return img_urls


def bato_scrape(driver):
    print("Input the link for a manga on bato.to (this should be the main page for the manga) "
          "to start scraping")
    user_input = input().strip().lower()
    url = user_input

    if user_input[0:4] != "http":
        user_input = "http://" + user_input
        spliced_input = user_input.split("/")
        if spliced_input[2] != "bato.to" or spliced_input[3] != "series" or len(spliced_input) != 6:
            print("not a valid series link\n")
            return
        response = requests.get(user_input)
        if response.status_code == 200:
            url = user_input

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    manga_name = soup.find("h3", class_="item-title").text
    manga_name = manga_name[1:len(manga_name) - 1]

    ch_raws = soup.find_all("a", class_="visited chapt")
    chapt_dict = dict()

    for chapt in ch_raws:
        url_target = "http://bato.to" + chapt['href']
        chapt_num = helper.format_filename(chapt.text[1:len(chapt.text) - 1])
        chapt_dict[chapt_num] = url_target

    folder_name = helper.make_manga_folder(manga_name)

    helper.make_folders(chapt_dict, folder_name)
    for chapter in chapt_dict:
        download_chapter(driver, chapter, chapt_dict[chapter], folder_name)

    driver.close()
    print("Download Success!")
    return
