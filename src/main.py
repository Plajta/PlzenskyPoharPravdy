import sys
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import requests
from dataloader.dataloader import Dataloader
import numpy as np
from dataloader.random_fact import generate_fact
from modules.loging import Logging
import yaml

LOG = Logging("Main")

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(main_dir,"src"))

#read server config
config = open(os.path.join(main_dir, "config", "server_conf.yaml"))
config_data = yaml.safe_load(config)

API_KEY = config_data["KEY"]
PORT = config_data["PORT"]
ADDR = config_data["ADDR"]

#own modules
from dataloader.loc_compute import MapDataManipulator
from dataloader.fetch import fetch_and_check

#variables
nuke_config_path = os.path.join(main_dir,"config/nuke_config.json")
data_path = os.path.join(main_dir,"data/csv_data/")

#loading facts
data_loader = Dataloader(data_path)

#loading nukes
nuke_config = open(nuke_config_path)
nuke_config_data = json.load(nuke_config)

#fetching and loading all data
fetch_and_check()

#loading all the map data to RAM
map_manip = MapDataManipulator()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    #loading nukesPrague
    nukes = []

    for nuke in nuke_config_data["nukes"]:
        nukes.append({
            "name": nuke["name"],
            "energy": str(nuke["energy"]) + "kt",
            "value": nuke["value"]
        })

    return render_template('index.html', nuke_data=nukes, api_key=API_KEY)
    

@socketio.on('generate')
def handle_generate(data):
    #generate random fact in current region

    #city info
    city = ""
    country = ""
    try:
        x = requests.get("https://api.mapy.cz/v1/rgeocodeurl",
                        params={"lon": data["lng"], "lat": data["lat"]},
                        headers={"accept": "application/json",
                                "X-Mapy-Api-Key": API_KEY})

        for y in x.json()["items"][0]["regionalStructure"]:
            if y["type"] == "regional.municipality":
                city = y["name"]
            if y["type"] == "regional.country":
                country = y["name"]
    except Exception as E:
        LOG.Error(f"City not found!")
        LOG.Error(E, 0)

    if country != "Česko":
        emit("client_response", "bad_country")
        return

    #generate random fact
    try:
        fact_message = generate_fact(data_loader, city)
    except Exception as E:
        LOG.Error("error while querying data & generating random fact, see below:")
        LOG.Error(E, 0)

    emit("send_random_fact", fact_message)

@socketio.on('get_city')
def handle_get_city(data):
    city = ""
    try:
        x = requests.get("https://api.mapy.cz/v1/rgeocodeurl",
                        params={"lon": data["lng"], "lat": data["lat"]},
                        headers={"accept": "application/json",
                                "X-Mapy-Api-Key": API_KEY})

        for y in x.json()["items"][0]["regionalStructure"]:
            if y["type"] == "regional.municipality":
                city = y["name"]
    except Exception as e:
        LOG.Error(e)
    LOG.Info("city: "+city)
    emit("send_city", city)

@socketio.on('nukede')
def handle_nukede(data):
    LOG.Info(f'received nukede message: {data}')
    latitude = data["lat"]
    longitude = data["lng"]
    choosed_nuke = data["choosed_nuke"]

    #city & country info
    city = ""
    country = ""
    try:
        x = requests.get("https://api.mapy.cz/v1/rgeocodeurl",
                        params={"lon": longitude, "lat": latitude},
                        headers={"accept": "application/json",
                                "X-Mapy-Api-Key": API_KEY})

        for y in x.json()["items"][0]["regionalStructure"]:
            if y["type"] == "regional.municipality":
                city = y["name"]
            if y["type"] == "regional.country":
                country = y["name"]
    except Exception as E:
        LOG.Error(f"City not found!")
        LOG.Error(E, 0)

    if country != "Česko":
        emit("client_response", "bad_country")
        return

    #fetching data
    try:
        data_all = int(data_loader.query(f"uzemi_txt=='{city}' and vek_txt.isnull() and pohlavi_txt.isnull()", ["hodnota"])[0][0])
        data_muz = int(data_loader.query(f"uzemi_txt=='{city}' and vek_txt.isnull() and pohlavi_txt =='muž'", ["hodnota"])[0][0])
        data_zen = int(data_loader.query(f"uzemi_txt=='{city}' and vek_txt.isnull() and pohlavi_txt =='žena'", ["hodnota"])[0][0])
    except Exception as E:
        LOG.Error("error while querying data, see below:")
        LOG.Error(E, 0)

    data_muz_percent = round((data_muz / data_all) * 100, 2)
    data_zen_percent = round((data_zen / data_all) * 100, 2) 

    #get nuke params
    selected_nuke = None
    for nuke in nuke_config_data["nukes"]:
        if nuke["value"] == choosed_nuke:
            selected_nuke = nuke
            LOG.Info("found nuke!")
    if selected_nuke == None:
        emit("client_response", "no_nuke_found")
        return

    #if everything is oke, we shall continue right?
    grassland, concrete, forest, water = map_manip.ProcessPoI(longitude, latitude, selected_nuke["fireball-radius"])

    #send nuke data to frontend #TODO add even more
    LOG.Info(f"geo: {grassland},{concrete},{forest},{water}")
    emit("explode_nuke", {
        "data": {
            "all_peope": data_all,
            "women": data_zen_percent,
            "men": data_muz_percent,
            "grass": f"{grassland} km\u00b2",
            "concrete": f"{concrete} km\u00b2",
            "forest": f"{forest} km\u00b2",
            "water": f"{water} km\u00b2"
        },
        "nuke_data": selected_nuke,
        "coords": {
            "lat": latitude,
            "long": longitude
        }
    })

    

if __name__ == '__main__':
    LOG.Info("Starting on port 5000")
    socketio.run(app, port=PORT, host=ADDR, allow_unsafe_werkzeug=True)
