import shutil
import urllib.request

from bs4 import BeautifulSoup
import requests

url = "https://chapmanganato.com/manga-rz951534"
page = requests.get(url)
print(page)

'''
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
job_elements = results.find_all("div", class_="card-content")
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
    '''

soup = BeautifulSoup(page.content, "html.parser")
ch_raws = soup.find_all("a", class_="chapter-name text-nowrap")
print(ch_raws)
ch_targets = []
for ch_raw in ch_raws:
    ch_targets.append(ch_raw['href'])

print(ch_targets)

url = ch_targets[0]
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
img_cont = soup.find(class_="container-chapter-reader")
imgs = img_cont.find_all("img")
x = 1
img_url = imgs[0]
img_url = img_url['src']
print(img_url)

r = requests.get(img_url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
print(r.status_code)
if r.status_code == 200:
    with open("img.png", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)