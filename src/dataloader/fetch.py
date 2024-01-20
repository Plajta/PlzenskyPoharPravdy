from urllib.request import urlretrieve
import json
import os
import img_loader

#get abs path
fetch_config_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/other_data/fetch_config.json"
img_data_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/img_data/"

fetch_config = open(fetch_config_path)
fetch_config_data = json.load(fetch_config)

#read image data
for obj in fetch_config_data["img_data"]:
   print(obj)
   urlretrieve(obj["link"], os.path.join(img_data_path, obj["name"]))

#modify images
img_loader.normalize_and_modify()