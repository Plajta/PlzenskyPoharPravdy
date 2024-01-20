import json
import urllib.request
import os
import hashlib

with open('data/other_data/fetch_config.json') as json_file:
    data = json.load(json_file)
keys = data.keys()
for key in keys:
    for file in data[key]:
        path = f"data/{key}/{file['name']}"
        if not os.path.isfile(path):
            urllib.request.urlretrieve(file["link"], path)
        else:
            print(f"{path}: {hashlib.sha1(open(path,'rb').read()).hexdigest()}")