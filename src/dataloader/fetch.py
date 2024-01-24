from urllib.request import urlretrieve
import json
import os.path
import hashlib

#own libs
import img_loader

#get abs path
main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fetch_config_path = os.path.join(main_dir, "config/fetch_config.json")
img_data_path = os.path.join(main_dir, "data/img_data/")

with open(fetch_config_path) as fetch_config:
    data = json.load(fetch_config)
keys = data.keys()

errors = False

print("Checking files")

for key in keys:
    for file in data[key]:
        path = f"data/{key}/{file['name']}"
        desired_hash = file["sha1"]
        print(f"{path}: {desired_hash}", end=" ", flush=True)
        if not os.path.isfile(path):
            print(f"- downloading", end=" ", flush=True)
            urlretrieve(file["link"], path)
        if desired_hash == hashlib.sha1(open(path,'rb').read()).hexdigest():
            print("✓")
        else:
            errors = True
            print("✗ - REMOVING")
            os.remove(path)
            mod = path[:-4]+"_mod.tif"
            if os.path.exists(mod):
                os.remove(mod)
            

#modify images
if errors:
    print("\033[31mRUN AGAIN, CURRUPTED FILES FOUND!\033[0m")
else:
    img_loader.normalize_and_modify()
