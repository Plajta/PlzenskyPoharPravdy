from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os
import requests
from dataloader.dataloader import Dataloader
import numpy as np
from dataloader.random_fact import generate_fact


#own modules
from dataloader.loc_compute import MapDataManipulator

#variables
nuke_config_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/other_data/nuke_config.json"
data_loader = Dataloader("data/csv_data/")

#loading nukes
nuke_config = open(nuke_config_path)
nuke_config_data = json.load(nuke_config)

#loading all the map data to RAM
map_manip = MapDataManipulator()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    #loading nukes
    nukes = []
    nuke_config = open(nuke_config_path)
    nuke_config_data = json.load(nuke_config)
    nukes = []

    for nuke in nuke_config_data["nukes"]:
        nukes.append({
            "name": nuke["name"],
            "energy": str(nuke["energy"]) + "kt",
            "value": nuke["value"]
        })

    print(nukes)
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
    map_manip.ProcessPoI(longitude, latitude, selected_nuke["fireball-radius"])

    #send nuke data to frontend #TODO add even more
    print("muzi:", data_muz)
    emit("explode_nuke", {
        "data":{
            "all_peope": data_all,
            "women": data_zen_percent,
            "men": data_muz_percent 
        },
        "nuke_data": selected_nuke,
        "coords": {
            "lat": latitude,
            "long": longitude
        }
    })

    

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)