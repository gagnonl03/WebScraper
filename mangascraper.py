import helper_functions as helper
import webscrape as bato_scraper
from selenium import webdriver




print("Welcome to webscraper v1.1")

data = ["Chrome", "Edge", "Firefox"]

num_input = helper.get_indexed_input("Select the browser you have installed",data)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=chrome_options)

run = True
while(run):
    program_options = ["Download manga", "Exit"]
    option_selected = helper.get_indexed_input("What would you like to do?", program_options)
    if option_selected == 0:
        bato_scraper.bato_scrape(driver)
    else:
        print("Quitting...")
        exit(0)
