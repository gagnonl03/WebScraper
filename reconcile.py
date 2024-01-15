import os


current_path = os.getcwd()
print(os.listdir(current_path))

paths = list()

for dir in os.listdir(current_path):
    print(dir)
    if dir != ".git" and dir != ".idea" and dir != "__pycache__" and dir != "helper_functions.py" and dir != "LICENSE" and dir != "README.md"\
            and dir != "reconcile.py" and dir != "bato_scraper.py" and dir != ".gitignore" and dir != "chaps.json" and dir != "filteredchaps.json"\
            and dir != "mangadex_api.py" and dir != "mangascraper.py" and dir != "venv":
        paths.append(dir)

manga_paths = list()
for chap in paths:
    manga_paths.append(current_path + "\\" + chap)


print(manga_paths)
for i in range(len(manga_paths)):
    for dir in os.listdir(manga_paths[i]):
        print("checking " + dir)
        chap_dir = manga_paths[i] + "\\" + dir
        for image in os.listdir(chap_dir):
            image_old = chap_dir + "\\" + image
            print(image[1::].split(".")[0])
            image_num = (image[1::].split(".")[0])
            if image.split(".")[1] == "png":
                image_new = chap_dir + f"\\{image_num}.png"
                os.rename(image_old, image_new)
            else:
                pass