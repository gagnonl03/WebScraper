import json
import math

import requests


def get_chapter_data(item_json):
    return(item['id'], )

base_url = "https://api.mangadex.org"
# https://mangadex.org/title/a25e46ec-30f7-4db6-89df-cacbc1d9a900
id = "a25e46ec-30f7-4db6-89df-cacbc1d9a900"
#title = "Kanojyo to Himitsu to Koimoyou"
r = requests.get(f"{base_url}/manga/{id}/feed")

response_json = r.json()

print(type(response_json))
total_items = response_json['total']
required_requests = math.ceil(total_items / 100) - 1
print(total_items)
print(required_requests)
data_list = response_json['data']
en_chaps = list()
for item in data_list:
    if item['attributes']['translatedLanguage'] == "en":
        en_chaps.append(item['id'], item[])
