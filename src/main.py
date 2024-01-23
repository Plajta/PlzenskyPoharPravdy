import sys
import os
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(main_dir,"src"))
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import requests
from dataloader.dataloader import Dataloader
import numpy as np
from dataloader.random_fact import generate_fact


#own modules
from dataloader.loc_compute import MapDataManipulator

#variables
nuke_config_path = os.path.join(main_dir,"data/other_data/nuke_config.json")
data_path = os.path.join(main_dir,"data/csv_data/")

#loading facts
data_loader = Dataloader(data_path)

#loading nukes
nuke_config = open(nuke_config_path)
nuke_config_data = json.load(nuke_config)

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

    return render_template('index.html', nuke_data=nukes)
    

@socketio.on('generate')
def handle_generate(data):
    #generate random fact in current region

    #city info
    city = ""
    try:
        x = requests.get("https://api.mapy.cz/v1/rgeocodeurl",
                        params={"lon": data["lng"], "lat": data["lat"]},
                        headers={"accept": "application/json",
                                "X-Mapy-Api-Key": "YmWIzXtT9Xx5rhFEc2rLnY8ymxWHpAW5D2pGf3P1QlA"})

        for y in x.json()["items"][0]["regionalStructure"]:
            if y["type"] == "regional.municipality":
                city = y["name"]
    except Exception as e:
        print(e)

    fact_message = generate_fact(data_loader, city)
    emit("send_random_fact", fact_message)

@socketio.on('get_city')
def handle_get_city(data):
    city = ""
    try:
        x = requests.get("https://api.mapy.cz/v1/rgeocodeurl",
                        params={"lon": data["lng"], "lat": data["lat"]},
                        headers={"accept": "application/json",
                                "X-Mapy-Api-Key": "YmWIzXtT9Xx5rhFEc2rLnY8ymxWHpAW5D2pGf3P1QlA"})

        for y in x.json()["items"][0]["regionalStructure"]:
            if y["type"] == "regional.municipality":
                city = y["name"]
    except Exception as e:
        print(e)
    print(city)
    emit("send_city", city)


@socketio.on('nukede')
def handle_nukede(data):
    print('received nukede message:', data)
    latitude = data["lat"]
    longitude = data["lng"]
    choosed_nuke = data["choosed_nuke"]

    #city info
    city = ""
    try:
        x = requests.get("https://api.mapy.cz/v1/rgeocodeurl",
                        params={"lon": longitude, "lat": latitude},
                        headers={"accept": "application/json",
                                "X-Mapy-Api-Key": "YmWIzXtT9Xx5rhFEc2rLnY8ymxWHpAW5D2pGf3P1QlA"})

        for y in x.json()["items"][0]["regionalStructure"]:
            if y["type"] == "regional.municipality":
                city = y["name"]
    except Exception as e:
        print(e)

    data_all = int(data_loader.query(f"uzemi_txt=='{city}' and vek_txt.isnull() and pohlavi_txt.isnull()", ["hodnota"])[0][0])
    data_muz = int(data_loader.query(f"uzemi_txt=='{city}' and vek_txt.isnull() and pohlavi_txt =='muž'", ["hodnota"])[0][0])
    data_zen = int(data_loader.query(f"uzemi_txt=='{city}' and vek_txt.isnull() and pohlavi_txt =='žena'", ["hodnota"])[0][0])

    data_muz_percent = round((data_muz / data_all) * 100, 2)
    data_zen_percent = round((data_zen / data_all) * 100, 2) 

    #get nuke params
    selected_nuke = None
    for nuke in nuke_config_data["nukes"]:
        if nuke["value"] == choosed_nuke:
            selected_nuke = nuke
            print("found nuke!")
    if selected_nuke == None:
        print("no nuke found!")
        emit("server_response", "no_nuke_found")

    #if everything is oke, we shall continue right?
    grassland, concrete, forest, water = map_manip.ProcessPoI(longitude, latitude, selected_nuke["fireball-radius"])

    #send nuke data to frontend #TODO add even more
    print("geo:", grassland,concrete,forest,water)
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
    socketio.run(app, allow_unsafe_werkzeug=True)