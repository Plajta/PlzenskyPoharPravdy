from urllib.request import urlretrieve
import json
import os
import hashlib

#own libs
import img_loader

#get abs path
fetch_config_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/other_data/fetch_config.json"
img_data_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/img_data/"

with open(fetch_config_path) as fetch_config:
    data = json.load(fetch_config)
keys = data.keys()

for key in keys:
    for file in data[key]:
        path = f"data/{key}/{file['name']}"
        if not os.path.isfile(path):
            urlretrieve(file["link"], path)
        else:
            print(f"{path}: {hashlib.sha1(open(path,'rb').read()).hexdigest()}")

#modify images
img_loader.normalize_and_modify()