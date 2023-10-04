import json
import math
import os
import urllib.request

import helper_functions as helper

import requests

base_url = "https://api.mangadex.org"


def mangadex_download():
    return

def save_json(file_name, data):
    json_data = json.dumps(data, indent=4)
    with open(f"{file_name}.json", "w") as outfile:
        outfile.write(json_data)


def filter_en_chapters(data_json):
    temp_list = list()
    for item in data_json:
        if item['attributes']['translatedLanguage'] == "en":
            temp_list.append(
                (item['id'], item['attributes']['chapter'], item['attributes']['title'],
                 item['attributes']['volume']))
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

    en_chaps.sort(key=lambda x: float(x[1]))
    print(en_chaps)
    print(len(en_chaps))
    save_json("chaps", en_chaps)
    helper.make_chapter_folders_mangadex(folder_name, en_chaps)
    download_images(folder_name, en_chaps)


def download_images(folder_name, data):
    for chapter in data:
        print(f"Downloading images for chapter {chapter[1]}")
        download_chapter_images(helper.get_mangadex_chaptername(chapter),
                                helper.build_mangadex_foldername(folder_name, chapter),
                                chapter[0])


def download_chapter_images(chapter_name, chapter_folder_name, manga_id):
    response_json = requests.get("https://api.mangadex.org/at-home/server/" + manga_id).json()
    base_url = response_json["baseUrl"]
    chapter_hash = response_json["chapter"]["hash"]
    chap_url = base_url + "/data/" + chapter_hash + "/"
    x = 1
    images = response_json["chapter"]["data"]
    images_src = list()
    for image in images:
        images_src.append(chap_url + image)
    helper.download_from_urls(chapter_name, chapter_folder_name, images_src)


#download_mangadex("https://mangadex.org/title/a25e46ec-30f7-4db6-89df-cacbc1d9a900")
