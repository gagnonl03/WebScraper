import requests
from bs4 import BeautifulSoup
import helper_functions as helper


# downloads a given chapter
# driver is the webdriver used to scrape
# chap is the chapter name (should be formatted using format_filename())
# chapter_url is the url for the given chapter
# folder name is the general folder for the entire manga
def download_chapter(driver, chap, chapter_url, folder_name):
    img_sources = collect_img_urls(driver, chapter_url)
    chapter_folder = folder_name + "\\" + chap
    helper.download_from_urls(chap, chapter_folder, img_sources)
    return


# collects specific image URLs from a given chapter URL
# webdriver needs to be passed in
# chap_url is the specific chapter's URL
def collect_img_urls(driver, chap_url):
    driver.get(chap_url)
    soup_source = BeautifulSoup(driver.page_source, "html.parser")
    ch_imgs = soup_source.find_all("img", class_="page-img")
    img_urls = list()
    # gets all the raw URLs for each image in the chapter
    for img in ch_imgs:
        img_urls.append(img['src'])
    return img_urls


# main launch for scraping bato
# needs a webdriver to be passed in!
def bato_scrape(driver):
    print("Input the link for a manga on bato.to (this should be the main page for the manga) "
          "to start scraping")
    user_input = input().strip().lower()
    url = user_input

    # checks link given for validity
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
        chapt_name = helper.format_filename(chapt.text[1:len(chapt.text) - 1])
        chapt_dict[chapt_name] = url_target

    # makes a folder for the given manga
    folder_name = helper.make_manga_folder(manga_name)

    # makes folders for each of the given chapters
    helper.make_folders(chapt_dict, folder_name)

    # downloads each chapter in the chapter dictionary
    for chapter in chapt_dict:
        download_chapter(driver, chapter, chapt_dict[chapter], folder_name)

    print("Download Success!")
    return
