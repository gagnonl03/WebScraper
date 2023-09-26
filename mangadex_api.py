import json
import math
import helper_functions as helper

import requests

base_url = "https://api.mangadex.org"
def filter_en_chapters(data_json):
    temp_list = list()
    for item in data_json:
        if item['attributes']['translatedLanguage'] == "en":
            temp_list.append((item['id'], item['attributes']['chapter'], item['attributes']['title'], item['attributes']['volume']))
    print(f"returned {len(temp_list)} items")
    return temp_list

def download_mangadex(manga_url):
    manga_id = manga_url.split("/")[4]
    r = requests.get(f"{base_url}/manga/{manga_id}").json()
    manga_name = r['data']['attributes']['title']['en']
    folder_name = helper.make_manga_folder(manga_name)
    response_json = requests.get(f"{base_url}/manga/{manga_id}/feed").json()

    print(type(response_json))
    total_items = response_json['total']
    required_requests = math.ceil(total_items / 100) - 1
    print(total_items)
    print(required_requests)
    data_list = response_json['data']
    en_chaps = list()
    en_chaps = en_chaps + filter_en_chapters(data_list)
    while required_requests > 0:
        r = requests.get(
            f"{base_url}/manga/{manga_id}/feed",
            params={
                "offset": required_requests * 100
            }
        ).json()
        en_chaps = en_chaps + filter_en_chapters(r['data'])
        required_requests -= 1

    print(en_chaps)
    print(len(en_chaps))
    en_chaps.sort(key=lambda x: float(x[1]))
    print(en_chaps)
    print(len(en_chaps))


download_mangadex("https://mangadex.org/title/a25e46ec-30f7-4db6-89df-cacbc1d9a900")