import helper_functions as helper
import bato_scraper as bato_scraper
from selenium import webdriver
import mangadex_api

print("Welcome to webscraper v1.1")

data = ["Chrome", "Edge"]

browser_type = helper.get_indexed_input("Select the browser you have installed", data)

run = True


def initialize_driver():
    print("Initializing Selenium Browser...")
    if browser_type == 0:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless=new")

        browser = webdriver.Chrome(options=chrome_options)
    else:
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument('--blink-settings=imagesEnabled=false')
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--headless=new")

        browser = webdriver.Edge(options=edge_options)

    return browser


while run:
    program_options = ["Download manga", "Exit"]
    option_selected = helper.get_indexed_input("What would you like to do?", program_options)
    if option_selected == 0:
        source_options = ["Bato", "MangaDex"]
        source_selected = helper.get_indexed_input("Select manga source", source_options)
        if source_selected == 0:
            driver = initialize_driver()
            bato_scraper.bato_scrape(driver)
            driver.close()
        else:
            mangadex_api.mangadex_download()
    else:
        print("Quitting...")
        run = False


exit(0)