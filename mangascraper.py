import helper_functions as helper
import bato_scraper as bato_scraper
from selenium import webdriver




print("Welcome to webscraper v1.1")

data = ["Chrome", "Edge"]

num_input = helper.get_indexed_input("Select the browser you have installed", data)

if num_input == 0:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
else:
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('--blink-settings=imagesEnabled=false')
    edge_options.add_argument("--disable-extensions")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--headless=new")

    driver = webdriver.Edge(options=edge_options)

run = True
while run:
    program_options = ["Download manga", "Exit"]
    option_selected = helper.get_indexed_input("What would you like to do?", program_options)
    if option_selected == 0:
        bato_scraper.bato_scrape(driver)
    else:
        print("Quitting...")
        exit(0)
