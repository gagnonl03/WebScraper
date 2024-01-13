import os
import shutil
import urllib.request


# makes manga folders
def make_folders(chapt_dict, manga_folder):
    replace_folders_status = 0
    for chapter in chapt_dict:
        chap_folder = manga_folder + "\\" + chapter
        if os.path.isdir(chap_folder) and replace_folders_status == 0:
            print(f"A folder for chapter {chapter} already exists")
            print("Would you like to replace folders that exist, or ignore them? (y/n)")
            print("Insert (ys/ns) to only skip this specific folder")
            user_input = input().strip().lower()
            if user_input == "y":
                shutil.rmtree(chap_folder)
                replace_folders_status = 1
                os.mkdir(chap_folder)
            elif user_input == "ys":
                shutil.rmtree(chap_folder)
                os.mkdir(chap_folder)
            elif user_input == "n":
                replace_folders_status = 2
        elif os.path.isdir(chap_folder) and replace_folders_status == 1:
            shutil.rmtree(chap_folder)
            os.mkdir(chap_folder)
        elif os.path.isdir(chap_folder) and replace_folders_status == 2:
            pass
        else:
            os.mkdir(chap_folder)


# creates a manga folder named for a
# user can select to replace an already existing folder if they'd like
def make_manga_folder(manga_name):
    folder_name = os.getcwd() + "\\" + format_filename(manga_name)
    if os.path.exists(folder_name):
        print("A folder with this manga's name already exists. Would you like to replace it? \n"
              "This will delete all subfolders and files! (y/n)")
        input1 = input()
        if input1.lower().strip() == "y":
            shutil.rmtree(folder_name)
            os.mkdir(folder_name)
        else:
            print("using existing directory")
    else:
        os.mkdir(folder_name)
    return folder_name


def download_from_urls(chapter_name, path_target, img_sources):
    x = 1
    total_images = len(img_sources)
    if len(os.listdir(path_target)) == 0:
        print(f"Downloading images for {chapter_name}")
        for uri in img_sources:
            print(f"Downloading image {x} / {total_images}")
            urllib.request.urlretrieve(uri, path_target + f"\\image_{x}.png")
            x += 1
    elif len(os.listdir(path_target)) < total_images:
        print(f"{chapter_name} appears damaged, attempting to repair")
        for index in range(len(img_sources)):
            if os.path.isfile(path_target + f"\\image_{index + 1}.png"):
                print(f"Image {index + 1} / {total_images} is OK")
            else:
                print(f"Downloading image {index + 1} / {total_images}")
                urllib.request.urlretrieve(img_sources[index], path_target + f"\\image_{index + 1}.png")

        print("Repair success")

    else:
        print(f"{chapter_name} is OK, skipping...")


def format_filename(name):
    formatted = (name.strip().replace(":", "-")
                 .replace("\n", "")
                 .replace("?", "")
                 .replace("*", " ")
                 .replace("\"", "'")
                 .replace("/", "_")
                 .replace("..", "")
                 .replace("<", "(lt)")
                 .replace(">", "(gt)"))

    return formatted

def get_indexed_input(prompt_string, data):
    print(prompt_string)
    for i in range(len(data)):
        print(f"[{i + 1}] {data[i]}")
    user_input = ""
    is_invalid = True
    while is_invalid:
        user_input = input()
        if user_input.lower().strip() == "exit":
            print("Forced program exit!")
            exit(900)
        if str.isdigit(user_input):
            user_input = int(user_input)
            if user_input <= len(data):
                is_invalid = False
            else:
                print("number is not in range")
        else:
            print("number needs to be an integer")

    return user_input - 1
